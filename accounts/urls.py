from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('feed/', views.UserFeedView.as_view(), name='user_feed'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    path('follow/<int:user_id>/', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>/', views.UserUnFollowView.as_view(), name='user_unfollow'),
    path('edit_user/', views.EditUserView.as_view(), name='user_edit'),

    # reset password 
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/confirm/complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]