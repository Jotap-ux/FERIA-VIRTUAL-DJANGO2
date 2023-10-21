from django.contrib import admin
from django.urls import path, include
from .views import index, productos, nosotros, contacto, inicio_sesion, carrito, regis_clien_em, regis_clien_per, regis_prod, regis_transp, regis_transp2, perfil_cli_datos, perfil_cli_domici, perfil_cli_pedi, perfil_pro_datos, perfil_pro_domici,perfil_pro_envios,perfil_pro_pedi, perfil_pro_productos, perfil_transp_datos, perfil_transp_domici, perfil_transp_pedi, perfil_transp_transpor, perfil_transp_vehi, subasta, detalle_producto, cerrar_sesion

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
    path('perfil_pro_datos', perfil_pro_datos, name='PROD_DATOS'),
    path('perfil_pro_domici', perfil_pro_domici, name='PROD_DOMICI'),
    path('perfil_pro_envios', perfil_pro_envios, name='PROD_ENVIOS'),
    path('perfil_pro_pedi', perfil_pro_pedi, name='PROD_PEDI'),
    path('perfil_pro_productos', perfil_pro_productos, name='PROD_PRODUC'),
    path('perfil_transp_datos', perfil_transp_datos, name='TRANSP_DATOS'),
    path('perfil_transp_domici', perfil_transp_domici, name='TRANSP_DOMICI'),
    path('perfil_transp_pedi', perfil_transp_pedi, name='TRANSP_PEDI'),
    path('perfil_transp_transpor', perfil_transp_transpor, name='TRANSP_TRANSPOR'),
    path('perfil_transp_vehi', perfil_transp_vehi, name='TRANSP_VEHI'),
    path('subasta', subasta, name='SUBASTAS'),
    path('detalle_producto', detalle_producto, name='DETALLE_PRODUCTO'),
    path('cerrar_sesion/', cerrar_sesion, name='CERRAR_SESION'),


]
