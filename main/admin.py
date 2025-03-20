from django.contrib import admin
from . import models

@admin.register(models.Signature)
class SignatureAdmin(admin.ModelAdmin):
    pass