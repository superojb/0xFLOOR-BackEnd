# Generated by Django 3.2.18 on 2023-04-26 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MiningMachineProduct', '0002_currency_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Combo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='套餐名称', max_length=200)),
                ('currencyId', models.IntegerField(help_text='货币ID')),
            ],
            options={
                'verbose_name': '套餐',
                'verbose_name_plural': '套餐',
                'db_table': 'Combo',
            },
        ),
        migrations.CreateModel(
            name='ComboModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='模式名称', max_length=200)),
            ],
            options={
                'verbose_name': '套餐模式',
                'verbose_name_plural': '套餐模式',
                'db_table': 'ComboModel',
            },
        ),
        migrations.CreateModel(
            name='ComboPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(help_text='天数')),
            ],
            options={
                'verbose_name': '套餐周期',
                'verbose_name_plural': '套餐周期',
                'db_table': 'ComboPeriod',
            },
        ),
        migrations.CreateModel(
            name='MiningMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comboId', models.IntegerField(help_text='套餐ID')),
                ('name', models.CharField(help_text='矿机名称', max_length=200)),
            ],
            options={
                'verbose_name': '矿机',
                'verbose_name_plural': '矿机',
                'db_table': 'MiningMachine',
            },
        ),
        migrations.CreateModel(
            name='MiningMachineProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comboId', models.IntegerField(help_text='套餐ID')),
                ('comboPeriodId', models.IntegerField(help_text='套餐周期ID')),
                ('comboModelId', models.IntegerField(help_text='套餐模式ID')),
                ('miningMachineSpecificationId', models.IntegerField(help_text='矿机规格ID')),
                ('price', models.FloatField(help_text='价钱')),
            ],
            options={
                'verbose_name': '矿机产品',
                'verbose_name_plural': '矿机产品',
                'db_table': 'MiningMachineProduct',
            },
        ),
        migrations.CreateModel(
            name='MiningMachineSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('miningMachineId', models.IntegerField(help_text='矿机ID')),
                ('specification', models.CharField(help_text='规格', max_length=200)),
            ],
            options={
                'verbose_name': '矿机规格',
                'verbose_name_plural': '矿机规格',
                'db_table': 'MiningMachineSpecification',
            },
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name': '货币', 'verbose_name_plural': '货币'},
        ),
        migrations.AlterField(
            model_name='currency',
            name='imgUrl',
            field=models.CharField(help_text='Logo Url', max_length=500),
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(help_text='币名', max_length=200),
        ),
        migrations.AlterField(
            model_name='currency',
            name='nickname',
            field=models.CharField(help_text='简称', max_length=200),
        ),
        migrations.AlterField(
            model_name='currency',
            name='staticIncome',
            field=models.FloatField(help_text='静态收益'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='status',
            field=models.IntegerField(help_text='状态'),
        ),
    ]
