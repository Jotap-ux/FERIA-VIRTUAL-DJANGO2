from django import forms
from django.shortcuts import render, redirect
#import zeep
from zeep import Client
import json



URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'


def autenticar_usuario(correoelectronico, contrasena):
    
    client = Client(URL_WEBSERVICE)
    
    peticion_login = client.service.listarlogin1(correoelectronico, contrasena)
    
    if peticion_login is None:
        # El usuario no existe, devuelve un valor especial o mensaje de error
        return json.dumps({'error': 'El usuario no existe'}, indent=4)
    
    
    response_data = {
        'Rut_usuario': peticion_login.identificador,
        'Tipo_usuario': peticion_login.tipousuario
    }
    
    # Convierte el diccionario a una cadena JSON
    json_data = json.dumps(response_data, indent=4)
    
    return json_data









