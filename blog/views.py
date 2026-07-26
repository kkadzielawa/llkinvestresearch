import json

from django.views import generic
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import strip_tags
from django.utils.text import Truncator

from .models import MicroViewEntry, OptionsStudyEntry, Post


class PublishedEntryListView(generic.ListView):
    context_object_name = "posts"
    paginate_by = 6
    template_name = "entry_archive.html"
    model = None
    archive_eyebrow = ""
    archive_title = ""
    archive_copy = ""
    empty_state = "No research notes have been published yet."
    page_description = ""

    def get_queryset(self):
        return self.model.objects.filter(
            status=self.model.PostStatus.PUBLISHED
        ).order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archive_eyebrow"] = self.archive_eyebrow
        context["archive_title"] = self.archive_title
        context["archive_copy"] = self.archive_copy
        context["empty_state"] = self.empty_state
        context["page_title"] = f"{self.archive_title} | LLK Investment Research"
        context["page_description"] = self.page_description or self.archive_copy
        return context


class PublishedEntryDetailView(generic.DetailView):
    template_name = "post_detail.html"
    context_object_name = "post"
    model = None
    archive_label = ""
    archive_url_name = ""

    def get_queryset(self):
        return self.model.objects.filter(status=self.model.PostStatus.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["archive_label"] = self.archive_label
        context["archive_url_name"] = self.archive_url_name
        context["page_title"] = (
            f"{self.object.title} | {self.archive_label} | LLK Investment Research"
        )
        summary = Truncator(
            " ".join(strip_tags(self.object.content or "").split())
        ).chars(160, truncate="…")
        context["page_description"] = summary or (
            f"{self.object.title} from {self.archive_label} at LLK Investment Research."
        )
        article_url = self.request.build_absolute_uri(self.object.get_absolute_url())
        context["json_ld"] = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": self.object.title,
                "description": context["page_description"],
                "datePublished": self.object.created_on.isoformat(),
                "dateModified": self.object.updated_on.isoformat(),
                "author": {
                    "@type": "Person",
                    "name": self.object.author.get_full_name()
                    or self.object.author.username,
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "LLK Investment Research",
                },
                "mainEntityOfPage": article_url,
                "url": article_url,
            },
            cls=DjangoJSONEncoder,
        )
        context["og_type"] = "article"
        return context


class PostList(PublishedEntryListView):
    model = Post
    archive_eyebrow = "Archive"
    archive_title = "MacroView"
    archive_copy = (
        "A running index of market notes, macro observations, and research commentary."
    )


class PostDetail(PublishedEntryDetailView):
    model = Post
    archive_label = "MacroView"
    archive_url_name = "blog"


class MicroViewList(PublishedEntryListView):
    model = MicroViewEntry
    archive_eyebrow = "MicroView"
    archive_title = "Company and sector notes."
    archive_copy = (
        "A dedicated stream for bottom-up work across single names, "
        "competitive positioning, earnings quality, and catalysts."
    )
    empty_state = "No MicroView entries have been published yet."


class MicroViewDetail(PublishedEntryDetailView):
    model = MicroViewEntry
    archive_label = "MicroView"
    archive_url_name = "microview_blog"


class OptionsStudyList(PublishedEntryListView):
    model = OptionsStudyEntry
    archive_eyebrow = "Options Study"
    archive_title = "Trade structure before trade impulse."
    archive_copy = (
        "A workspace for options setups, scenario analysis, risk definitions, "
        "and timing notes that support disciplined execution."
    )
    empty_state = "No options studies have been published yet."


class OptionsStudyDetail(PublishedEntryDetailView):
    model = OptionsStudyEntry
    archive_label = "Options"
    archive_url_name = "options_study"
