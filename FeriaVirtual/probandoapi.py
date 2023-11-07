from django import forms
from django.shortcuts import render, redirect
from zeep import Client
import json

URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'


client = Client(URL_WEBSERVICE)

rutabuscar = '12345678'
peticion_vehi_transportista = client.service.listarTransportexRut(rutabuscar)

# Inicializa una lista para almacenar los datos de los productos
vehiculos_data = []

# Itera a través de la lista de productos en la respuesta
for vehiculo in peticion_vehi_transportista:
    vehiculo_data = {
        'capacidad_carga': vehiculo.capacidadcarga,
        'frigorificotrans': vehiculo.frigorificotrans,
        'modelo_idmodelo': vehiculo.modelo_idmodelo,
        'patente' : vehiculo.patente,                 
        'permisocirculacion': vehiculo.permisocirculacion,            
    }
    vehiculos_data.append(vehiculo_data)

# Convierte la lista de productos a una cadena JSON
json_data = json.dumps(vehiculos_data, indent=4)

print(json_data)
#return json_data