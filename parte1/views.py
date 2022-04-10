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


public_key = "bd07dc3cf0bdea676f7868d4c1f721f6"
private_key = "20b00992aa393d21b032585b0213a65dae16b5c7"
ts = 1
hash = "a3fb693ba08b04aedf9a6e479f825652"
url_comics = f"https://gateway.marvel.com:443/v1/public/comics?ts={ts}&apikey={public_key}&hash={hash}&"
url_characters = f"https://gateway.marvel.com:443/v1/public/characters?ts={ts}&apikey={public_key}&hash={hash}"
# Create your views here.
@csrf_exempt
def searchComic(request, id=0):

    response = requests.get(url_comics)
    response_character = requests.get(url_characters)

    lista_comics = []
    lista_character = []

    if request.method == "GET":
        print("Si desea realizar una busqueda de un comics escriba 1\nSi desea realizar busqueda por personajes escriba 2\nSi desea buscar por ambos escribir 3\nsi desea ver todos los personajes dar un enter")
        filter = input("> ")
        if filter=="2":
            print("Buscar por nombre del personaje")
            name = input("> ")
            queryUrl = url_characters + f"&name={name}"
            
            if name:
                response_character = requests.get(queryUrl)
            
            if response_character.status_code == 200:
                response_json_character= json.loads(response_character.text)
                for j in response_json_character["data"]["results"]:

                    image_character = j["thumbnail"]

                    if image_character:
                        path_character = j["thumbnail"]['path']
                        extension_character = j["thumbnail"]['extension']
                        image_character = path_character + "." + extension_character
                    appearances = j["comics"]["returned"]
                    dic_character = {"id":j["id"],"name":j["name"],"image": image_character, "appearances": appearances}
                    lista_character.append(dic_character)

            data = {
                    "personaje":lista_character
            }

            return JsonResponse(data, safe=False)
        elif filter == "1":
            print("Buscar por nombre del comics ")
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
            data = {
                    "comics":lista_comics,
            }
            return JsonResponse(data, safe=False)
        elif filter == "3":
            print("Escriba el nombre del comic o personaje ")
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
 
            if name:
                queryUrl = url_characters + f"&name={name}"
                response_character = requests.get(queryUrl)
            
            if response_character.status_code == 200:
                response_json_character= json.loads(response_character.text)
                for j in response_json_character["data"]["results"]:

                    image_character = j["thumbnail"]

                    if image_character:
                        path_character = j["thumbnail"]['path']
                        extension_character = j["thumbnail"]['extension']
                        image_character = path_character + "." + extension_character
                    appearances = j["comics"]["returned"]
                    dic_character = {"id":j["id"],"name":j["name"],"image": image_character, "appearances": appearances}
                    lista_character.append(dic_character)

            data = {
                    "personaje":lista_character,
                    "comics":lista_comics,

            }

            return JsonResponse(data, safe=False)
        else:
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

            if response_character.status_code == 200:
                response_json_character= json.loads(response_character.text)
                for j in response_json_character["data"]["results"]:

                    image_character = j["thumbnail"]

                    if image_character:
                        path_character = j["thumbnail"]['path']
                        extension_character = j["thumbnail"]['extension']
                        image_character = path_character + "." + extension_character
                    appearances = j["comics"]["returned"]
                    dic_character = {"id":j["id"],"name":j["name"],"image": image_character, "appearances": appearances}
                    lista_character.append(dic_character)

            data = {
                    "comics":lista_comics,
                    "personaje":lista_character
            }

        return JsonResponse(data, safe=False)

def home(request):
    if request.user.is_authenticated:
        users = User.objects.get(id=request.user.id)
        token = Token.objects.get(user_id=request.user.id)
        user_atlas =usuarios_atlas.objects.get(id=request.user.id)
        return render(request, 'index.html', {'token':token,'user_atlas':user_atlas})
    else:
        return render(request, 'index.html')

class moduloComics(TemplateView):
    template_name = "list_comics.html"
    def get(self, request):

        lista_comics = []
        lista_character = []
        
        response = requests.get(url_comics)
        response_character = requests.get(url_characters)

        if response.status_code == 200:
            response_json = json.loads(response.text)
            for i in response_json["data"]["results"]:
                image = i["images"]
                onsaleDate = i["dates"][0]["date"]

                if image:
                    path = i["images"][0]['path']
                    extension = i["images"][0]['extension']
                    image = path + "." + extension
                    
                context = {"id":i["id"],"name":i["title"],"image": image, "onsaleDate": onsaleDate}
                lista_comics.append(context)

        if response_character.status_code == 200:
            response_json_character= json.loads(response_character.text)
            for j in response_json_character["data"]["results"]:

                image_character = j["thumbnail"]

                if image_character:
                    path_character = j["thumbnail"]['path']
                    extension_character = j["thumbnail"]['extension']
                    image_character = path_character + "." + extension_character
                appearances = j["comics"]["returned"]
                dic_character = {"id":j["id"],"name":j["name"],"image": image_character, "appearances": appearances}
                lista_character.append(dic_character)
        context = {'object_list':lista_comics, 'object_list_character':lista_character}

        return render(request, self.template_name, context)

