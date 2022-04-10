import imp
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [

  path('list-users', (views.moduloUsers.as_view()), name = 'list-users'),
  path('crear-usuario-api', views.CrearuserApi.as_view(), name = 'crear-usuario-api'),

]
