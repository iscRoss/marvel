#from turtle import title
from django.shortcuts import render
from inspect import getcallargs
import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import json
import requests
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from parte2.models import usuarios_atlas
from parte2.serializers import UsuarioSerializers, CurrentUserSerializer
from parte3.models import comics
from rest_framework.views import APIView
from django.http import HttpResponse
public_key = "bd07dc3cf0bdea676f7868d4c1f721f6"
private_key = "20b00992aa393d21b032585b0213a65dae16b5c7"
ts = 1
hash = "a3fb693ba08b04aedf9a6e479f825652"
url_comics = f"https://gateway.marvel.com:443/v1/public/comics?ts={ts}&apikey={public_key}&hash={hash}&"
url_characters = f"https://gateway.marvel.com:443/v1/public/characters?ts={ts}&apikey={public_key}&hash={hash}"
# Create your views here.
@csrf_exempt
def searchComicUser(request, id=0):

    response = requests.get(url_comics)

    lista_comics = []

    if request.method == "GET":
        print("Escriba su nombre de usuario")
        nombre = input("> ")
        if nombre:
            print("Escriba su contraseña")
            password = input("> ")
            if password:
                try:
                    userfc = usuarios_atlas.objects.filter(name=nombre, password= password).exists()
                    if userfc:
                        print("Registrar comics digite 1\n Buscar comics digite 2")
                        opcion = input("> ")
                        if opcion =="1":
                            print("Escriba el comics que quiera agregar")
                            name = input("> ")
                            queryUrlcomics = url_comics + f"&title={name}"
                            if name:
                                response = requests.get(queryUrlcomics)
                                if response.status_code == 200:
                                    response_json = json.loads(response.text)
                                    if response_json["data"]["results"]:
                                        for i in response_json["data"]["results"]:
                                            title =i["title"]
                                            id =i["id"]

                                            image = i["images"]
                                            onsaleDate = i["dates"][0]["date"]
                                            if image:
                                                path = i["images"][0]['path']
                                                extension = i["images"][0]['extension']
                                                image = path + "." + extension
                                        userf = usuarios_atlas.objects.get(name=nombre, password= password)

                                        c = comics()
                                        c.id_comics = id
                                        c.title = title
                                        c.image = image
                                        c.onsaleDate = onsaleDate
                                        c.user_crea_id = userf.id
                                        c.save()
                                        print("comics agregado")
                                        return JsonResponse("Comics agregados", safe=False)

                                    else:
                                        return JsonResponse("No existe comics", safe=False)

                        elif opcion =="2":
                            print("Buscar comic")
                            name = input("> ")
                            queryUrlcomics = url_comics + f"&title={name}"
                            if name:
                                response = requests.get(queryUrlcomics)
                            if response.status_code == 200:
                                response_json = json.loads(response.text)
                                for i in response_json["data"]["results"]:
                                    image = i["images"]
                                    onsaleDate = i["dates"][0]["date"]

                                    if image:
                                        path = i["images"][0]['path']
                                        extension = i["images"][0]['extension']
                                        image = path + "." + extension
                                    
                                    dic = {"id":i["id"],"name":i["title"],"image": image, "onsaleDate": onsaleDate}
                                    lista_comics.append(dic)
                            print(lista_comics)
                        return JsonResponse("Comics encontrado", safe=False)

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

        return JsonResponse(data, safe=False)
@csrf_exempt
def searchComicUserValidate(request, id=0):
    response = requests.get(url_comics)
    input_bucar = request.POST['input_bucar']
    lista_comics = []

    if input_bucar:
        queryUrlcomics = url_comics + f"&title={input_bucar}"
        response = requests.get(queryUrlcomics)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            for i in response_json["data"]["results"]:
                image = i["images"]
                onsaleDate = i["dates"][0]["date"]

                if image:
                    path = i["images"][0]['path']
                    extension = i["images"][0]['extension']
                    image = path + "." + extension
                    
                dic = {"id":i["id"],"name":i["title"],"image": image, "onsaleDate": onsaleDate}
                lista_comics.append(dic)
            return JsonResponse(lista_comics, safe=False)

    else:
        print("Debe escribir")
        return JsonResponse("Debe escribir un valor", safe=False)

class moduloComicsUser(TemplateView):
    template_name = "list_comics_part3.html"
    def get(self, request):
        if request.user.is_authenticated:
            users = User.objects.get(id=request.user.id)
            token = Token.objects.get(user_id=request.user.id)
            user_atlas =usuarios_atlas.objects.get(id=request.user.id)
            comic = comics.objects.filter(user_crea_id=request.user.id)
            return render(request, 'list_comics_part3.html', {'token':token,'user_atlas':user_atlas, 'comic':comic})
        else:
            return render(request, 'list_comics_part3.html')
@csrf_exempt
def agrega_comics(request, id=0):
    id_comics = request.POST['id_comics']
    queryUrlcomics = url_comics + f"&id={id_comics}"
    response = requests.get(queryUrlcomics)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        for i in response_json["data"]["results"]:
            title = i["title"]
            onsaleDate = i["dates"][0]["date"]

            image = i["images"]
            onsaleDate = i["dates"][0]["date"]

            if image:
                path = i["images"][0]['path']
                extension = i["images"][0]['extension']
                image = path + "." + extension
        c = comics()
        c.id_comics = id_comics
        c.title = title
        c.image = image
        c.onsaleDate = onsaleDate
        c.user_crea_id = request.user.id
        c.save()
        return JsonResponse("200", safe=False)
