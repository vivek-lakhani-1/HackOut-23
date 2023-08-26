from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import response,status
from .models import AppointmentData,history_user
from login.views import check_register
import requests
from decouple import config
import json

@api_view(['POST'])
def book_appointment(request):
    if(request.data != {}):
        data = request.data
        for key,_ in data.items():
            if(str(data[key]).replace(" ","")==""):
                return response.Response({'message':'Please Provide ' + key + " Details"},status=status.HTTP_400_BAD_REQUEST)
        email = data['Emailid']
        print(email)
        internal_api_url = config('Dev_Url')+'/api/check_email_validate?email_id='+email
        resp = requests.get(internal_api_url,data={'email_id': email})
        status__c = resp.status_code
        if(status__c == 200):
                if(AppointmentData.objects.filter(Emailid=email).values()=={}):
                    app_db = AppointmentData()
                    app_db.Emailid = data["Emailid"]
                    app_db.hospital_id=data["hospital_id"]
                    app_db.Hospital=data["Hospital"]
                    app_db.Doctor=data["Doctor"]
                    app_db.doctor_id=data["doctor_id"]
                    app_db.Slot=data["Slot"]
                    app_db.Date1=data["Date1"]
                    app_db.Date2=data["Date2"]
                    app_db.description = data['description']
                    app_db.scheduled="No"
                    app_db.save()
                    return response.Response({'status':200,'message':'OK!!'},status=status.HTTP_200_OK)
                else:
                    return response.Response({'message':"Already Exist !! Please Send After Sometime"},status=status.HTTP_302_FOUND)
        else:   
                return response.Response({'message':"Please Verify Your Email Address"},status=status.HTTP_401_UNAUTHORIZED)
       
    else:
        return response.Response({'message':'Please Provide Details'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def history(request):
    email = request.data['Email_Id']
    data = AppointmentData.objects.filter(Emailid = email).values()[0]
    data.pop('doctor_id')
    data.pop('hospital_id')
    history = history_user.objects.filter(Emailid = email).values()
    past_data = []
    for i in range(len(history[0]['history'])):
        past_data.append(history[0]['history'][i])
    past_data.append(data)
    print(past_data)
    hs = history_user()
    hs.Emailid = email
    hs.history = past_data
    hs.save()
    return response.Response({'status':200,'message':'OK!!'},status=status.HTTP_200_OK)

def save_history(request):
    ema