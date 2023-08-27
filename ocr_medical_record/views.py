from django.shortcuts import render
import base64
import requests
from rest_framework import response,status
from rest_framework.decorators import api_view
from decouple import config
import openai
from .models import ocr_data
import json
import datetime

def ocr_image(image_base64):
    API_KEY = config("Google_Vision_API")
    VISION_URL = "https://vision.googleapis.com/v1/images:annotate?key=" + API_KEY
    request_body = {
        "requests": [
            {
                "image": {
                    "content": image_base64
                },
                "features": [
                    {
                        "type": "LABEL_DETECTION"
                    },
                    {
                        "type": "DOCUMENT_TEXT_DETECTION"
                    }
                ]
            }
        ]
    }


    response_data = requests.post(VISION_URL, json=request_body)
    tex = response_data.json()['responses'][0]['fullTextAnnotation']['text']
    return tex

def text_to_json_chat_gpt(query):
    
    api_key = config('Api_Key')
    openai.api_key = api_key
    prompt = query
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=prompt,
        max_tokens=3000,  
        n = 1
    )
    translated_text = response.choices[0].text
    return translated_text

@api_view(['POST'])
def digitalize_record(request):
    
    path = request.data['base64']
    img_data = ocr_image(path)
    
    query = img_data + "Extract all details in json format and  make keys of this data good"
    data_s = str(text_to_json_chat_gpt(query)).replace("   ","")
    print(data_s)
    ocr = ocr_data()
    ocr.hospital_id = "demo123"
    ocr.date = datetime.datetime.now()
    ocr.data = {'data' : data_s}
    ocr.save()
    return response.Response({'status':200,'message':data_s},status=status.HTTP_200_OK)
