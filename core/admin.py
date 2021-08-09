from django.contrib import admin

from .models import (
    Appointment,
    Stock,
    BloodDonation,
    Hospital,
    BloodRequest,
    Withdraw,
)

@admin.register(Appointment)
class AppointmenAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'donate_date', 'status']

    def fullname(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['blood_type', 'blood_volume', 'receive_date', 'expire_date', 'expire_status']


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone', 'email']


@admin.register(BloodDonation)
class BloodDonationAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'blood_volume', 'donate_date', 'blood_type']

    def fullname(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'


@admin.register(BloodRequest)
class BLoodRequestAdmin(admin.ModelAdmin):
    list_display = ['hospital', 'blood_type', 'request_amount', 'withdraw_date', 'status']


@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    list_display = ['hospital', 'withdraw_date']