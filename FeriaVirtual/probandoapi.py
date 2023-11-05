from django import forms
from django.shortcuts import render, redirect
from zeep import Client
import json

URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'

client = Client(URL_WEBSERVICE)

#def listarMontoSubasta(ruttransportista, idsubasta):

    #client = Client(URL_WEBSERVICE)

response = client.service.listarMontoSubastas(12345678, 266)



# Resto de tu lógica
print(response)

#return id_pedido_str