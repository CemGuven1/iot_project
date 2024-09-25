from django.urls import path
from .views import receive_data, dashboard, device_detail, fetch_latest_data, register, login_view, logout_view, register_device, project_list, create_project

urlpatterns = [
    path('data-entry/', receive_data, name='data-entry'),
    path('projects/', project_list, name='project-list'),
    path('project/<int:project_id>/devices/', dashboard, name='dashboard'),
    path('project/<int:project_id>/register-device/', register_device, name='register_device'),
    path('projects/create/', create_project, name='create_project'), 
    
    path('device/<int:device_id>/', device_detail, name='device-detail'),
    path('device/<int:device_id>/latest-data/', fetch_latest_data, name='fetch-latest-data'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]
