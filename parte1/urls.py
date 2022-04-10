import imp
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [

  path('list-comics', (views.moduloComics.as_view()), name = 'list-comics'),

]
