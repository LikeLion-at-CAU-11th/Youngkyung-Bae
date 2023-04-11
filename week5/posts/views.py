from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Post, Comment
import json

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