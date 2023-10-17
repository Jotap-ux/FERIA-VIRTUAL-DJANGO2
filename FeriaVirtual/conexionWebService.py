from django import forms
from django.shortcuts import render, redirect
#import zeep
from zeep import Client
import json



URL_WEBSERVICE = 'http://localhost:8080/WEBSERVICEFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'


def crear_productor(rut, dv, nombre, apellidopat, apellidomat, fechanacimiento, direccion, correoelectronico, contrasena, comuna_idcomuna):

    client = Client(URL_WEBSERVICE)

    response = client.service.agregarProductor(rut=rut, dv=dv, nombre=nombre, apellidopat=apellidopat, apellidomat=apellidomat,
                                               fechanacimiento=fechanacimiento, direccion=direccion, correoelectronico=correoelectronico,
                                               contrasena=contrasena, comuna_idcomuna=comuna_idcomuna)

    return response


def crear_clienteNormal(rut, dv, nombre, apellidopat, apellidomat, direccion, fechanacimiento, correoelectronico, contrasena, comuna_idcomuna):

    client = Client(URL_WEBSERVICE)

    response = client.service.agregarClienteNormal(rut=rut, dv=dv, nombre=nombre, apellidopat=apellidopat, apellidomat=apellidomat,
                                                   direccion=direccion, fechanacimiento=fechanacimiento, correoelectronico=correoelectronico,
                                                   contrasena=contrasena, comuna_idcomuna=comuna_idcomuna)

    return response

#client = zeep.Client(URL_WEBSERVICE)