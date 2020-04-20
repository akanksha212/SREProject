"""videoSummarizer URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from summarize import views 
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('register/', views.register, name = 'register'),
    path('userpage/', views.userpage, name ='userpage' ),
    path('video_upload', views.video_upload, name='video_upload'),
    path('', views.home)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 

 
    
    # urlpatterns = [  
    #     path('admin/', admin.site.urls),  
    #     path('emp', views.emp),  
    #     path('show',views.show),  
    #     path('edit/<int:id>', views.edit),  
    #     path('update/<int:id>', views.update),  
    #     path('delete/<int:id>', views.destroy),  
    # ]  