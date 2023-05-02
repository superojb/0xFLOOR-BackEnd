# Generated by Django 3.2.18 on 2023-04-26 15:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField(help_text='用户ID')),
                ('ip', models.GenericIPAddressField(help_text='登入IP')),
                ('address', models.CharField(help_text='登入地址', max_length=200)),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now, help_text='登入时间')),
            ],
            options={
                'verbose_name': '登录记录',
                'verbose_name_plural': '登录记录',
                'db_table': 'LoginLogs',
            },
        ),
    ]
