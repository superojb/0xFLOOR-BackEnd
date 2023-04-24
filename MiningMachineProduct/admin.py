from django.contrib import admin

# Register your models here.
from MiningMachineProduct.models.CurrencyModels import Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'staticIncome')

admin.site.register(Currency, CurrencyAdmin)