import json
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import boto3
import io
import os

import esQuery

def handler(event, context):
    os.environ["TRANSFORMERS_CACHE"] = "/tmp"
    s3 = boto3.client("s3")
    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name'] 
    object_key = record['s3']['object']['key']
    print("object_key : ", object_key)
    print("Bucket_name  : ", bucket_name)
    #이미지 처리
    image_response  = s3.get_object(Bucket = bucket_name, Key = object_key)
    print("complete to load image from s3")
    image_data = image_response['Body'].read()
    raw_image = Image.open(io.BytesIO(image_data)).convert('RGB')
    #모델 로드
    model_path = os.path.join(os.environ['LAMBDA_TASK_ROOT'], "models")
    processor = BlipProcessor.from_pretrained(model_path)
    model = BlipForConditionalGeneration.from_pretrained(model_path)
    print("complete to load model")
    #모델에 이미지 넣음
    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    imageCaptionResult = processor.decode(out[0], skip_special_tokens=True)
    print("imageCaption : " , imageCaptionResult)
    #api trigger
    awsName = object_key.split("/")[-1]
    print("awsName : ", awsName)
    esQuery.elasticSearchApi(awsName, imageCaptionResult)