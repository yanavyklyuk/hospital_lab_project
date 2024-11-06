from django.urls import path
from .templates.frontend.doctor import doctor_view
from .templates.frontend.specialisation import specialisation_view
from .templates.frontend.patient import patient_view
from .templates.frontend.schedule import schedule_view
from .templates.frontend.favor import favor_view
from .templates.frontend.disease import disease_view
from .templates.frontend.disease_history import disease_history_view
from .templates.frontend.appointment import appointment_view

urlpatterns = [
    path('doctors/', doctor_view.doctor_list, name='doctor_list'),
    path('doctors/<int:id>/', doctor_view.doctor_detail, name='doctor_detail'),
    path('doctors/new/', doctor_view.doctor_form, name='doctor_form'),
    path('doctors/<int:id>/edit/', doctor_view.doctor_form, name='doctor_form'),
    path('specialisations/', specialisation_view.specialisation_list, name='specialisation_list'),
    path('specialisations/<int:id>/', specialisation_view.specialisation_detail, name='specialisation_detail'),
    path('patients/', patient_view.patient_list, name='patient_list'),
    path('patients/<int:id>/', patient_view.patient_detail, name='patient_detail'),
    path('patients/new/', patient_view.patient_form, name='patient_form'),
    path('patients/<int:id>/edit/', patient_view.patient_form, name='patient_form'),
    path('schedules/', schedule_view.schedule_list, name='schedule_list'),
    path('schedules/<int:id>/', schedule_view.schedule_detail, name='schedule_detail'),
    path('favors/', favor_view.favor_list, name='favor_list'),
    path('favors/<int:id>/', favor_view.favor_detail, name='favor_detail'),
    path('diseases/', disease_view.disease_list, name='disease_list'),
    path('diseases/<int:id>/', disease_view.disease_detail, name='disease_detail'),
    path('disease_histories/', disease_history_view.disease_history_list, name='disease_history_list'),
    path('disease_histories/<int:id>/', disease_history_view.disease_history_detail, name='disease_history_detail'),
    path('appointments/', appointment_view.appointment_list, name='appointment_list'),
    path('appointments/<int:id>/', appointment_view.appointment_detail, name='appointment_detail'),
]
