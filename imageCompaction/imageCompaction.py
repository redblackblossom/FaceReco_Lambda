import boto3
import io
from PIL import Image
import os


def imageResize(raw_image):
    (width, hight) = raw_image.size
    resize_factor = 1
    long_factor = 400
    if(width >hight):
        resize_factor = width / long_factor
    else:
        resize_factor = hight / long_factor
    if(resize_factor <= 1):
        return raw_image
    
    return raw_image.resize((int(width / resize_factor), int(hight / resize_factor)))

def handler(event, context):
    s3 = boto3.client("s3")
    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name']  # 버킷 이름
    object_key = record['s3']['object']['key']    # 객체 키(파일 경로 및 이름)
    _ , file_format  = os.path.splitext(object_key)
    file_format = file_format[1:].upper()
    if file_format == 'JPG':
        file_format = 'JPEG'
    #이미지 로드
    print(object_key)
    image_response = s3.get_object(Bucket =bucket_name, Key =object_key)
    image_data = image_response['Body'].read()
    raw_image = Image.open(io.BytesIO(image_data)).convert('RGB')
    #이미지 리사이즈
    compact_image = imageResize(raw_image)
    #압축된 이미지 파일 경로
    object_key_list = object_key.split('/')
    compact_image_key = "compaction" +"/" + object_key_list[1]
    #이미지 클래스를 바이트 형식으로 변환
    byte_stream = io.BytesIO()
    compact_image.save(byte_stream, format=file_format)
    compact_image_byte = byte_stream.getvalue()
    #이미지 s3에 저장
    s3.put_object(Bucket =bucket_name, Key =compact_image_key, Body = compact_image_byte)