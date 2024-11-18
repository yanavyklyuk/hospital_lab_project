from django.urls import path
from dashboard.version1 import dashboard1_view
from .version1 import dashboard_app

urlpatterns = [
    path('v1/', dashboard1_view.dashboard_view, name='dashboard'),
]