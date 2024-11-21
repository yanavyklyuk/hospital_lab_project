from django.urls import path
from . import views
from dashboard.dash_apps.version1 import dashboard

urlpatterns = [
    path('v1/', views.create_dashboard, name='dashboard'),
    path('v2/', views.create_bokeh_dashboard, name='bokeh_dashboard'),
]