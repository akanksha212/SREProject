from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from summarize import views as core_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    url(r'^$', core_views.homepage, name='homepage'),
    url(r'^$',views.homepage, name='homepage'),
    path("login/", auth_views.LoginView.as_view(template_name='summarize/login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page='homepage'), name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
        
    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^video/new/$', core_views.video_new, name='video_new'),
    url(r'^video/(?P<pk>\d+)/$',core_views.video_detail, name='video_detail'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
