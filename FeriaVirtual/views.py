from django import forms
from django.shortcuts import render, redirect
from .conexionWebService import crear_productor, crear_clienteNormal, crear_clienteEmpresa, crear_transportista ,obtener_productos_json, autenticar_usuario, agregar_productos, listar_calibres, listar_productos_combobox, crearPedido, crearDetalle_pedido
#from .Apiproductos import agregar_productos
from.models import Productor, Cliente, Transportista
#from .models import Producto
from django.http import HttpResponse, JsonResponse
from django.http import JsonResponse, HttpResponseRedirect
import xml.etree.ElementTree as ET
import json
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
#from django.contrib.auth.decorators import login_required
from .decorators import user_info_required
from django.utils import formats
#from .probandoapi import listar_calibres, listar_productos_combobox
from urllib.parse import unquote
import re
from django.views.decorators.csrf import csrf_exempt
import json



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

                 # veriricando contraseña, aunque no funciona f
                if productor.contrasena != contrasena:
                    response = HttpResponse("Error, contraseña incorrecta!")
                    return response
                
                # Concatena nombre y apellido y agrega el valor resultante a user_info
                nombre_completo = f"{productor.nombre} {productor.apellidopat} {productor.apellidomat}"

                rut_completo = f"{rut_usuario}-{productor.dv}"
                
                #nombre = {productor.nombre}
                #apellido = {productor.apellidopat}
                # Obtiene la fecha de nacimiento del modelo Productor
                #fecha_nacimiento = productor.fechanacimiento.strftime("%Y-%m-%d")

                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'NombreCompleto': nombre_completo,
                    'Rut_completo': rut_completo,
                    'Fecha_nacimiento': productor.fechanacimiento.strftime("%d-%m-%Y"),
                    'Nombre': productor.nombre,
                    'Apellido': productor.apellidopat,
                    'Direccion': productor.direccion
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/Perfil_productor_datos.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})

            except Productor.DoesNotExist:

                response = HttpResponse("USUARIO NO EXISTE")
                return response

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
                    'Rut_completo': rut_completo,
                    'Fecha_nacimiento': cliente.fechanacimiento.strftime("%d-%m-%Y"),
                    'Nombre': cliente.nombre,
                    'Apellido': cliente.apellidopat,
                    'Direccion': cliente.direccion,
                    'id_cliente': cliente.id_cliente
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/Perfil_cliente_datos.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})
            except Productor.DoesNotExist:

                response = HttpResponse("USUARIO NO EXISTE")
                return response
        
        elif tipo_usuario == 'CLIENTEEMP':
            try:
                # Busca el objeto Productor en la base de datos utilizando el campo 'rut'
                cliente = Cliente.objects.get(identificadorempresa=rut_usuario)

                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'RazonSocial': cliente.razonsocial,
                    'Direccion': cliente.direccion,
                    'id_cliente': cliente.id_cliente
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/Perfil_cliente_datos.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})
            except Productor.DoesNotExist:

                response = HttpResponse("USUARIO NO EXISTE")
                return response
        
        elif tipo_usuario == 'TRANSPORTISTA':
            try:
                # Busca el objeto Productor en la base de datos utilizando el campo 'rut'
                transportista = Transportista.objects.get(rut=rut_usuario)

                 # Concatena nombre y apellido y agrega el valor resultante a user_info
                nombre_completo = f"{transportista.nombre} {transportista.apellidopat} {transportista.apellidomat}"

                rut_completo = f"{rut_usuario}-{transportista.dv}"

                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'NombreCompleto': nombre_completo,
                    'Rut_completo': rut_completo,
                    'Fecha_nacimiento': transportista.fechanacimiento.strftime("%d-%m-%Y"),
                    'Nombre': transportista.nombre,
                    'Apellido': transportista.apellidopat,
                    'Direccion': transportista.direccion
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/Perfil_transportista_datos.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})
            except Productor.DoesNotExist:

                response = HttpResponse("USUARIO NO EXISTE")
                return response
        
        else:
            response = HttpResponse("El usuario no existe!")
            return response
            # Aquí puedes manejar otros tipos de usuarios o redirigir a páginas diferentes
            #return render(request, "core/Inicio_de_sesión.html", {'resultado_json': resultado_json})

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
  # Esto es necesario si estás enviando datos desde un sitio web (para deshabilitar CSRF)

