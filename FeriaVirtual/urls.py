from django.contrib import admin
from django.urls import path, include
from .views import index, productos, nosotros, contacto, inicio_sesion, carrito, regis_clien_em, regis_clien_per, regis_prod, regis_transp, regis_transp2, perfil_cli_datos, perfil_cli_domici, perfil_cli_pedi

urlpatterns = [
    path('',index, name='INDEX'),
    path('productos/', productos, name='PRODUCTOS'),
    path('nosotros/', nosotros, name='NOSOTROS'),
    path('contacto/', contacto, name='CONTACTO'),
    path('inicio_sesion/', inicio_sesion, name='INICIO_SESION'),
    path('carrito/', carrito, name='CARRITO'),
    path('regis_clien_em', regis_clien_em, name='REGIS_EMPRESA'),
    path('regis_clien_per', regis_clien_per, name='REGIS_PERSONA'),
    path('regis_prod', regis_prod, name='REGIS_PROD'),
    path('regis_transp', regis_transp, name='REGIS_TRANSP'),
    path('regis_transp2', regis_transp2, name='REGIS_TRANSP2'),
    path('perfil_cli_datos', perfil_cli_datos, name='CLIENTE_DATOS'),
    path('perfil_cli_domici', perfil_cli_domici, name='CLIENTE_DOMICI'),
    path('perfil_cli_pedi', perfil_cli_pedi, name='CLIENTE_PEDI'),
]
