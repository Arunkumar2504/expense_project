# Generated by Django 5.2.1 on 2025-05-21 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0004_alter_expense_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='expense',
            table='expense_expense',
        ),
    ]
