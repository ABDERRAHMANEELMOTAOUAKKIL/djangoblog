from django.urls import path
from . import views
from .views import ArticleDetailView, AddPostView, UpdatePostView,DeletePostView,LikeView,PostsByCategoryView

urlpatterns = [
    path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    #categories urr
     path('category/<str:category_name>/', views.PostsByCategoryView.as_view(), name='category_posts'),

    #detailview for articles
    path('article/<int:pk>', ArticleDetailView.as_view(), name="article"),
    #addpost url
    path('add_post/', AddPostView.as_view(), name='add_post'),
    #update post
    path('article/edit/<int:pk>', UpdatePostView.as_view(), name="update_post"),
    #delete post
    path('article/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
    #like post
    path('like/<int:pk>', LikeView, name='like_post'),
    #search link
    path('search_post/', views.search_post, name='search_post'),

   



]