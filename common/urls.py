from django.urls import path
from . import views

urlpatterns = [
    path('uploadFile/start', views.start_upload, name='start_upload'),
    path('uploadFile/chunk', views.upload_chunk, name='upload_chunk'),
    path('uploadFile/complete', views.complete_upload, name='complete_upload'),
    path('getTimezones', views.get_timezones, name='get_timezones'),
]
