"""llkinvestresearch URL Configuration."""

from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from blog import views as blog_views

from .sitemaps import (
    ArchiveSitemap,
    ArticleSitemap,
    ContactSitemap,
    HomeSitemap,
    MarketAnalyzerSitemap,
    MicroViewSitemap,
    OptionsStudySitemap,
)
from .views import ContactView, HomeView, MarketAnalyzerPageView

sitemaps = {
    "home": HomeSitemap,
    "archives": ArchiveSitemap,
    "blog_posts": ArticleSitemap,
    "microview": MicroViewSitemap,
    "options": OptionsStudySitemap,
    "market_analyzer": MarketAnalyzerSitemap,
    "contact": ContactSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap_xml"),
    path("", HomeView.as_view(), name="home"),
    path("microview/", blog_views.MicroViewList.as_view(), name="microview_blog"),
    path(
        "microview/<slug:slug>/",
        blog_views.MicroViewDetail.as_view(),
        name="microview_detail",
    ),
    path(
        "options-study/",
        blog_views.OptionsStudyList.as_view(),
        name="options_study",
    ),
    path(
        "options-study/<slug:slug>/",
        blog_views.OptionsStudyDetail.as_view(),
        name="options_detail",
    ),
    path("swing_trading/", blog_views.OptionsStudyList.as_view(), name="swing_trading"),
    path("market-analyzer/", MarketAnalyzerPageView.as_view(), name="market_analyzer"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("blog/", include("blog.urls")),
]
