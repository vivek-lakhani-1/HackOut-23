# Generated by Django 4.2.4 on 2023-08-26 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_appointment', '0002_history_user_alter_appointmentdata_date1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history_user',
            name='Emailid',
            field=models.EmailField(max_length=254),
        ),
    ]
