from django.urls import path
from posts.views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # path('', hello_world, name = 'hello_world'),
    # path('introduction', introduction, name = 'introduction'),
    # path('<int:id>/', post_detail, name="post_detail"),
    # path('new/', create_post, name="create_post"),
    # path('all/', get_post_all, name="get_post_all"),
    # path('comment/<int:post_id>/', get_comment, name='get_comment'),
    # path('new_comment/', create_comment, name='create_comment'),

	#path('', PostList.as_view()),
    #path('<int:id>/', PostDetail.as_view()),

    #path('', PostListMixins.as_view()),
	#path('<int:pk>/', PostDetailMixins.as_view()),
    #path('', PostListGenericAPIView.as_view()),
    #path('<int:pk>/', PostDetailGenericAPIView.as_view()),
    path('', post_list),
    path('<int:pk>/', post_detail_vs),

]

# {Class명}.as_view() 방식으로 view를 연동

# router = DefaultRouter()
# router.register('', PostViewSet) #import 방식때문에 다름.

# urlpatterns = [
#     path('',include(router.urls)),
# ]