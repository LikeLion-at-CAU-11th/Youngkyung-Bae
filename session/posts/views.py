from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post, Comment
import json
from rest_framework import generics
from rest_framework import mixins

from .serializers import PostSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# Create your views here.

def hello_world(request):
     if request.method == "GET":
         return JsonResponse({
             'status' : 200,
             'success' : True,
             'message' : '메시지 전달 성공!',
             'data': "Hello world",
         })
     
     
def introduction(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공!',
            'data' : [
		    {
			    "name" : "한윤호",
			    "age" : 23,
			    "major" : "Computer Science and Engineering"
		    },  
		    {
			    "name" : "배영경",
			    "age" : 21,
			    "major" : "Computer Science and Engineering"
		    }
	    ]
        })
    
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
        # 요청 메소드가 GET일 때는 게시글을 조회하는 View가 동작하도록 함
    if request.method == "GET":
        post = get_object_or_404(Post, pk=id)

        post_json={
            "id" : post.post_id,
            "writer" : post.writer,
            "content" : post.content,
            "category" : post.category,
        }

        return JsonResponse({
            'status' : 200,
            'message': '게시글 조회 성공',
            'data': post_json
        })
    
    # 요청 메소드가 PATCH일 때는 게시글을 조회하는 View가 동작하도록 함
    elif request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        update_post = get_object_or_404(Post, pk=id)

        update_post.content = body['content']
        update_post.save()

        update_post_json = {
            "id": update_post.post_id,
            "writer": update_post.writer,
            "content": update_post.content,
            "category": update_post.category,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
    
    elif request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=id)
        delete_post.delete()

        return JsonResponse({
                'status': 200,
                'message': '게시글 삭제 성공',
                'data': None
        })


@require_http_methods(["GET"])
def get_post_all(request):

		# Post 데이터베이스에 있는 모든 데이터를 불러와 queryset 형식으로 저장함
    post_all = Post.objects.all()
    
		# 각 데이터를 Json 형식으로 변환하여 리스트에 저장함
    post_json_all = []
    for post in post_all:
        post_json = {
            "id": post.post_id,
            "writer": post.writer,
            "content" : post.content,
            "category": post.category
        }
        post_json_all.append(post_json)
    
    return JsonResponse({
        'status': 200,
        'message': '게시글 전체 목록 조회 성공',
        'data': post_json_all
    })


@require_http_methods(["POST"])
def create_post(request):
    body = json.loads(request.body.decode('utf-8'))
		
		# ORM을 통해 새로운 데이터를 DB에 생성함
    new_post = Post.objects.create(
        writer = body['writer'],
        content = body['content'],
        category = body['category']
    )
		
		# Response에서 보일 데이터 내용을 Json 형태로 예쁘게 만들어줌
    new_post_json = {
        "id": new_post.post_id,
        "writer": new_post.writer,
        "content": new_post.content,
        "category": new_post.category
    }

    return JsonResponse({
        'status': 200,
        'message': '게시글 목록 조회 성공',
        'data': new_post_json
    })

@require_http_methods(["GET"])
def get_comment(request, post_id):
    comments = Comment.objects.filter(post=post_id)

    comment_json_list = []
    for comment in comments:
        commet_json = {
            'writer':comment.writer,
            'content':comment.content
        }
        comment_json_list.append(commet_json)
    
    return JsonResponse({
        'status':200,
        'message':'댓글 읽어오기 성공',
        'data':comment_json_list
    })


#@require_http_methods(["POST"])
#def create_comment(request, post_id):
#    body = json.loads(request.body.decode('utf-8'))

#    new_comment = Comment.objects.create(
#        writer = body['writer'],
#        content = body['content'],
#    )

#    new_comment_json = {
#        "id": new_post.post_id,
#        "writer": new_post.writer,
#        "content": new_post.content,
#        "category": new_post.category
#    }


@require_http_methods(["POST"])
def create_comment(request):                                
    body = json.loads(request.body.decode('utf-8'))

    comment_post = Post.objects.get(post_id = body["id"])

    new_comment = Comment.objects.create(
        writer = body['writer'],
        content = body['content'],
        post = comment_post
    )

    new_post_json = {
        "writer": new_comment.writer,
        "content": new_comment.content,
        "post": body['id']
    }

    return JsonResponse({
        'status': 200,
        'message': '댓글 생성 성공',
        'data': new_post_json
    })


# 게시글 작성
class PostList(APIView):
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 제대로 작동하지 않으면 400 에러

# 게시글 전체 불러오기
class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# 게시글 하나 아이디로 불러오기
class PostDetail(APIView):
    def get(self,request,id):
        post = get_object_or_404(Post, post_id=id)  # model.py에서 post_id로 짰기 때문에
        serializer = PostSerializer(post)
        return Response(serializer.data)

# 게시글 하나 수정하기
class PostDetail(APIView):
    def put(self,request,id):
        post = get_object_or_404(Post, post_id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시글 하나 삭제하기
class PostDetail(APIView):
    def delete(self,request,id):
        post = get_object_or_404(Post, post_id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#from rest_framework.response import Response
#from .models import Post
#from .serializers import PostSerializer

# APIView는 각 request method 마다 직접 serializer 처리 -> 중복 많음 -> Mixin

class PostListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # ListModelMixin : 데이터베이스에 저장되어 있는 데이터들을 목록 형태로 response body로 리턴
    # CreateModelMixin : 모델 인스턴스를 생성하고 저장
    
    def get(self, request, *args, **kwargs):
        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class PostDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # RetrieveModelMixin : 존재하는 모델 인스턴스를 리턴
    # UpdateModelMixin : 모델 인스턴스를 수정하여 저장
    # DestoryModelMixin : 모델 인스턴스를 삭제

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    

# genericsAPiview
# Mixin은 여러 개를 상속해야 하기 때문에 가독성이 떨어짐 -> rest_framework.generics에서 이들이 상속한 새로운 클래스를 정의

class PostListGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # ListCreateAPIView : GenericAPIView, ListModeMixin, CreateModelMixin을 상속받음

class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # RetrieveUpdateDestroyAPIView : GenericAPIView, RetrieveModeMixin, UpdateModeMixin, DestroyModelMixin을 상속받음


# viewset
# generics APIView를 통해 많이 간소화 but 여전히 공통적인 queryset과 serializer 따로 기재 -> ViewSet

from rest_framework import viewsets

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer   

post_list = PostViewSet.as_view({
    'get': 'list', #get 요청받으면 가지고있는 것 중 list 실행시킴
    'post': 'create',
})

post_detail_vs = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})