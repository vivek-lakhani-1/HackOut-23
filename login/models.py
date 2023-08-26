from django.db import models

class Register_Data(models.Model):
    Email_Id = models.EmailField(unique=True)
    Phone_No = models.CharField(max_length=256)
    Full_Name = models.CharField(max_length=256)
    Password = models.CharField(max_length=256)
    is_verified = models.BooleanField()
    
    def __str__(self):
        return self.Email_Id
    
    
    
