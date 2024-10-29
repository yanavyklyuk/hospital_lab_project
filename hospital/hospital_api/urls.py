from django.urls import path
from .views.specialisation_view import SpecialisationList, SpecialisationDetail
from .views.doctor_view import DoctorList, DoctorDetail
from .views.schedule_view import ScheduleList, ScheduleDetail
from .views.favor_view import FavorList, FavorDetail
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
]