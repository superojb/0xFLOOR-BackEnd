from django.contrib import admin

# Register your models here.
from MiningMachineProduct.models.ComboModelModels import ComboModel
from MiningMachineProduct.models.ComboModels import Combo
from MiningMachineProduct.models.ComboPeriodModels import ComboPeriod
from MiningMachineProduct.models.CurrencyModels import Currency
from MiningMachineProduct.models.MiningMachineModels import MiningMachine
from MiningMachineProduct.models.MiningMachineProductModels import MiningMachineProduct
from MiningMachineProduct.models.MiningMachineSpecificationModels import MiningMachineSpecification


class ComboModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class ComboAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'currencyId']

class ComboPeriodAdmin(admin.ModelAdmin):
    list_display = ['id', 'day']

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'staticIncome']

class MiningMachineAdmin(admin.ModelAdmin):
    list_display = ['id', 'comboId', 'name']

class MiningMachineProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'comboId', 'comboPeriodId', 'comboModelId', 'miningMachineSpecificationId', 'price']

class MiningMachineSpecificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'miningMachineId', 'specification']

admin.site.register(ComboModel, ComboModelAdmin)
admin.site.register(Combo, ComboAdmin)
admin.site.register(ComboPeriod, ComboPeriodAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(MiningMachine, MiningMachineAdmin)
admin.site.register(MiningMachineProduct, MiningMachineProductAdmin)
admin.site.register(MiningMachineSpecification, MiningMachineSpecificationAdmin)
