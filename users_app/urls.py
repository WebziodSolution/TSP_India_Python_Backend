from django.urls import path
from . import views

urlpatterns = [
    path('getAllUsers', views.get_all_users, name='get_all_users'),
    path('get/<str:id>', views.get_user, name='get_user'),
    path('create', views.create_user, name='create_user'),
    path('update/<str:id>', views.update_user, name='update_user'),
    path('delete/<str:id>', views.delete_user, name='delete_user'),
    path('login', views.user_login, name='user_login'),
    path('generateResetLink', views.generate_reset_link, name='generate_reset_link'),
    path('validateToken', views.validate_token, name='validate_token'),
    path('resetPassword', views.reset_password, name='reset_password'),
    path('uploadProfileImage', views.upload_profile_image, name='upload_profile_image'),
    path('deleteProfileImage', views.delete_profile_image, name='delete_profile_image'),
]
