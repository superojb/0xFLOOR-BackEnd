from django.contrib import admin

from User.models.LoginLogsModels import LoginLogs
from User.models.RevenueAddressModels import RevenueAddress


class LoginLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'userId', 'ip', 'address', 'createTime']

class RevenueAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'userId', 'currencyId', 'address', 'notes']


admin.site.register(LoginLogs, LoginLogsAdmin)
admin.site.register(RevenueAddress, RevenueAddressAdmin)