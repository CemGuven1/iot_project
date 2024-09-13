from django.urls import path
from .views import receive_data, dashboard, device_detail, fetch_latest_data

urlpatterns = [
    path('data-entry/', receive_data, name='data-entry'),
    path('dashboard/', dashboard, name='dashboard'),
    path('device/<int:device_id>/', device_detail, name='device-detail'),
    path('device/<int:device_id>/latest-data/', fetch_latest_data, name='fetch-latest-data'),
]
