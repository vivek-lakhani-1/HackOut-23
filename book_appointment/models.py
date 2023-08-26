from django.db import models

class AppointmentData(models.Model):
    Emailid = models.EmailField(unique=True)
    hospital_id = models.CharField(max_length=255)
    Hospital = models.CharField(max_length=255)
    Doctor = models.CharField(max_length=255)
    doctor_id = models.CharField(max_length=255)
    Slot = models.CharField(max_length=255)
    Date1 = models.CharField(max_length=255)
    Date2 = models.CharField(max_length=255)
    description = models.CharField(max_length=255)  
    scheduled = models.CharField(max_length=255)

    def __str__(self):
        return self.Emailid

class history_user(models.Model):
    Emailid = models.EmailField()
    history = models.JSONField()