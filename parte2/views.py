from hashlib import md5
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import usuarios_atlas
from .serializers import UsuarioSerializers, CurrentUserSerializer
from django.contrib.auth.models import User

#from rest_framework.authentication import TokenAuthentication
#from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView,  FormView 
from django.urls import reverse_lazy
from django.contrib.auth.models import User

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import login, logout
from .forms import FormularioLogin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect

# Create your views here.
@csrf_exempt
def usersApi(request, id=0):
    if request.method == "GET":
        print("Opción 1 Consultar mis datos\nOpción 2 Todos los registros\nEscriba el número")
        opc = input("> ")
        print(opc)
        if opc == "1":
            print("Escriba su nombre de usuario")
            nombre = input("> ")
            if nombre:
                print("Escriba su contraseña")
                password = input("> ")
                if password:
                    try:
                        userfc = usuarios_atlas.objects.filter(name=nombre, password= password).exists()
                        if userfc:
                            userf = usuarios_atlas.objects.get(name=nombre, password= password)
                            user= usuarios_atlas.objects.filter(id=userf.id)
                            user_serializer = UsuarioSerializers(user, many=True)
                            print(user_serializer.data)
                            return JsonResponse(user_serializer.data, safe=False)
                        else:
                            print("Datos erroneos")
                            return JsonResponse("Datos erroneos", safe=False)       
                    except User.DoesNotExist:
                        return JsonResponse("Datos erroneos", safe=False)       
                else:
                    print("Esriba su contraseña")
                    return JsonResponse("Esriba su contraseña", safe=False)
            else:
                print("Esriba su nombre")
                return JsonResponse("Esriba su nombre", safe=False)
        elif opc=="2":
            user = usuarios_atlas.objects.all()
            user_serializer = UsuarioSerializers(user, many=True)
            print(user_serializer.data)
            return JsonResponse(user_serializer.data, safe=False)
        else:
            return JsonResponse("", safe=False)

    elif request.method == "POST":
        user_data = JSONParser().parse(request)
        user_serializer = UsuarioSerializers(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            user =  User.objects.create_user(user_data["name"], 'sinemail@coopel.com', user_data["password"])
            user.save()
            token = Token.objects.get_or_create(user_id=user.id)
            print(user.id)
            u = usuarios_atlas.objects.get(id=user.id)
            t = Token.objects.get(user_id=user.id)
            u.token = t.key
            u.password= user_data["password"]
            u.save()
            return JsonResponse("Usuario registrado", safe=False)
        else:
            print(user_serializer)
            return JsonResponse("Error al registrar", safe=False)
    elif request.method == "PUT":
        user_data = JSONParser().parse(request)
        user = usuarios_atlas.objects.get(id=user_data["id"])
        user_serializer =  UsuarioSerializers(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Usuario modificado", safe=False)
        else:
            return JsonResponse("Error al modificar", safe=False)
    elif request.method == "DELETE":
        user = usuarios_atlas.objects.get(id=id)
        user.delete()
        return JsonResponse("Usuario eliminado", safe=False)

class CrearuserApi(APIView):
    def post(self, request):
        data = {'status': 200}
        
        usuario = self.request.data['usuario']
        password = self.request.data['pass']
        edad = self.request.data['edad']

        user =  User.objects.create_user(usuario, 'sinemail@coopel.com', password)
        user_atlas = usuarios_atlas()
        t = Token()

        try:
        
            user.save()
            t.user_id = user.id
            t.save()
            user_atlas.id = user.id
            user_atlas.name = usuario
            user_atlas.password = password
            user_atlas.edad = edad
            user_atlas.token = t.key
            user_atlas.save()
            print(data)

            return Response(data)

        except User.DoesNotExist:
            data.append({'error': 'usuario no valido'})

        return Response(data)

class moduloUsers(TemplateView):
    model = User
    template_name = "list_user.html"
    def get_context_data(self, **kwargs):
        context = super(moduloUsers, self).get_context_data(**kwargs)
        users = User.objects.all()
        token = Token.objects.all().values("key","user_id")
        user_atlas =usuarios_atlas.objects.all()
        if users:
            context["users"] = users 
        if token:
            context["token"] = token 
        if user_atlas:
            context["user_atlas"] = user_atlas 
        return context

class Login(FormView):
    template_name = 'registration/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect (self.get_success_url())
        else:
            return super (Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login,self).form_valid(form)


def logoutusuario (request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')