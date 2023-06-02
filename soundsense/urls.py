"""
URL configuration for soundsense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('upload/', views.upload_music, name='upload'),
    path('song/<int:song_id>', views.song, name='song'),
    path('retrain/', views.retrain_model, name='retrain'),
    path('update_csvs/', views.update_csv_files, name='update_csv'),
    path('update_others/', views.update_genre_tags_processed, name='update_others')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
