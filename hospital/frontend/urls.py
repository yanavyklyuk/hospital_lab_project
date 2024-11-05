from django.urls import path
from .templates.frontend.doctor import doctor_view

urlpatterns = [
    path('doctors/', doctor_view.doctor_list, name='doctor_list'),
    path('doctors/<int:id>/', doctor_view.doctor_detail, name='doctor_detail'),
]
