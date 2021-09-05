from django.urls import path
from basic_app import views

# TEMPLATE URLS! Need this other was template tag urls don't work.
app_name = 'basic_app'

urlpatterns = [
    path('register', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
]