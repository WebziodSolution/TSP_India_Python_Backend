from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_bank_account_info, name='create_bank_account_info'),
    path('get/<int:id>', views.get_bank_account_info_by_id, name='get_bank_account_info_by_id'),
    path('get/all', views.get_all_bank_account_info, name='get_all_bank_account_info'),
    path('update/<int:id>', views.update_bank_account_info, name='update_bank_account_info'),
    path('delete/<int:id>', views.delete_bank_account_info, name='delete_bank_account_info'),
    path('uploadPassbookImage', views.upload_passbook_image, name='upload_passbook_image'),
    path('deletePassbookImage/<int:companyId>/<int:bankId>', views.delete_passbook_image, name='delete_passbook_image'),
]
