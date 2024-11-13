"""
URL configuration for the_library_of_ohara project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.most_popular_content, name='index'),

    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('create-category/', views.create_category, name='create_category'),
    path('user-collection/', views.user_collection, name='user_collection'),

    path('manga/', views.manga, name='manga'),
    path('user_manga/', views.user_manga_collection, name='user_manga'),
    path('manga/<int:manga_id>/', views.manga_detail, name='manga_detail'),
    path('manga-list/', views.manga_list, name='manga_list'),
    path('add_manga/<int:manga_id>/', views.add_manga_to_collection, name='add_manga'),
    path('remove_manga/<int:manga_id>/', views.remove_manga_from_collection, name='remove_manga'),

    path('anime/', views.anime, name='anime'),
    path('user_anime/', views.user_anime_collection, name='user_anime'),
    path('anime/<int:anime_id>/', views.anime_detail, name='anime_detail'),
    path('anime-list/', views.anime_list, name='anime_list'),
    path('add_anime/<int:anime_id>/', views.add_anime_to_collection, name='add_anime'),
    path('remove_anime/<int:anime_id>/', views.remove_anime_from_collection, name='remove_anime'),

    path('serie/', views.serie, name='serie'),
    path('user_serie/', views.user_serie_collection, name='user_serie'),
    path('serie/<int:serie_id>/', views.serie_detail, name='serie_detail'),
    path('serie-list/', views.serie_list, name='serie_list'),
    path('add_serie/<int:serie_id>/', views.add_serie_to_collection, name='add_serie'),
    path('remove_serie/<int:serie_id>/', views.remove_serie_from_collection, name='remove_serie'),

    path('movie/', views.movie, name='movie'),
    path('user_movie/', views.user_movie_collection, name='user_movie'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie-list/', views.movie_list, name='movie_list'),
    path('add_movie/<int:movie_id>/', views.add_movie_to_collection, name='add_movie'),
    path('remove_movie/<int:movie_id>/', views.remove_movie_from_collection, name='remove_movie'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
