from django.contrib import admin
from django.http import HttpResponseRedirect

from User.models.LoginLogsModels import LoginLogs
from User.models.RevenueAddressModels import RevenueAddress
from User.models.UserWalletModels import UserWallet
from User.models.UserCashOutApplyModels import UserCashOutApply


class LoginLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'userId', 'ip', 'address', 'createTime']

class RevenueAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'userId', 'currencyId', 'address', 'notes']

class UserWalletAdmin(admin.ModelAdmin):
    list_display = ['userId', 'currency', 'address', 'register']
    readonly_fields = ("userWalletId", "currency", "userId", "address", "privateKey", "register")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class UserCashOutApplyAdmin(admin.ModelAdmin):
    list_display = ['userId', 'address', 'currencyId', 'amount', 'status', 'updateTime']
    readonly_fields = ("userId", "address", "status", "currencyId", "amount", "note", "updateTime", "createTime")

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ["userId", "address", "status", "currencyId", "amount", "note", "updateTime", "createTime"]

        if obj.hax != "":
            readonly_fields.append('hax')
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if 'hax' not in form.cleaned_data:
            self.message_user(request, "没有需要修改！", level="ERROR")
            return
        obj.hax = form.cleaned_data['hax']
        obj.status = 3
        obj.save()

        UW = UserWallet.objects.get(userId=obj.userId_id, currency=obj.currencyId_id)
        UW.cashOut -= obj.amount
        UW.save()

    def response_change(self, request, obj):
        return HttpResponseRedirect(".")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(LoginLogs, LoginLogsAdmin)
admin.site.register(RevenueAddress, RevenueAddressAdmin)
admin.site.register(UserWallet, UserWalletAdmin)
admin.site.register(UserCashOutApply, UserCashOutApplyAdmin)