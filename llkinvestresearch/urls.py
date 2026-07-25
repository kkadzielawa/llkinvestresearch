"""llkinvestresearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    ContactView,
    HomeView,
    MarketAnalyzerPageView,
    MicroViewPageView,
    OptionsStudyPageView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('microview/', MicroViewPageView.as_view(), name='microview_blog'),
    path('options-study/', OptionsStudyPageView.as_view(), name='options_study'),
    path('swing_trading/', OptionsStudyPageView.as_view(), name='swing_trading'),
    path('market-analyzer/', MarketAnalyzerPageView.as_view(), name='market_analyzer'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('blog/', include('blog.urls')),
]
