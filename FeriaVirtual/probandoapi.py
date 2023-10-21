from django import forms
from django.shortcuts import render, redirect
#import zeep
from zeep import Client
import json

URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'


def obtener_productos_json():
    
    # Crea un cliente SOAP con la URL del servicio web
    client = Client(URL_WEBSERVICE)
    
    # Realizamos la petición al servicio web
    peticion_listar_productos = client.service.listarProductos()
    
    # Inicializa una lista para almacenar los datos de los productos
    productos_data = []
    
    # Itera a través de la lista de productos en la respuesta
    for producto in peticion_listar_productos:
        producto_data = {
            'calibre': producto.calibre_idcalibre,
            'img': producto.img,
            'nombre_productor': producto.nombre_productor,
            'precio': producto.precio,
            'nombre_producto': producto.producto_idproducto,
            'rut_productor': producto.productor_rut,
            'stock': producto.stock   
        }
        productos_data.append(producto_data)
    
    # Convierte la lista de productos a una cadena JSON
    json_data = json.dumps(productos_data, indent=4)
    
    return json_data


