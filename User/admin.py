from django.contrib import admin

from User.models.LoginLogsModels import LoginLogs
from User.models.RevenueAddressModels import RevenueAddress
from User.models.UserWalletModels import UserWallet


class LoginLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'userId', 'ip', 'address', 'createTime']

class RevenueAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'userId', 'currencyId', 'address', 'notes']

class UserWalletAdmin(admin.ModelAdmin):
    list_display = ['userWalletId', 'userId', 'type', 'address', 'privateKey', 'register']

admin.site.register(LoginLogs, LoginLogsAdmin)
admin.site.register(RevenueAddress, RevenueAddressAdmin)
admin.site.register(UserWallet, UserWalletAdmin)