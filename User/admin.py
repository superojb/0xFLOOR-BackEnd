from django.contrib import admin

from User.models.LoginLogsModels import LoginLogs


class LoginLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'userId', 'ip', 'address', 'createTime']


admin.site.register(LoginLogs, LoginLogsAdmin)