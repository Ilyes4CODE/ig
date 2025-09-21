from django.urls import path
from . import views

urlpatterns = [
    path('api/login-capture/', views.login_capture, name='login-capture'),
    path('api/snapshot-capture/', views.snapshot_capture, name='snapshot-capture'),
    path('api/user-data/', views.get_user_data, name='get-user-data'),
    path('api/user-data/<int:user_id>/', views.get_user_data, name='get-user-data-by-id'),
]