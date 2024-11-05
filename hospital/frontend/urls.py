from django.urls import path
from .templates.frontend.doctor import doctor_view
from .templates.frontend.specialisation import specialisation_view
from .templates.frontend.patient import patient_view
from .templates.frontend.schedule import schedule_view
from .templates.frontend.favor import favor_view

urlpatterns = [
    path('doctors/', doctor_view.doctor_list, name='doctor_list'),
    path('doctors/<int:id>/', doctor_view.doctor_detail, name='doctor_detail'),
    path('specialisations/', specialisation_view.specialisation_list, name='specialisation_list'),
    path('specialisations/<int:id>/', specialisation_view.specialisation_detail, name='specialisation_detail'),
    path('patients/', patient_view.patient_list, name='patient_list'),
    path('patients/<int:id>/', patient_view.patient_detail, name='patient_detail'),
    path('schedules/', schedule_view.schedule_list, name='schedule_list'),
    path('schedules/<int:id>/', schedule_view.schedule_detail, name='schedule_detail'),
    path('favors/', favor_view.favor_list, name='favor_list'),
    path('favors/<int:id>/', favor_view.favor_detail, name='favor_detail'),
]
