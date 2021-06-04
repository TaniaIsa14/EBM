from django.contrib import admin

# Register your models here.
from ebm.mixins import ExportCsvMixin
from frontend_app.models import FrontendInfo, PackageType, Package, EventsOrganize, TeamMember, CheckoutInfo, EventBook, \
    UserInfo, PackageFood


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'user',
        'phone_number',
        'location',
    )
    actions = ["export_as_csv"]


@admin.register(FrontendInfo)
class FrontendAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'phone_number',
        'active_hour',
        'first_banner',
        'checkout_background',
        'login_background',
        'banner_title',
        'banner_subtitle',
        'description',
        'description_image',
        'description_banner',

    )
    actions = ["export_as_csv"]


@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'name',
    )
    actions = ["export_as_csv"]


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'type',
        'title',
        'subtitle',
        'description',
        'image',
        'package_cost',
    )
    actions = ["export_as_csv"]


@admin.register(PackageFood)
class PackageAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'package',
        'religion',
        'food',
        'price',
    )
    actions = ["export_as_csv"]


@admin.register(EventsOrganize)
class EventsOrganizeAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'title',
        'description',
        'image',
        'price',
    )
    actions = ["export_as_csv"]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'name',
        'role',
        'twitter',
        'facebook',
        'instagram',
        'linkedin',
    )
    actions = ["export_as_csv"]


@admin.register(EventBook)
class EventBookingAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'package',
        'user',
        'package_food',
        'my_venue',
        'time',
        'message',
        'people',
        'accept',
        'finished',
    )
    actions = ["export_as_csv"]


@admin.register(CheckoutInfo)
class EventBookingAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = (
        'user',
        'tran_id',
        'amount',
        'cart_type',
        'transaction_date',
        'bank_transaction_id',
    )
    actions = ["export_as_csv"]
