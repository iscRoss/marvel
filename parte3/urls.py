import imp
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [

  path('list-user', (views.moduloComicsUser.as_view()), name = 'list-users'),
  path('buscar-comics', login_required(views.searchComicUserValidate), name = 'buscar-comics'),
  path('guardar-comics',login_required (views.agrega_comics), name = 'guardar-comics'),

]
