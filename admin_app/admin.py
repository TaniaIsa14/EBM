from django.contrib import admin

# Register your models here.
from admin_app.models import Venue
from ebm.mixins import ExportCsvMixin


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'name',
        'location',
        'price',
    )
    actions = ["export_as_csv"]
