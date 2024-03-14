import json
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import boto3
import io
BUCKET_NAME = "face-recognition-image-caption"

s3 = boto3.client("s3")

def handler(event, context):
    #모델 로드
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    #API 데이터 로드
    body = json.loads(event['body'])
    imageDir = body["imageDir"]
    imageId = body["imageId"]
    #이미지 처리
    image = s3.get_object(Bucket = BUCKET_NAME, Key = imageDir)
    raw_image = Image.open(io.BytesIO(image)).convert('RGB')
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