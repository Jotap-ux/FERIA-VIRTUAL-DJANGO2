from django import forms
from django.shortcuts import render, redirect
from zeep import Client
import json

URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'


def listar_calibres():
    
    # Crea un cliente SOAP con la URL del servicio web
    client = Client(URL_WEBSERVICE)

    # Realizamos la petición al servicio web
    peticion_listar_calibres = client.service.listarCalibre()

    # Inicializa una lista para almacenar los datos de los calibres
    calibres_data = []

    # Itera a través de la lista de calibres en la respuesta
    for calibre in peticion_listar_calibres:
        calibre_data = {
            'desc_calibre': calibre.desccalibre,
            'id_calibre': calibre.idcalibre,
        }
        calibres_data.append(calibre_data)

    # Convierte la lista de calibres a una cadena JSON
    json_data = json.dumps(calibres_data, indent=4)

    return json_data



def listar_productos_combobox():
    
    # Crea un cliente SOAP con la URL del servicio web
    client = Client(URL_WEBSERVICE)

    # Realizamos la petición al servicio web
    peticion_listar_productos_combobox = client.service.listarProductosxIdyNombre()

    # Inicializa una lista para almacenar los datos de los productos
    productos_data = []

    # Itera a través de la lista de calibres en la respuesta
    for productos in peticion_listar_productos_combobox:
        producto_data = {
            'id_producto': productos.idproducto,
            'nombre_producto': productos.nombreproducto,
        }
        productos_data.append(producto_data)

    # Convierte la lista de calibres a una cadena JSON
    json_data = json.dumps(productos_data, indent=4)

    return json_data