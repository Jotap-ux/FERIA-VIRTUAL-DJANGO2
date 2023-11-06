from django import forms
from django.shortcuts import render, redirect
from zeep import Client
import json

URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'

client = Client(URL_WEBSERVICE)

marca = 'm01'
peticion_modelo = client.service.listarModelos(marca)

# Inicializa una lista para almacenar los datos de los productos
modelos_data = []

# Itera a través de la lista de calibres en la respuesta
for modelo in peticion_modelo:
    modelo_data = {
        'nombre_modelo': modelo.descmodelo,
        'id_modelo': modelo.idmodelo,
    }
    modelos_data.append(modelo_data)

# Convierte la lista de calibres a una cadena JSON
json_data = json.dumps(modelos_data, indent=4)

print(json_data)
#return json_data