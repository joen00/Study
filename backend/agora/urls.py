from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path

from .views import *
from allauth.account import views
from rest_auth.views import LoginView as lg
#app_name = 'agora'
urlpatterns = [

    # 로그
    path(r'rest-auth/', include('rest_auth.urls')),
    path(r'rest-auth/registration', ONEUserRegisterView.as_view()),
    path("accounts/signup/inactive", user_inactive, name="account_inactive"),
    path(r'rest-auth/password/rest/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(r'password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    #path(r'rest-auth/login', LoginView.as_view(), name='account_inactive'),

    path(r'delete/account', delete_oneuser),
    path('activate/<str:uidb64>/<str:token>',
         CustomActivate.as_view()),  # email-url 클릭시 실행
    path('info', DetailONEUserAPIView.as_view()),  # 유저 정보
    path('keyword', set_oneuser_keywords),  # 유저 키워드 설정
    path('leave/<int:classroompk>', leave_classroom),  # 방 떠나기

]

""" template login 방식

    path('accounts/login/', ONEUserLoginView.as_view(), name='account_login'),
    path('accounts/logout/', views.logout ,name='account_logout'),
   
    path('accounts/signup/', ONEUserSignupView.as_view(), name='account_signup'),
    path("accounts/signup/inactive", ONEUserInactiveView.as_view(), name="account_inactive"),
    
    path(
        "accounts/confirm-email/",
        ONEUserEmailVerificationSentView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^accounts/confirm-email/(?P<key>[-:\w]+)/$",
        views.confirm_email,
        name="account_confirm_email",
    ),
   

    path("accounts/password/change/",ONEUSerPWChangeView.as_view(), name="account_change_password",),
    path("accounts/password/change/complete",pw_change_complete, name="account_change_password_complete",),
    path("accounts/password/set/", views.password_set, name="account_set_password"),


    # password reset
    path("accounts/password/reset/", ONEUserPWResetView.as_view(), name="account_reset_password"),
    path(
        "accounts/password/reset/done/",
        views.password_reset_done,
        name="account_reset_password_done",
    ),
    re_path(r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        ONEUserPWResetConfirmView.as_view(),
        name="account_reset_password_from_key",
    ),
    path(
        "accounts/password/reset/key/done/",
        pw_reset_complete,
        name="account_reset_password_from_key_done",
    ),



"""
