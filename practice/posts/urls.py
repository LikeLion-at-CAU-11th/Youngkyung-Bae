from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name = 'hello_world'),
    path('introduction', introduction, name = 'introduction'),
    path('post_detail/<int:id>/', get_post_detail, ),
    path('new', create_post, name="create_post"),
    path('<int:id>', post_detail, name="post_detail"),
    path('all', get_post_all, name="get_post_all"),
    path('comment/<int:post_id>/', get_comment, name='get_comment'),
]