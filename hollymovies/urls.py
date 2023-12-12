"""hollymovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth.views import LoginView
from django.urls import path, include

from accounts.views import SignUpView
from viewer.views import *

from viewer.models import *

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Country)
admin.site.register(Person)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Rating)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'), # vlastne views
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),     #defaultni views pre prihlasovanie
    path('hello', hello),
    path('hello1/<s>', hello1),
    path('hello2/', hello2),
    path('hello3/', hello3),
    path('', index, name="index"),
    path('movies/', movies, name="movies"),
    path('movie/<pk>/', movie, name='movie_detail'),
    path('movie/create/', MovieCreateView.as_view(), name="movie_create"),
    path('person/create', PersonCreateView.as_view(), name="person_create"),

    path('rate_movie/', rate_movie, name='rate_movie'),
    path('add_comment', add_comment, name='add_comment'),

]
