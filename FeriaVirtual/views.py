from django import forms
from django.shortcuts import render, redirect
from .conexionWebService import crear_productor, crear_clienteNormal, crear_clienteEmpresa, obtener_productos_json, autenticar_usuario
#from .probandoapi import obtener_productos_json
#from .login import autenticar_usuario
from.models import Productor, Cliente
#from .models import Producto
from django.http import HttpResponse
import xml.etree.ElementTree as ET
import json
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
#from django.contrib.auth.decorators import login_required

# lista
def index(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})


    return render(request, "core/index.html", {'usuario_autenticado': usuario_autenticado, 'user_info': user_info})
    #return render(request, "core/index.html")

#para poder listar los PRODUCTOS 
def productos(request):
    
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    # Llama a la función para obtener la lista de productos en formato JSON
    json_data = obtener_productos_json()

    # Parsea la cadena JSON a una lista de diccionarios
    lista_de_productos = json.loads(json_data)


    return render(request, "core/Productos.html", {"productos": lista_de_productos, 'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def nosotros(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Nosotros.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def contacto(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Formulario_contacto.html", {'usuario_autenticado': usuario_autenticado, 'user_info': user_info} )

# lista
#def inicio_sesion(request):
    #return render(request, "core/Inicio_de_sesión.html")

def inicio_sesion(request):
    if request.method == 'POST':
        correoelectronico = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        resultado_json = autenticar_usuario(correoelectronico, contrasena)

        # Parsea el resultado JSON
        resultado_dict = json.loads(resultado_json)
        tipo_usuario = resultado_dict.get('Tipo_usuario')
        rut_usuario = resultado_dict.get('Rut_usuario')

        if tipo_usuario == 'PRODUCTOR':
            try:
                # Busca el objeto Productor en la base de datos utilizando el campo 'rut'
                productor = Productor.objects.get(rut=rut_usuario)

                # Concatena nombre y apellido y agrega el valor resultante a user_info
                nombre_completo = f"{productor.nombre} {productor.apellidopat} {productor.apellidomat}"

                rut_completo = f"{rut_usuario}-{productor.dv}"

                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'NombreCompleto': nombre_completo,
                    'Rut_completo': rut_completo
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/Perfil_productor_datos.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})

            except Productor.DoesNotExist:

                error_message = 'El usuario no existe. Por favor, verifica tus credenciales.'
                return HttpResponse(error_message)

                # Aquí puedes manejar el caso en el que no se encuentre un Productor con el 'Rut_usuario' proporcionado
                return render(request, "core/Inicio_de_sesión.html", {'resultado_json': resultado_json})
            
        elif tipo_usuario == 'CLIENTENORMAL':
            try:
                # Busca el objeto Productor en la base de datos utilizando el campo 'rut'
                cliente = Cliente.objects.get(rut=rut_usuario)

                # Concatena nombre y apellido y agrega el valor resultante a user_info
                nombre_completo = f"{cliente.nombre} {cliente.apellidopat} {cliente.apellidomat}"

                rut_completo = f"{rut_usuario}-{cliente.dv}"

                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'NombreCompleto': nombre_completo,
                    'Rut_completo': rut_completo
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/Perfil_cliente_datos.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})
            except Productor.DoesNotExist:

                error_message = 'El usuario no existe. Por favor, verifica tus credenciales.'
                return HttpResponse(error_message)
        
        elif tipo_usuario == 'CLIENTEEMP':
            try:
                # Busca el objeto Productor en la base de datos utilizando el campo 'rut'
                cliente = Cliente.objects.get(identificadorempresa=rut_usuario)

                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'RazonSocial': cliente.razonsocial
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/Perfil_cliente_datos.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})
            except Productor.DoesNotExist:

                error_message = 'El usuario no existe. Por favor, verifica tus credenciales.'
                return HttpResponse(error_message)
        else:
            # Aquí puedes manejar otros tipos de usuarios o redirigir a páginas diferentes
            return render(request, "core/Inicio_de_sesión.html", {'resultado_json': resultado_json})

    return render(request, "core/Inicio_de_sesión.html")

@never_cache
def cerrar_sesion(request):
    if 'user_info' in request.session:
        del request.session['user_info']  # Elimina la información de usuario
    # Cierra la sesión del usuario
    logout(request)
    return redirect('INDEX')  # Redirige a la página de inicio o a donde desees

