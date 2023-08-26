from django.shortcuts import render
import base64
import requests
from rest_framework import response,status
from rest_framework.decorators import api_view
from decouple import config
import openai
import json
def ocr_image(filename):
    API_KEY = config("Google_Vision_API")
    VISION_URL = "https://vision.googleapis.com/v1/images:annotate?key=" + API_KEY
    image_path = f'{filename}'
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
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
    path = request.data['Image_Path']
    img_data = ocr_image(path)
    query = img_data+"Extract all details in json format and  make keys of this data good"
    data_ = str(text_to_json_chat_gpt(query)).replace("   ","")
    data_ = json.loads(data_)
    
    return response.Response({'status':200,'message':data_},status=status.HTTP_200_OK)