def carrito(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    if request.method == 'POST':
        # Verificar el encabezado Content-Type
        if request.content_type == 'application/json':
            try:
                # Recibe los datos del carrito enviados desde el cliente
                carrito_data = json.loads(request.body)

                # Obtén el id_cliente del usuario con sesión iniciada
                id_cliente = user_info.get('id_cliente', None)

                if id_cliente is not None:
                    # Llama a la función que crea un pedido pasando id_cliente como parámetro
                    response_pedido = crearPedido(id_cliente)

                    #para ver si me trae el id_pedido
                    print(response_pedido)

                    if response_pedido == 'OK':
                        print('Hola sangre')
                    else:

                        # El pedido se creó con éxito, ahora agreguemos detalles
                        for producto in carrito_data:
                            cantidad = producto['cantidad']
                            print('cantidad:', cantidad)
                            id_producto = producto['id_producto']
                            print('id_producto:', id_producto)
                            productor_rut = producto['rut_productor']
                            print('productor_rut:', productor_rut)
                            pedido_idpedido = response_pedido  # El ID del pedido que se creó anteriormente
                            print('id_pedido:',pedido_idpedido)
                            calibre_idcalibre = producto['calibreId']
                            print('calibre id:', calibre_idcalibre)

                            # Llama a la función que crea un detalle de pedido
                            response_detalle = crearDetalle_pedido(cantidad, id_producto, productor_rut, pedido_idpedido, calibre_idcalibre)

                            # Puedes manejar la respuesta del detalle aquí, por ejemplo, verificar si se creó con éxito

                        # Redirige al usuario a la página deseada después de procesar el carrito
                        return HttpResponseRedirect('/productos/')  # Reemplaza la URL de redirección según tus necesidades                       

                return redirect('PRODUCTOS') 
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Error al decodificar JSON'}, status=400)

    return render(request, "core/Carrito.html", {'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

#-----------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
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


# Formulario registro TRANSPORTISTA - USA LA API
def regis_transp(request):
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
        #comuna_idcomuna = request.POST.get('comuna_idcomuna')
        
        response = crear_transportista(
            rut,
            dv,
            nombre,
            apellidopat,
            apellidomat,
            fechanacimiento,
            direccion,                        
            correoelectronico,
            contrasena,
            #comuna_idcomuna
        )
         # Procesa la respuesta del servicio SOAP, si es necesario

        if response == 'OK':
            return redirect('REGIS_TRANSP')
        else:
            #return HttpResponse('Hello World')
            return redirect('REGIS_TRANSP')
    else:
        
        return render(request, "core/Registro_transportista.html")

# lista
def regis_transp2(request):
    return render(request, "core/Registro_transportista2.html")

#-----------------------------------------------------------------------------------------------!!
#PERFILES DE CADA USUARIO
#CLIENTE

# lista
@user_info_required
def perfil_cli_datos(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_cliente_datos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
@user_info_required
def perfil_cli_domici(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_cliente_domicilio.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
@user_info_required
def perfil_cli_pedi(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_cliente_pedidos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

#PRODUCTOR-------------------------------------------------------------------------------------
# lista
@user_info_required
def perfil_pro_datos(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_productor_datos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
@user_info_required
def perfil_pro_domici(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_productor_domicilio.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
@user_info_required
def perfil_pro_envios(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_productor_envios.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
@user_info_required
def perfil_pro_pedi(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_productor_pedidos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
@user_info_required
def perfil_pro_productos(request):

    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    # Obtener los datos de los calibres utilizando la función de la API
    calibres_json = listar_calibres()

    # Parsea la cadena JSON a una lista de diccionarios
    calibres_data = json.loads(calibres_json)

    # Obtener los datos de los productos utilizando la función de la API
    productos_json = listar_productos_combobox()

    # Parsea la cadena JSON a una lista de diccionarios
    productos_data = json.loads(productos_json)

    

    if request.method == 'POST':        
        precio = request.POST.get('precio')     
        stock = request.POST.get('stock')
        calibre_idcalibre = request.POST.get('calibre_idcalibre')
        producto_idproducto = request.POST.get('producto_idproducto')
        productor_rut = user_info['Rut_usuario']
        img = request.POST.get('img')
        
        response = agregar_productos(            
           precio,
           stock,
           calibre_idcalibre,
           producto_idproducto,
           productor_rut,
           img
        )
         # Procesa la respuesta del servicio SOAP, si es necesario

        if response == 'OK':
            return redirect('PROD_PRODUC')
        else:
            #return HttpResponse('Hello World')
            return redirect('PROD_PRODUC')
    else:
        return render(request, "core/Perfil_productor_productos.html",{
            'usuario_autenticado': usuario_autenticado, 
            'user_info': user_info,
            'calibres':calibres_data,
            'productos': productos_data})
    
    #return render(request, "core/Perfil_productor_productos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

#TRANSPORTISTA
# lista
def perfil_transp_datos(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_transportista_datos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_transp_domici(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_transportista_domicilio.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_transp_pedi(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_transportista_pedidos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_transp_transpor(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_transportista_transportes.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_transp_vehi(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_transportista_vehiculos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

#subasta---
def subasta(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})
    
    return render(request, "core/Subastas.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

#DETALLE DEL PRODUCTO
def detalle_producto(request, rut_productor, nombre_producto, calibre):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})


    nombre_producto = unquote(nombre_producto)
    calibre = unquote(calibre)

    # Elimina espacios en blanco alrededor del nombre del producto
    nombre_producto = nombre_producto.strip()

    # Elimina espacios en blanco alrededor del calibre 
    calibre = calibre.strip()

    # Agregar impresiones para depuración
    #print("Rut de productor :", rut_productor)
    #print("Nombre de producto :", nombre_producto)
    #print("El calibre :", calibre)

    json_data = obtener_productos_json()
    lista_de_productos = json.loads(json_data)

    rut_productor = int(rut_productor)

    #print(lista_de_productos)
    # Buscar el producto por nombre
    producto_seleccionado = None
    for producto in lista_de_productos:

        if (
            producto['rut_productor'] == rut_productor
            and producto['nombre_producto'].strip().lower() == nombre_producto.lower()
            and producto['calibre'].strip().lower() == calibre.lower()
                        
        ):
            print(producto)
            producto_seleccionado = producto
           
            break
           
    return render(request, "core/Producto_detalle.html",{'usuario_autenticado': usuario_autenticado,
                                                        'user_info': user_info,
                                                        'producto': producto_seleccionado})





