from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import StaticViewSitemap

app_name = 'bocords'

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    # robots.txt는 반드시 가장 먼저
    path('robots.txt', views.robots),
    path('', views.home, name='home'),
    path('<int:id>/', views.details, name='details'),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",),

]
