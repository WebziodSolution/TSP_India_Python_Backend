from django.urls import path
from . import views

urlpatterns = [
    path('getAllShift', views.get_all_shift, name='get_all_shift'),
    path('get/<str:id>', views.get_user_shift, name='get_user_shift'),
    path('create', views.create_user_shift, name='create_user_shift'),
    path('update/<str:id>', views.update_user_shift, name='update_user_shift'),
    path('delete/<str:id>', views.delete_user_shift, name='delete_user_shift'),
]
