from django.contrib import admin
from .models import Tutor, Skills, TutorScheduleItems, TutorRatings

# Register your models here.
admin.site.register(Tutor)
admin.site.register(Skills)
admin.site.register(TutorScheduleItems)
admin.site.register(TutorRatings)