from django import forms
from django.shortcuts import render, redirect
#import zeep
from zeep import Client
import json



URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'



def agregar_productos(precio, stock, calibre_idcalibre, producto_idproducto, productor_rut, img):

    client = Client(URL_WEBSERVICE)

    response = client.service.agregarNuevoProducto(precio=precio, stock=stock, calibre_idcalibre=calibre_idcalibre,
                                                   producto_idproducto=producto_idproducto, productor_rut=productor_rut, img=img)

    return response    