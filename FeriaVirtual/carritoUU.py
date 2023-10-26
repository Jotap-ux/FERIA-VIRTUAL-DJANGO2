from django import forms
from django.shortcuts import render, redirect
#from .models import Producto
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import json
from django.contrib.auth import logout


def carrito(request):
   
    # Obtener el carrito del Local Storage y convertirlo a objetos Python
    carrito_str = request.session.get("carrito", "[]")
    carrito = json.loads(carrito_str)

    print(carrito)  # Agrega esta línea para imprimir el valor de 'carrito'

    
