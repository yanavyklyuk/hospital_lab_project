from django.urls import path
from .views.specialisation_view import SpecialisationList, SpecialisationDetail
from .views.doctor_view import DoctorList, DoctorDetail
from .views.schedule_view import ScheduleList, ScheduleDetail
from .views.favor_view import FavorList, FavorDetail
from .views.appointment_view import AppointmentList, AppointmentDetail
from .views.disease_view import DiseaseList, DiseaseDetail
from .views.disease_history_view import DiseaseHistoryList, DiseaseHistoryDetail
from .views.patient_view import PatientList, PatientDetail
from .views.doctor_schedule_view import DoctorScheduleView
from .views.patient_diseases_view import PatientDiseasesView
from rest_framework.authtoken.views import obtain_auth_token
from .views.user_view import UserView
from django.conf import settings

urlpatterns = [
    path("specialisations/", SpecialisationList.as_view()),
    path("specialisations/<int:id>/", SpecialisationDetail.as_view()),
    path("doctors/", DoctorList.as_view()),
    path("doctors/<int:id>/", DoctorDetail.as_view()),
    path("schedules/", ScheduleList.as_view()),
    path("schedules/<int:id>/", ScheduleDetail.as_view()),
    path("favors/", FavorList.as_view()),
    path("favors/<int:id>/", FavorDetail.as_view()),
    path("appointments/", AppointmentList.as_view()),
    path("appointments/<int:id>/", AppointmentDetail.as_view()),
    path("diseases/", DiseaseList.as_view()),
    path("diseases/<int:id>/", DiseaseDetail.as_view()),
    path("disease_histories/", DiseaseHistoryList.as_view()),
    path("disease_histories/<int:id>/", DiseaseHistoryDetail.as_view()),
    path("patients/", PatientList.as_view()),
    path("patients/<int:id>/", PatientDetail.as_view()),
    path("api-token-auth/", obtain_auth_token),
    path("register/", UserView.as_view()),
    path("doctors/<int:doctor_id>/schedules/", DoctorScheduleView.as_view()),
    path("patients/<int:patient_id>/diseases_journal/", PatientDiseasesView.as_view())
]
