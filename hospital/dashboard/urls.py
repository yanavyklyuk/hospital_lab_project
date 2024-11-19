from django.urls import path
from . import views
from dashboard.dash_apps.finished_apps import simpleexample

urlpatterns = [
    path('v1/', views.create_dashboard, name='dashboard')
]