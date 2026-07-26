import json

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.urls import reverse

from .forms import ContactForm


class SEOContextMixin:
    page_title = "LLK Investment Research"
    page_description = (
        "Independent market notes across macro, digital assets, commodities, "
        "and options strategy."
    )
    og_type = "website"

    def get_json_ld(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("page_title", self.page_title)
        context.setdefault("page_description", self.page_description)
        context.setdefault("og_type", self.og_type)
        json_ld = self.get_json_ld()
        if json_ld:
            context["json_ld"] = json.dumps(json_ld, cls=DjangoJSONEncoder)
        return context


class HomeView(SEOContextMixin, TemplateView):
    template_name = "home.html"
    page_title = "LLK Investment Research | Independent Market Notes"
    page_description = (
        "Independent market notes across macro, digital assets, commodities, "
        "and options strategy."
    )

    def get_json_ld(self):
        home_url = self.request.build_absolute_uri(reverse("home"))
        organization = {
            "@type": "Organization",
            "@id": f"{home_url}#organization",
            "name": "LLK Investment Research",
            "url": home_url,
            "logo": self.request.build_absolute_uri("/static/img/logo.png"),
        }
        website = {
            "@type": "WebSite",
            "@id": f"{home_url}#website",
            "name": "LLK Investment Research",
            "url": home_url,
            "publisher": {"@id": f"{home_url}#organization"},
        }
        return {
            "@context": "https://schema.org",
            "@graph": [organization, website],
        }


class MicroViewPageView(SEOContextMixin, TemplateView):
    template_name = "microview_blog.html"
    page_title = "MicroView | LLK Investment Research"
    page_description = (
        "Short-form equity and sector notes focused on catalysts, earnings "
        "quality, and competitive positioning."
    )


class OptionsStudyPageView(SEOContextMixin, TemplateView):
    template_name = "options_study.html"
    page_title = "Options Study | LLK Investment Research"
    page_description = (
        "Options setups, scenario planning, and disciplined trade structure "
        "focused on risk framing."
    )


class MarketAnalyzerPageView(SEOContextMixin, TemplateView):
    template_name = "market_analyzer.html"
    page_title = "Market Analyzer | LLK Investment Research"
    page_description = (
        "A future home for valuation snapshots, cross-asset dashboards, and "
        "screening logic."
    )


class ContactView(SEOContextMixin, FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    page_title = "Contact Konrad Kadzielawa | LLK Investment Research"
    page_description = (
        "Get in touch about research, collaboration, or a market question "
        "worth exploring."
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_email"] = settings.CONTACT_EMAIL
        context["linkedin_url"] = "https://www.linkedin.com/in/konradkadzielawa/"
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        phone = cleaned_data.get("phone") or "Not provided"
        body = (
            f"Name: {cleaned_data['name']}\n"
            f"Email: {cleaned_data['email']}\n"
            f"Phone: {phone}\n\n"
            f"{cleaned_data['message']}"
        )
        send_mail(
            subject=f"Website inquiry from {cleaned_data['name']}",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        messages.success(
            self.request,
            "Thanks for reaching out. Your note has been sent successfully.",
        )
        return super().form_valid(form)
