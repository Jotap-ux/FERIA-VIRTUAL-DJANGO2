from django import forms
from django.shortcuts import render, redirect
from zeep import Client
import json

URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'


client = Client(URL_WEBSERVICE)


#----------SECCION GESTIONAR PAGO------------------
pago_exitoso = 1
pedido_idpedido = '282'



response = client.service.crearPago(pago_exitoso, pedido_idpedido)

#id_pedido = int(response)  # Convierte la respuesta a un entero
#id_pedido_str = str(id_pedido)  # Convierte el entero a una cadena

# Resto de tu lógica
#print(id_pedido_str)

print(response)