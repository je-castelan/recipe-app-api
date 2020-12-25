from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('loginv1/', views.UserLoginApiViewv1.as_view(), name='tokenv1'),
    path('loginv2/', views.UserLoginApiViewv2.as_view(), name='tokenv2'),
]