#--------------------------------------------------------------------
# lista
def carrito(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})
    return render(request, "core/Carrito.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info} )

# Formulario registro CLIENTE EMPRESA - USA LA API
def regis_clien_em(request):
    if request.method == 'POST':        
        direccion = request.POST.get('direccion')
        #fechanacimiento = request.POST.get('fechanacimiento')        
        correoelectronico = request.POST.get('correoelectronico')
        contrasena = request.POST.get('contrasena')
        identificadorempresa = request.POST.get('identificadorempresa')
        razonsocial = request.POST.get('razonsocial')
        comuna_idcomuna = request.POST.get('comuna_idcomuna')
        
        response = crear_clienteEmpresa(            
            direccion,
            #fechanacimiento,            
            correoelectronico,
            contrasena,
            identificadorempresa,
            razonsocial,
            comuna_idcomuna
        )
         # Procesa la respuesta del servicio SOAP, si es necesario

        if response == 'OK':
            return redirect('REGIS_EMPRESA')
        else:
            #return HttpResponse('Hello World')
            return redirect('REGIS_EMPRESA')
    else:
        return render(request, "core/Registro_cliente_empresa.html")

# Formulario registro CLIENTE PERSONA - USA LA API
def regis_clien_per(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        dv = request.POST.get('dv')
        nombre = request.POST.get('nombre')
        apellidopat = request.POST.get('apellidopat')
        apellidomat = request.POST.get('apellidomat')
        direccion = request.POST.get('direccion')
        fechanacimiento = request.POST.get('fechanacimiento')        
        correoelectronico = request.POST.get('correoelectronico')
        contrasena = request.POST.get('contrasena')
        comuna_idcomuna = request.POST.get('comuna_idcomuna')
        
        response = crear_clienteNormal(
            rut,
            dv,
            nombre,
            apellidopat,
            apellidomat,
            direccion,
            fechanacimiento,            
            correoelectronico,
            contrasena,
            comuna_idcomuna
        )
         # Procesa la respuesta del servicio SOAP, si es necesario

        if response == 'OK':
            return redirect('REGIS_PERSONA')
        else:
            #return HttpResponse('Hello World')
            return redirect('REGIS_PERSONA')
    else:
        return render(request, "core/Registro_cliente_persona.html")

# Formulario registro PRODUCTOR - USA LA API
def regis_prod(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')
        dv = request.POST.get('dv')
        nombre = request.POST.get('nombre')
        apellidopat = request.POST.get('apellidopat')
        apellidomat = request.POST.get('apellidomat')
        fechanacimiento = request.POST.get('fechanacimiento')
        direccion = request.POST.get('direccion')
        correoelectronico = request.POST.get('correoelectronico')
        contrasena = request.POST.get('contrasena')
        comuna_idcomuna = request.POST.get('comuna_idcomuna')

        response = crear_productor(
            rut,
            dv,
            nombre,
            apellidopat,
            apellidomat,
            fechanacimiento,
            direccion,
            correoelectronico,
            contrasena,
            comuna_idcomuna
        )

        # Procesa la respuesta del servicio SOAP, si es necesario

        if response == 'OK':
            return redirect('REGIS_PROD')
        else:
            #return HttpResponse('Hello World')
            return redirect('REGIS_PROD')
    else:
        # Cualquier otro código que necesites para la vista si no se envió un formulario POST
        return render(request, 'core/Registro_productor.html')
    

#Mi archivo conexionWebService.py contiene la lógica para el servicio web SOAP,
# y el archivo views.py se encarga de manejar el formulario y llamar a la función correspondiente 
# desde el archivo conexionWebService.py. 
#------------------------------------------------------------------


# lista
def regis_transp(request):
    return render(request, "core/Registro_transportista.html")

# lista
def regis_transp2(request):
    return render(request, "core/Registro_transportista2.html")

#-----------------------------------------------------------------------------------------------!!
#PERFILES DE CADA USUARIO
#CLIENTE

# lista
def perfil_cli_datos(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_cliente_datos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_cli_domici(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_cliente_domicilio.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_cli_pedi(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_cliente_pedidos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

#PRODUCTOR-------------------------------------------------------------------------------------
# lista
def perfil_pro_datos(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_productor_datos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_pro_domici(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_productor_domicilio.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_pro_envios(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_productor_envios.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_pro_pedi(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_productor_pedidos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_pro_productos(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_productor_productos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

#TRANSPORTISTA
# lista
def perfil_transp_datos(request):
    return render(request, "core/Perfil_transportista_datos.html")

# lista
def perfil_transp_domici(request):
    return render(request, "core/Perfil_transportista_domicilio.html")

# lista
def perfil_transp_pedi(request):
    return render(request, "core/Perfil_transportista_pedidos.html")

# lista
def perfil_transp_transpor(request):
    return render(request, "core/Perfil_transportista_transportes.html")

# lista
def perfil_transp_vehi(request):
    return render(request, "core/Perfil_transportista_vehiculos.html")

#subasta---
def subasta(request):
    return render(request, "core/Subastas.html")

#DETALLE DEL PRODUCTO
def detalle_producto(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})
    return render(request, "core/Producto_detalle.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})