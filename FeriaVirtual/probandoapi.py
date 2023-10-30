from django import forms
from django.shortcuts import render, redirect
from zeep import Client
import json

URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'

client = Client(URL_WEBSERVICE)

peticion_productos_productor = client.service.listarproductosporrutproductor(20279147)

# Inicializa una lista para almacenar los datos de los productos
productos_data = []

 # Itera a través de la lista de productos en la respuesta
for producto in peticion_productos_productor:
    producto_data = {
        'calibre': producto.calibre_idcalibre,
        'img': producto.img,
        'precio': producto.precio,
        'nombre_producto' : producto.producto_idproducto,                 
        'stock': producto.stock   
    }
    productos_data.append(producto_data)

# Convierte la lista de productos a una cadena JSON
json_data = json.dumps(productos_data, indent=4)

print(json_data)
#return json_data