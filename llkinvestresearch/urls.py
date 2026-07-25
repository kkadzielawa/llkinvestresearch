"""llkinvestresearch URL Configuration."""

from django.contrib import admin
from django.urls import include, path

from blog import views as blog_views

from .views import ContactView, HomeView, MarketAnalyzerPageView


urlpatterns = [
    path("admin/", admin.site.urls),
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
