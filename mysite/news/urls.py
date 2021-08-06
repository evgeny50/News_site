from django.urls import path
from news.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(HomeNews.as_view()), name='home'),
    path('category/<int:category_id>/', NewsCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add_news/', CreateNews.as_view(), name='add_news'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
]