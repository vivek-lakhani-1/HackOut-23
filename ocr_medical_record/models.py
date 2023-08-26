from django.db import models

class ocr_data(models.Model):
    hospital_id = models.CharField(max_length=256)
    date = models.DateField()
    data = models.FileField(upload_to='Uploaded_Data')
    