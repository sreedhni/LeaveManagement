# Generated by Django 4.2.5 on 2024-01-30 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Leave', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
