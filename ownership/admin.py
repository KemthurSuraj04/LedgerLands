from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Landreg)
#admin.site.register(models.LandInspector)

# Register your models here.
