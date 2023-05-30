from rest_framework import serializers
from .models import Post

# ModelSerializer : 모델에 담긴 정보들 복제하여 코드의 중복을 줄인다.
class PostSerializer(serializers.ModelSerializer):

  class Meta:
    model = Post  # 시리얼라이즈 할 모델
    fields = "__all__"  # 모델에서 가져올 필드
