from django.contrib import admin
from . import models

admin.site.register(models.CompanySheet)
admin.site.register(models.Company)
admin.site.register(models.MainDomain)
admin.site.register(models.SubDomain)
admin.site.register(models.Prefecture)

