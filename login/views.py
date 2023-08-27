from django.shortcuts import render
from .serializer import Serializingdata
from rest_framework import response,status
from rest_framework.decorators import api_view
from cryptography.fernet import Fernet
from decouple import config
from .models import Register_Data as Registration_Database
from .serializer import Serializingdata
from .custom_functions import Validate_Email,Reset_Password
key = str(config('key'))
key = key.encode()
cipher_suite = Fernet(key)



@api_view(['GET'])
def Validate_Email_Id_Link(request,cipher_text):
    try:
        decrypted_text = cipher_suite.decrypt(cipher_text)
        email_id = decrypted_text.decode('utf-8')
        query = Registration_Database.objects.get(Email_Id=email_id)
        if(query != None):
            query.is_verified = True
            query.save()
            prm = {
                    'title' : 'Verified',
                    'message' : "Your Email Address is Verified"
                }
            return render(request,'verified.html',prm)
    except:
        # return response.Response({'status':404,'message':'Page Not Found !!'},status=status.HTTP_404_NOT_FOUND)
        return render(request,'404.html')
    
@api_view(['POST'])
def Register_Data(request):
        data = request.data
        if(data!={}):
            data['is_verified'] = False
            serializer = Serializingdata(data = data)
            if(serializer.is_valid()):
                if(not serializer.errors):
                    print(Validate_Email(request.data['Email_Id']))
                    serializer.save()
                    return response.Response({'status':200,'message':'OK!!'},status=status.HTTP_200_OK)         
            else:
                if('Email_Id' in serializer._errors):
                    if (serializer._errors['Email_Id'][0].code == 'unique'):
                        return response.Response({'status': 409,'message':"Emaild Id Exist"},status=status.HTTP_409_CONFLICT)
                else:
                    return response.Response({'status': 400,'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        else: 
            return response.Response({'status': 400,'message':"Please Enter Valid Details"},status=status.HTTP_400_BAD_REQUEST)
            
@api_view(['POST'])
def login_(request):
    data = request.data
    try:
        query = Registration_Database.objects.filter(Email_Id=data['Email_Id']).values()[0]
        if(query['is_verified']==True):
            if(query['Password']==data['Password']):
                return response.Response({'status':200,'message':'Password matched; login successful!'},status=status.HTTP_200_OK)
            else:
                return response.Response({'status':400,'message':'The entered passwords do not match.'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response({'status':422,'message':'Please ensure your email address is verified.'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except:
        return response.Response({'status':404,'message':'Please Enter Correct Data.'},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def resend_email_verify(request):
    if('Email_Id' in request.data):
        filter = Registration_Database.objects.filter(Email_Id = request.data['Email_Id'])
        if(filter.exists()):
            if(filter.values()[0]['is_verified'] == False):
                try:
                    pass
                    # Validate_Email(request.data['Email_Id'])
                except:
                    return response.Response({'status':404,'message':'Email is not Valid'},status=status.HTTP_200_OK)
                return response.Response({'status':200,'message':'Email Verification Link Sended. Please Check Your Inbox.'},status=status.HTTP_200_OK)
            else:
                return response.Response({'status':400,'message':'Emaild Id Already Verified'},status=status.HTTP_400_BAD_REQUEST)
        else:
             return response.Response({'status':400,'message':'Email Address Not Found.'},status=status.HTTP_400_BAD_REQUEST)
    else:
             return response.Response({'status':401,'message':'Email Id Not Exists Please Register First'},status=status.HTTP_401_UNAUTHORIZED)
         

@api_view(['POST'])     
def reset_password_link_gen(request):
    if('Email_Id' in request.data):
        filter = Registration_Database.objects.filter(Email_Id = request.data['Email_Id'])
        if(filter.exists()):
            if(filter.values()[0]['is_verified'] == False):
                return response.Response({'status':200,'message':'Please Verify Your Email First !!'},status=status.HTTP_200_OK)
            else:
                Reset_Password(request.data['Email_Id'])
                return response.Response({'status':200,'message':'Password Reset Link Sent to Your Regiser Mail Id'},status=status.HTTP_200_OK)
        else:
             return response.Response({'status':400,'message':'Email Address Not Found.'},status=status.HTTP_400_BAD_REQUEST)
    else:
             return response.Response({'status':401,'message':'Email Id Not Exists Please Register First'},status=status.HTTP_401_UNAUTHORIZED)
        
  
def reset_password(request,cipher_text):
    if(request.method == "POST"):
        try:
            decrypted_text = cipher_suite.decrypt(cipher_text)
            email_id = decrypted_text.decode('utf-8')
            query = Registration_Database.objects.get(Email_Id=email_id)
            if(query != None):
                query.Password = request.POST.get('Password')
                query.save()
                prm = {
                    'title' : 'Password Updated',
                    'message' : "New Password Has Set Sucessfully"
                }
                return render(request,'verified.html',prm)
        except:
            return render(request,'404.html')
    else:
            return render(request,'Reset_Pass.html')
        

@api_view(['GET'])
def check_register(request):
    try:
        email_id = request.GET.get('email_id')
        flg = Registration_Database.objects.filter(Email_Id = email_id).values()[0]['is_verified']
        return response.Response({'is_verified':flg},status=status.HTTP_200_OK)
    except:
        return response.Response({'error':'Not Exist'},status=status.HTTP_400_BAD_REQUEST)