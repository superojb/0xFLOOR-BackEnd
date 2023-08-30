from django.contrib import admin

# Register your models here.
from MiningMachineProduct.models.ComboModelModels import ComboModel
from MiningMachineProduct.models.ComboModels import Combo
from MiningMachineProduct.models.ComboPeriodModels import ComboPeriod
from MiningMachineProduct.models.CurrencyModels import Currency
from MiningMachineProduct.models.MiningMachineModels import MiningMachine
from MiningMachineProduct.models.MiningMachineProductModels import MiningMachineProduct, MiningMachineProductPostForm
from MiningMachineProduct.models.MiningMachineSettingModels import MiningMachineSetting
from MiningMachineProduct.models.MiningMachineSpecificationModels import MiningMachineSpecification
from MiningMachineProduct.models.PledgeProfitRatioModels import PledgeProfitRatio
from MiningMachineProduct.models.CurrencyNetworkModels import CurrencyNetwork


class ComboModelAdmin(admin.ModelAdmin):
    list_display = ['name']

class ComboAdmin(admin.ModelAdmin):
    list_display = ['name', 'currencyId']

class ComboPeriodAdmin(admin.ModelAdmin):
    list_display = ['Period']

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'Logo', 'staticIncome', 'Status']

class MiningMachineAdmin(admin.ModelAdmin):
    list_display = ['name', 'comboId']

class MiningMachineProductAdmin(admin.ModelAdmin):
    list_display = ['Name', 'ThePrice', 'powerConsumption', 'pledgeStatus', 'soldAndStock']
    form = MiningMachineProductPostForm

class MiningMachineSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']

class MiningMachineSpecificationAdmin(admin.ModelAdmin):
    list_display = ['specification', 'miningMachineId']

class PledgeProfitRatioAdmin(admin.ModelAdmin):
    list_display = ['CurrencyName', 'Pledge', 'Ratio']

admin.site.register(ComboModel, ComboModelAdmin)
admin.site.register(Combo, ComboAdmin)
admin.site.register(ComboPeriod, ComboPeriodAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(MiningMachine, MiningMachineAdmin)
admin.site.register(MiningMachineProduct, MiningMachineProductAdmin)
admin.site.register(MiningMachineSetting, MiningMachineSettingAdmin)
admin.site.register(MiningMachineSpecification, MiningMachineSpecificationAdmin)
admin.site.register(PledgeProfitRatio, PledgeProfitRatioAdmin)

