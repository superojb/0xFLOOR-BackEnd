import sys
from django.contrib import admin

from Order.models.OrderModels import Order
from Order.models.OrderItemModels import OrderItem
from Order.models.OrderPaymentInfoModels import OrderPaymentInfo
from Order.models.RevenueBindModels import OrderRevenueBind
from Order.models.TronConfirmationOfTransactionModels import TronConfirmationOfTransaction
from Order.models.TronIncomeRecordModels import TronIncomeRecord
from Order.models.TronRequestLogsModels import TronRequestLogs
from Order.models.MinerBindingModels import MinerBinding
from Tools.Tron.models.AccountResource import AccountResource


class OrderAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'orderName', 'userId', 'orderStatusId', 'createTime']
    search_fields = ("orderId",)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['orderItemId', 'orderId', 'productId', 'productTypeId', 'price']

class OrderPaymentInfoAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'type', 'price', 'confirmationUrl', 'createTime']

class OrderRevenueBindAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'revenueAddressId', 'createTime']

class TronConfirmationOfTransactionAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'type', 'result', 'updateTime', 'createTime']
    search_fields = ("orderId",)

class TronIncomeRecordAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'type', 'num', 'createTime']

class TronRequestLogsAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'url', 'params', 'response', 'type', 'createTime']

class MinerBindingAdmin(admin.ModelAdmin):
    list_display = ['orderId', 'miningMachineProductId', 'userId', 'minerAccount', 'miningStatusId', 'updateTime']
    search_fields = ("orderId",)
    readonly_fields = ("MinerBindingId", "orderId", "miningMachineProductId", "userId", "miningStatusId", "updateTime", "createTime")

    def save_model(self, request, obj, form, change):
        obj.miningStatusId = 2
        obj.minerAccount = form.cleaned_data['minerAccount']
        obj.save()

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderPaymentInfo, OrderPaymentInfoAdmin)
admin.site.register(OrderRevenueBind, OrderRevenueBindAdmin)
admin.site.register(TronConfirmationOfTransaction, TronConfirmationOfTransactionAdmin)
admin.site.register(TronIncomeRecord, TronIncomeRecordAdmin)
admin.site.register(TronRequestLogs, TronRequestLogsAdmin)
admin.site.register(MinerBinding, MinerBindingAdmin)

from Order.models.TronRequestLogsModels import TronRequestLogs
from Tools.Tron.TronAPI import TronAPI
from Backend.settings import company_Tron_address

# 获取Tron 基础内容
if "runserver" in sys.argv:
    response = TronAPI.GetAccountResource("Main", company_Tron_address)
    AccountResource(response)
    AccountResource.SetEnergyPrices(TronAPI.getEnergyPrices())
    AccountResource.SetBandWidthPrices(TronAPI.getBandWidthPrices())

    # 改变记录Log 方式
    TronAPI.Log = TronRequestLogs.Create