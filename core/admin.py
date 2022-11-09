from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Agentname)
admin.site.register(models.Lga)
admin.site.register(models.Party)
admin.site.register(models.States)
admin.site.register(models.Ward)
admin.site.register(models.PollingUnit)
admin.site.register(models.AnnouncedLgaResults)
admin.site.register(models.AnnouncedPuResults)
admin.site.register(models.AnnouncedWardResults)
admin.site.register(models.AnnouncedStateResults)
