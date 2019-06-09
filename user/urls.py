from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    # path('register_or_login/', views.RegisterOrLogin.as_view(), name='register_or_login'),
    path('login/', views.MyLoginView.as_view(template_name='user/register_or_login.html'), name='user_login'),
    path('logout/', views.MyLogoutView.as_view(), name='user_logout'),
]