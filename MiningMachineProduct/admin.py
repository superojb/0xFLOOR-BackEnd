from django.contrib import admin

# Register your models here.
from MiningMachineProduct.models.ComboModelModels import ComboModel
from MiningMachineProduct.models.ComboModels import Combo
from MiningMachineProduct.models.ComboPeriodModels import ComboPeriod
from MiningMachineProduct.models.CurrencyModels import Currency
from MiningMachineProduct.models.MiningMachineModels import MiningMachine
from MiningMachineProduct.models.MiningMachineProductModels import MiningMachineProduct
from MiningMachineProduct.models.MiningMachineSettingModels import MiningMachineSetting
from MiningMachineProduct.models.MiningMachineSpecificationModels import MiningMachineSpecification


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
    list_display = ['id', 'comboId', 'comboPeriodId', 'comboModelId', 'miningMachineSpecificationId', 'price']

class MiningMachineSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']

class MiningMachineSpecificationAdmin(admin.ModelAdmin):
    list_display = ['specification', 'miningMachineId']

admin.site.register(ComboModel, ComboModelAdmin)
admin.site.register(Combo, ComboAdmin)
admin.site.register(ComboPeriod, ComboPeriodAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(MiningMachine, MiningMachineAdmin)
admin.site.register(MiningMachineProduct, MiningMachineProductAdmin)
admin.site.register(MiningMachineSetting, MiningMachineSettingAdmin)
admin.site.register(MiningMachineSpecification, MiningMachineSpecificationAdmin)
