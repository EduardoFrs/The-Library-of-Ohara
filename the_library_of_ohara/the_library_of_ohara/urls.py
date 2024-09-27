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
    path('', views.index, name='index'),
    path('manga/', views.manga, name='manga'),
    path('anime/', views.anime, name='anime'),
    path('serie/', views.serie, name='serie'),
    path('movie/', views.movie, name='movie'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('create-category/', views.create_category, name='create_category'),
    path('anime/<int:anime_id>/', views.anime_detail, name='anime_detail'),
    path('manga/<int:manga_id>/', views.manga_detail, name='manga_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
