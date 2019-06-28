from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from users import views as user_view

urlpatterns = [
    path('index/', views.index, name='index-home'),
    path('', views.device_index, name='device-index'),
    path('<str:name>', views.index_phone, name='index_phone'),
    path('blog/', PostListView.as_view(), name='blog-home'),
    path('post_detail/?P<id>/', views.post_detail, name='post-detail'),
    path('post_detail/?P<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post_detail/?P<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('blog/new/', PostCreateView.as_view(), name='post-create'),
    path('index/compare_in/', views.compare, name='compare'),
    path('index/compare_in/<str:value>', views.compare, name='index-compare'),
    path('demo/', views.demo, name='demo'),
    path('under_filter/', views.filter_result, name='range_result'),
    path('under_filter/<str:range_val>', views.filter_result, name='range_res'),
    path(r'like/', views.like_post, name='like_post'),
    path(r'add_like/', user_view.add_to_like, name='add_like')
]