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
from Tools.Khala.KhalaMange import KhalaMange
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
    list_display = ['MinerBindingId', 'miningMachineProductId', 'PledgeProfitRatioString', 'userId', 'minerAccount', 'miningStatusId', 'updateTime']
    search_fields = ("MinerBindingId",)
    readonly_fields = ("MinerBindingId", "orderId", "miningMachineProductId", "userId", "miningStatusId", "updateTime", "createTime")

    def save_model(self, request, obj, form, change):
        if obj.minerAccount != None:
            self.message_user(request, "不可修改机器账号！", level="ERROR")
            return

        obj.minerAccount = form.cleaned_data['minerAccount']

        result = MinerBinding.GetPledgeInfo(obj.MinerBindingId, obj.userId_id)

        # 如果质押状态也确定， 或者无需质押
        if result.type == 2 or result.PledgeNum == 0:
            if obj.miningStatusId == 7:
                obj.miningStatusId = 7
            elif result.status == 1 or result.PledgeNum == 0:
                # 檢查是否在工作
                response = KhalaMange.GetPhalaComputationSessions(obj.minerAccount, obj.MinerBindingId)
                IsWork = KhalaMange.getPhalaComputationIsWork(response)
                obj.miningStatusId = 4 if IsWork else 3
            else:
                obj.miningStatusId = 2
        else:
            obj.miningStatusId = 2

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
