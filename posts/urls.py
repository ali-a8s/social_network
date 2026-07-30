from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'), 
    path('post/detail/<int:post_id>/<slug:post_slug>/', views.PostDeteilView.as_view(), name='post_detail'),
    path('post/delete/<int:post_id>/', views.PostDeleteView.as_view(), name='post_delete'),
]
