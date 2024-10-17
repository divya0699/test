from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('blog_list', views.blog_list, name='blog_list'),
    path('<int:id>/', views.blog_detail, name='blog_detail'),
    path('search/', views.blog_search, name='blog_search'), 
]

