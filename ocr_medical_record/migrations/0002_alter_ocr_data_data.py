# Generated by Django 4.2.4 on 2023-08-27 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_medical_record', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocr_data',
            name='data',
            field=models.JSONField(),
        ),
    ]
