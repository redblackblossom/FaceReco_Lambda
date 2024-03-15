import json
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import boto3
import io
import os

def handler(event, context):
    os.environ["TRANSFORMERS_CACHE"] = "/tmp"
    BUCKET_NAME = "face-recognition-image-caption"
    s3 = boto3.client("s3")
    #모델 로드
    model_path = os.path.join(os.environ['LAMBDA_TASK_ROOT'], "models")
    processor = BlipProcessor.from_pretrained(model_path)
    model = BlipForConditionalGeneration.from_pretrained(model_path)
    #API 데이터 로드
    if isinstance(event['body'], (str, bytes, bytearray)):
        body = json.loads(event['body'])
    else:
        body = event['body']
    imageDir = body["imageDir"]
    imageId = body["imageId"]
    #이미지 처리
    image_response  = s3.get_object(Bucket = BUCKET_NAME, Key = imageDir)
    image_data = image_response['Body'].read()
    raw_image = Image.open(io.BytesIO(image_data)).convert('RGB')
    #모델에 이미지 넣음
    inputs = processor(raw_image, return_tensors="pt")
    out = model.generate(**inputs)
    imageCaptionResult = processor.decode(out[0], skip_special_tokens=True)

    resultApi = {
        "imageId" : imageId,
        "caption" : imageCaptionResult
    }

    return{
        "statusCode": 200,
        'body': json.dumps(resultApi)
    }