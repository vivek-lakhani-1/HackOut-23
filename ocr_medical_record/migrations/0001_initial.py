# Generated by Django 4.2.4 on 2023-08-27 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ocr_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_id', models.CharField(max_length=256)),
                ('date', models.DateField()),
                ('data', models.FileField(upload_to='Uploaded_Data')),
            ],
        ),
    ]
