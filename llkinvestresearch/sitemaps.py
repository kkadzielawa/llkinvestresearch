from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import MicroViewEntry, OptionsStudyEntry, Post


class StaticPageSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return [
            "home",
            "market_analyzer",
            "contact",
        ]

    def location(self, item):
        return reverse(item)


class HomeSitemap(StaticPageSitemap):
    priority = 1.0

    def items(self):
        return ["home"]


class ArchiveSitemap(StaticPageSitemap):
    priority = 0.8

    def items(self):
        return ["blog", "microview_blog", "options_study"]


class ContactSitemap(StaticPageSitemap):
    priority = 0.5

    def items(self):
        return ["contact"]


class MarketAnalyzerSitemap(StaticPageSitemap):
    priority = 0.4

    def items(self):
        return ["market_analyzer"]


class PublishedEntrySitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 0.8
    model = None

    def items(self):
        return self.model.objects.filter(status=self.model.PostStatus.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_on


class ArticleSitemap(PublishedEntrySitemap):
    model = Post
    priority = 0.9


class MicroViewSitemap(PublishedEntrySitemap):
    model = MicroViewEntry


class OptionsStudySitemap(PublishedEntrySitemap):
    model = OptionsStudyEntry
