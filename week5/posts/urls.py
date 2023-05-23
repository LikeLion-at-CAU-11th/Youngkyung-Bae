from django.urls import path
from posts.views import *


urlpatterns = [
    # path('', hello_world, name = 'hello_world'),
    # path('introduction', introduction, name = 'introduction'),
    # path('<int:id>/', post_detail, name="post_detail"),
    # path('new/', create_post, name="create_post"),
    # path('all/', get_post_all, name="get_post_all"),
    # path('comment/<int:post_id>/', get_comment, name='get_comment'),
    # path('new_comment/', create_comment, name='create_comment'),
	path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()),
]

# {Class명}.as_view() 방식으로 view를 연동