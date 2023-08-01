from rest_framework import serializers
from .models import Post
from config import settings
import boto3
from botocore.exceptions import ClientError

# ModelSerializer : 모델에 담긴 정보들 복제하여 코드의 중복을 줄인다.
class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = Post  # 시리얼라이즈 할 모델
    fields = "__all__"  # 모델에서 가져올 필드

  def validate(self, data):
        image = data.get('thumbnail')
        if not is_image(image):
            raise serializers.ValidationError('Not an image file')
        else:
            s3_url = self.save_image(image)
            if not s3_url:
                raise serializers.ValidationError('Invalid image file')
            data['thumbnail'] = s3_url
        return data
  
  def save_image(self, image):
        try:
            # s3 client 생성
            s3 = boto3.client('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_REGION)

            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            file_path = image.name
            s3.upload_fileobj(image, bucket_name, file_path)    # s3에 업로드

            s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_path}"
            return s3_url
        except:
            print("s3 upload error")
            return None
  

	
# 이미지 파일 검사
def is_image(image):
    file_extensions = ['jpg', 'jpeg', 'png', 'gif']
    file_extension = image.name.split('.')[-1].lower()  # 이미지의 확장자

    if file_extension not in file_extensions:
        return False
    return True