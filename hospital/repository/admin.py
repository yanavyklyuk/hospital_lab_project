from django.contrib import admin
from repository.models.patient import Patient
from repository.models.specialisation import Specialisation
from repository.models.doctor import Doctor
from repository.models.schedule import Schedule
from repository.models.disease import Disease
from repository.models.disease_history import DiseaseHistory
from repository.models.favor import Favor
from repository.models.appointment import Appointment

# Register your models here.
admin.site.register(Patient)
admin.site.register(Specialisation)
admin.site.register(Doctor)
admin.site.register(Schedule)
admin.site.register(Disease)
admin.site.register(DiseaseHistory)
admin.site.register(Favor)
admin.site.register(Appointment)