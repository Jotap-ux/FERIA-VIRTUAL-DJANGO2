from django import forms
from django.shortcuts import render, redirect
from .conexionWebService import crear_productor, crear_clienteNormal, crear_clienteEmpresa, crear_transportista ,obtener_productos_json, autenticar_usuario, agregar_productos, listar_calibres, listar_productos_combobox, crearPedido, crearDetalle_pedido, obtener_subastas_json
from .conexionWebService import listar_pais_combobox, listar_region_por_pais, listar_comuna_por_region, listarProductos_Productor, crearOfertaSubasta, listarMontoSubasta, listarPedidos_cliente, crearTransporte
from .conexionWebService import listar_marca_combobox, listar_modelo_por_marca, listar_vehiculos_transportista, crearPago, listar_pedidosTransportista
from .conexionWebService import actualizar_pedido_Enviado, actualizar_pedido_Recibido, listar_pedidosTransportista_Finalizados, actualizar_pedido_recha_cliente, actualizar_pedido_recha_transportista
from .conexionWebService import actualizar_IMGinicio, actualizar_IMGfinal, actualizarDireccionDespacho
from .conexionWebService import desactivarCuentaClienteNormal, desactivarCuentaClienteEmpresa, desactivarCuentaProductor, desactivarCuentaTransportista
from .conexionWebService import actualizar_productos, actualizar_clienteNORMAL, actualizar_clienteEMPRESA, actualizar_productor, actualizar_transportista
from .conexionWebService import eliminarVEHICULO
from.models import Productor, Cliente, Transportista, OfertarSubasta, Transporte, Comuna, Region, Pais, Direccion
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
from django.db.models import Min
# SDK de Mercado Pago
import mercadopago
# Importa el módulo urljoin para construir URLs absolutas
from urllib.parse import urljoin
import requests
from django.db.models import Max
from rut_chile import rut_chile

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
    #--------------------------------------------------//////////////
    # Obtener el término de búsqueda de la URL (PARA PRODUCTOS)
    search_term = request.GET.get('q', '')

    #----------------------------------------------------////////////////
    # Llama a la función para obtener la lista de productos en formato JSON
    json_data = obtener_productos_json()

    # Parsea la cadena JSON a una lista de diccionarios
    lista_de_productos = json.loads(json_data)

    #----------------------------------------------------////////////
    # Filtra los productos según el término de búsqueda
    if search_term:
        lista_de_productos = [producto for producto in lista_de_productos if search_term.lower() in producto['nombre_producto'].lower()]

    #-----------------------------------------------------///////////
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
                
                #---------------OBTENER COMUNA, REGION Y PAIS----------------------------------

                # Obtén el id de la comuna como cadena
                id_comuna_str = str(productor.comuna_idcomuna_id)  # Accede directamente al ID

                #buscamos el nombre de la COMUNA de acuerdo a ese id...
                comuna = Comuna.objects.get(idcomuna = id_comuna_str)

                nombre_comuna = comuna.nombrecomuna
                
                # Obtén el id de la region como cadena
                id_region_str = str(comuna.region_idregion_id)

                #buscamos el nombre de la REGION de acuerdo a ese id...
                region = Region.objects.get(idregion = id_region_str)

                nombre_region = region.nombreregion

                # Obtén el id del pais como cadena
                id_pais_str = str(region.pais_idpais_id)

                #buscamos el nombre de la PAIS de acuerdo a ese id...
                pais = Pais.objects.get(idpais = id_pais_str)

                nombre_pais = pais.nombrepais                
                #--------------------------------------------------------
                print('Su comuna es : ', id_comuna_str, 'y el nombre es:', nombre_comuna, 'su region : ', id_region_str, 'Su pais : ', id_pais_str)

                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'NombreCompleto': nombre_completo,
                    'Rut_completo': rut_completo,
                    'Fecha_nacimiento': productor.fechanacimiento.strftime("%d-%m-%Y"),
                    'Nombre': productor.nombre,
                    'Apellido': productor.apellidopat,
                    'ApellidoMATERNO': productor.apellidomat,
                    'Direccion': productor.direccion,
                    'comuna_id': id_comuna_str,  # Convertimos el id de la comuna a cadena
                    'comuna' : nombre_comuna,
                    'region': nombre_region,
                    'pais' : nombre_pais
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/index.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})

            except Productor.DoesNotExist:

                response = HttpResponse("CREDENCIALES INCORRECTAS!")
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
                
                #---------------OBTENER COMUNA, REGION Y PAIS----------------------------------

                # Obtén el id de la comuna como cadena
                id_comuna_str = str(cliente.comuna_idcomuna_id)  # Accede directamente al ID

                #buscamos el nombre de la COMUNA de acuerdo a ese id...
                comuna = Comuna.objects.get(idcomuna = id_comuna_str)

                nombre_comuna = comuna.nombrecomuna
                
                # Obtén el id de la region como cadena
                id_region_str = str(comuna.region_idregion_id)

                #buscamos el nombre de la REGION de acuerdo a ese id...
                region = Region.objects.get(idregion = id_region_str)

                nombre_region = region.nombreregion

                # Obtén el id del pais como cadena
                id_pais_str = str(region.pais_idpais_id)

                #buscamos el nombre de la PAIS de acuerdo a ese id...
                pais = Pais.objects.get(idpais = id_pais_str)

                nombre_pais = pais.nombrepais                
                #--------------------------------------------------------
                print('Su comuna es : ', id_comuna_str, 'y el nombre es:', nombre_comuna, 'su region : ', id_region_str, 'Su pais : ', id_pais_str)
                #-----------------OBTENER DIRECCION DE ENTREGA (PEDIDO)------------------
                #buscamos el la direccion registrada con ese id...
                direccion = Direccion.objects.get(cliente_id_cliente = cliente.id_cliente)
                
                nombre_direccion = direccion.direccion_nueva
                print(nombre_direccion)

                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'NombreCompleto': nombre_completo,
                    'Rut_completo': rut_completo,
                    'Fecha_nacimiento': cliente.fechanacimiento.strftime("%d-%m-%Y"),
                    'Nombre': cliente.nombre,
                    'Apellido': cliente.apellidopat,
                    'ApellidoMATERNO': cliente.apellidomat, 
                    'Direccion': cliente.direccion,  
                    'id_cliente': cliente.id_cliente,                
                    'comuna_id': id_comuna_str,  # Convertimos el id de la comuna a cadena
                    'comuna' : nombre_comuna,
                    'region': nombre_region,
                    'pais' : nombre_pais,
                    'direccion_entrega' : nombre_direccion
                    #'estado_activo': cliente.estadoactivo #---para ver si tiene la cuenta ok
                }

                print('Su id de cliente es : ', cliente.id_cliente)

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/index.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})
            except Productor.DoesNotExist:

                response = HttpResponse("USUARIO NO EXISTE")
                return response
        
        elif tipo_usuario == 'CLIENTEEMP':
            try:
                # Busca el objeto Productor en la base de datos utilizando el campo 'rut'
                cliente = Cliente.objects.get(identificadorempresa=rut_usuario)

                #---------------OBTENER COMUNA, REGION Y PAIS----------------------------------

                # Obtén el id de la comuna como cadena
                id_comuna_str = str(cliente.comuna_idcomuna_id)  # Accede directamente al ID

                #buscamos el nombre de la COMUNA de acuerdo a ese id...
                comuna = Comuna.objects.get(idcomuna = id_comuna_str)

                nombre_comuna = comuna.nombrecomuna
                
                # Obtén el id de la region como cadena
                id_region_str = str(comuna.region_idregion_id)

                #buscamos el nombre de la REGION de acuerdo a ese id...
                region = Region.objects.get(idregion = id_region_str)

                nombre_region = region.nombreregion

                # Obtén el id del pais como cadena
                id_pais_str = str(region.pais_idpais_id)

                #buscamos el nombre de la PAIS de acuerdo a ese id...
                pais = Pais.objects.get(idpais = id_pais_str)

                nombre_pais = pais.nombrepais                
                #--------------------------------------------------------
                print('Su comuna es : ', id_comuna_str, 'y el nombre es:', nombre_comuna, 'su region : ', id_region_str, 'Su pais : ', id_pais_str)


                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'RazonSocial': cliente.razonsocial,
                    'Direccion': cliente.direccion,
                    'id_cliente': cliente.id_cliente,
                    'comuna_id': id_comuna_str,  # Convertimos el id de la comuna a cadena
                    'comuna' : nombre_comuna,
                    'region': nombre_region,
                    'pais' : nombre_pais
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/index.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})
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

                #---------------OBTENER COMUNA, REGION Y PAIS----------------------------------

                              
                #--------------------------------------------------------
                
                request.session['user_info'] = {
                    'username': correoelectronico,
                    'tipo_usuario': tipo_usuario,
                    'Rut_usuario': rut_usuario,
                    'NombreCompleto': nombre_completo,
                    'Rut_completo': rut_completo,
                    'Fecha_nacimiento': transportista.fechanacimiento.strftime("%d-%m-%Y"),
                    'Nombre': transportista.nombre,
                    'Apellido': transportista.apellidopat,
                    'ApellidoMATERNO': transportista.apellidomat,
                    'Direccion': transportista.direccion,
                    #'comuna_id': id_comuna_str,  # Convertimos el id de la comuna a cadena
                    #'comuna' : nombre_comuna,
                    #'region': nombre_region,
                    #'pais' : nombre_pais
                }

                request.session['usuario_autenticado'] = True  # Indica que el usuario ha iniciado sesión

                # Redirige a la página de perfil del productor
                return render(request, 'core/index.html', {'user_info': request.session['user_info'], 'resultado_json': resultado_json})
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
    messages.success(request, 'La sesión se ha cerrado :( ')
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

    # Obtener los datos de los productos utilizando la función de la API
    paises_json = listar_pais_combobox()

    # Parsea la cadena JSON a una lista de diccionarios
    paises_data = json.loads(paises_json)    

    if request.method == 'POST':        

        #---------------------------
        rut = request.POST.get('identificadorempresa')
        dv_empresa = request.POST.get('dv_empresa')

        # Concatena rut y dv con '-'
        identificadorempresa = f"{rut}-{dv_empresa}"

        print(identificadorempresa)

        print(rut_chile.is_valid_rut(identificadorempresa)) 
        #--------------------------------------------
        # Valida el rut utilizando la biblioteca rut_chile
        if rut_chile.is_valid_rut(identificadorempresa) == True:

            direccion = request.POST.get('direccion')
            #fechanacimiento = request.POST.get('fechanacimiento')        
            correoelectronico = request.POST.get('correoelectronico')
            contrasena = request.POST.get('contrasena')        
            razonsocial = request.POST.get('razonsocial')
            comuna_idcomuna = request.POST.get('comuna')
                    
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
                messages.success(request, 'Usted se ha registrado exitosamente :) ')
                return redirect('REGIS_EMPRESA')
        else:
            response = HttpResponse("Ingrese un rut válido!")
            return response
    else:
        return render(request, "core/Registro_cliente_empresa.html",
                      {'paises': paises_data})

# Formulario registro CLIENTE PERSONA - USA LA API
def regis_clien_per(request):

    # Obtener los datos de los productos utilizando la función de la API
    paises_json = listar_pais_combobox()

    # Parsea la cadena JSON a una lista de diccionarios
    paises_data = json.loads(paises_json)    

    if request.method == 'POST':
        rut = request.POST.get('rut')
        dv = request.POST.get('dv')

        # Concatena rut y dv con '-'
        rut_completo = f"{rut}-{dv}"

        print(rut_completo)

        print(rut_chile.is_valid_rut(rut_completo)) 

        # Valida el rut utilizando la biblioteca rut_chile
        if rut_chile.is_valid_rut(rut_completo) == True:

            
            # Continúa con el resto del código
            nombre = request.POST.get('nombre')
            apellidopat = request.POST.get('apellidopat')
            apellidomat = request.POST.get('apellidomat')
            direccion = request.POST.get('direccion')
            fechanacimiento = request.POST.get('fechanacimiento')        
            correoelectronico = request.POST.get('correoelectronico')
            contrasena = request.POST.get('contrasena')
            comuna_idcomuna = request.POST.get('comuna')

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

            if response == 'OK':
                return redirect('REGIS_PERSONA')
            else:
                messages.success(request, 'Usted se ha registrado exitosamente :) ')
                return redirect('REGIS_PERSONA')
        else:
            response = HttpResponse("Ingrese un rut válido!")
            return response
    else:
        return render(request, "core/Registro_cliente_persona.html", {'paises': paises_data})

# Formulario registro PRODUCTOR - USA LA API
def regis_prod(request):

    # Obtener los datos de los productos utilizando la función de la API
    paises_json = listar_pais_combobox()

    # Parsea la cadena JSON a una lista de diccionarios
    paises_data = json.loads(paises_json) 


    if request.method == 'POST':

        #---------------------------
        rut = request.POST.get('rut')
        dv = request.POST.get('dv')

        # Concatena rut y dv con '-'
        rut_completo = f"{rut}-{dv}"

        print(rut_completo)

        print(rut_chile.is_valid_rut(rut_completo)) 
        #--------------------------------------------
        # Valida el rut utilizando la biblioteca rut_chile
        if rut_chile.is_valid_rut(rut_completo) == True:
            
            nombre = request.POST.get('nombre')
            apellidopat = request.POST.get('apellidopat')
            apellidomat = request.POST.get('apellidomat')
            fechanacimiento = request.POST.get('fechanacimiento')
            direccion = request.POST.get('direccion')
            correoelectronico = request.POST.get('correoelectronico')
            contrasena = request.POST.get('contrasena')
            comuna_idcomuna = request.POST.get('comuna')

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
                messages.success(request, 'Usted se ha registrado exitosamente :) ')
                return redirect('REGIS_PROD')
        else:
            response = HttpResponse("Ingrese un rut válido!")
            return response
    else:
        # Cualquier otro código que necesites para la vista si no se envió un formulario POST
        return render(request, 'core/Registro_productor.html',
                      {'paises': paises_data})
    
#------------------------------------------------------------------


# Formulario registro TRANSPORTISTA - USA LA API
def regis_transp(request):

    # Obtener los datos de los productos utilizando la función de la API
    paises_json = listar_pais_combobox()

    # Parsea la cadena JSON a una lista de diccionarios
    paises_data = json.loads(paises_json) 

    if request.method == 'POST':

        #---------------------------
        rut = request.POST.get('rut')
        dv = request.POST.get('dv')

        # Concatena rut y dv con '-'
        rut_completo = f"{rut}-{dv}"

        print(rut_completo)

        print(rut_chile.is_valid_rut(rut_completo)) 
        #--------------------------------------------
        # Valida el rut utilizando la biblioteca rut_chile
        if rut_chile.is_valid_rut(rut_completo) == True:
            
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
                messages.success(request, 'La información se ha guardado exitosamente :) ')
                return redirect('REGIS_TRANSP')
        else:
            response = HttpResponse("Ingrese un rut válido!")
            return response
    else:
        
        return render(request, "core/Registro_transportista.html",
                      {'paises': paises_data})

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

    #------DESACTIVAR CUENTA------
    if request.method == 'POST':
        rut = request.POST.get('rut_usuario_Desactivar')        
        identificadorabuscar = request.POST.get('rut_usuario_Desactivar2') 
        #----
        
        rutabuscar = request.POST.get('rut_clientePERSONA')
        nombre = request.POST.get('nombre_clientePERSONA')
        apellidopat = request.POST.get('apellido_clientePERSONA')
        apellidomat = request.POST.get('apellidomat_clientePERSONA')
        fechanacimiento = request.POST.get('fecha_clientePERSONA')

        razonsocial = request.POST.get('razonsocial_EMP')
        identificadorabuscar = request.POST.get('rut_EMP')

        #---PARA CAMBIAR DATOS
        if 'modificar-CLIENTE' in request.POST:

            response = actualizar_clienteNORMAL(            
            rutabuscar,
            nombre,
            apellidopat,
            apellidomat,
            fechanacimiento
            )
            # Procesa la respuesta del servicio SOAP, si es necesario

            if response == 'OK':
                return redirect('CLIENTE_DATOS')
            else:
                #messages.success(request, 'Los productos fueron agregados exitosamente :) ')
                return redirect('CLIENTE_DATOS')
            
        #---PARA CAMBIAR DATOS
        if 'modificar-CLIENTE-EMP' in request.POST:

            response = actualizar_clienteEMPRESA(            
            identificadorabuscar,
            razonsocial         
            )
            # Procesa la respuesta del servicio SOAP, si es necesario

            if response == 'OK':
                return redirect('CLIENTE_DATOS')
            else:
                #messages.success(request, 'Los productos fueron agregados exitosamente :) ')
                return redirect('CLIENTE_DATOS')


        #-----------------------------------------------
        if rut:

            response = desactivarCuentaClienteNormal(rut)
        elif identificadorabuscar:
            response = desactivarCuentaClienteEmpresa(identificadorabuscar)

        if response == 'OK':
            return redirect('CERRAR_SESION')
        else:
            #messages.success(request, 'SU CUENTA SE HA DESACTIVADO!! ')
            return redirect('CERRAR_SESION')    

        
    else:
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

    #----------------------------seccion para listar los productos por productor----------------------------------------------

    id_cliente = user_info['id_cliente']

    print(id_cliente)
    lista_pedidos_cliente = listarPedidos_cliente(id_cliente)

    print(lista_pedidos_cliente)
    # Parsea la cadena JSON a una lista de diccionarios
    pedidos_cliente = json.loads(lista_pedidos_cliente)

    return render(request, "core/Perfil_cliente_pedidos.html",{'usuario_autenticado': usuario_autenticado,
                                                                'user_info': user_info,
                                                                'pedidos_cliente': pedidos_cliente})

#PRODUCTOR-------------------------------------------------------------------------------------
# lista
@user_info_required
def perfil_pro_datos(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    if request.method == 'POST':
        rut = request.POST.get('rut_usuario_DesactivarProd')  

        #----
        
        rutabuscar = request.POST.get('rut_productor')
        nombre = request.POST.get('nombre_productor')
        apellidopat = request.POST.get('apellido_productor')
        apellidomat = request.POST.get('apellidomat_productor')
        fechanacimiento = request.POST.get('fecha_productor')

        #---PARA CAMBIAR DATOS
        if 'modificar-PRODUCTOR' in request.POST:

            response = actualizar_productor(            
            rutabuscar,
            nombre,
            apellidopat,
            apellidomat,
            fechanacimiento
            )
            # Procesa la respuesta del servicio SOAP, si es necesario

            if response == 'OK':
                return redirect('PROD_DATOS')
            else:
                #messages.success(request, 'Los productos fueron agregados exitosamente :) ')
                return redirect('PROD_DATOS')

        if rut:
            response = desactivarCuentaProductor(rut)

        if response == 'OK':
            return redirect('CERRAR_SESION')
        else:
            #messages.success(request, 'SU CUENTA SE HA DESACTIVADO!! ')
            return redirect('CERRAR_SESION')

        
    else:
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

    #----------------------------seccion para listar los productos por productor----------------------------------------------

    rut_productor = user_info['Rut_usuario']

    lista_productos_productor = listarProductos_Productor(rut_productor)

    # Parsea la cadena JSON a una lista de diccionarios
    productos_productor = json.loads(lista_productos_productor)

    print(productos_productor)

    if request.method == 'POST':        
        precio = request.POST.get('precio')     
        stock = request.POST.get('stock')
        calibre_idcalibre = request.POST.get('calibre_idcalibre')
        producto_idproducto = request.POST.get('producto_idproducto')
        productor_rut = user_info['Rut_usuario']
        
        if 'agregar' in request.POST:
            response = agregar_productos(            
            precio,
            stock,
            calibre_idcalibre,
            producto_idproducto,
            productor_rut
            )
            # Procesa la respuesta del servicio SOAP, si es necesario

            if response == 'OK':
                return redirect('PROD_PRODUC')
            else:
                #messages.success(request, 'Los productos fueron agregados exitosamente :) ')
                return redirect('PROD_PRODUC')
            
        elif 'modificar' in request.POST:

            rutabuscar = productor_rut

            response = actualizar_productos(       
            rutabuscar,     
            precio,
            stock,
            calibre_idcalibre,
            producto_idproducto        
            )
            # Procesa la respuesta del servicio SOAP, si es necesario

            if response == 'OK':
                return redirect('PROD_PRODUC')
            else:
                
                return redirect('PROD_PRODUC')
    else:
        return render(request, "core/Perfil_productor_productos.html",{
            'usuario_autenticado': usuario_autenticado, 
            'user_info': user_info,
            'calibres':calibres_data,
            'productos': productos_data,
            'productos_productor': productos_productor})
    
    #return render(request, "core/Perfil_productor_productos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

#TRANSPORTISTA
# lista
def perfil_transp_datos(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    if request.method == 'POST':
        rut = request.POST.get('rut_usuario_DesactivarTranspor')  

        #----
        
        rutabuscar = request.POST.get('rut_transp')
        nombre = request.POST.get('nombre_transp')
        apellidopat = request.POST.get('apellido_transp')
        apellidomat = request.POST.get('apellidomat_transp')
        fechanacimiento = request.POST.get('fecha_transp')

        #---PARA CAMBIAR DATOS
        if 'modificar-TRANSP' in request.POST:

            response = actualizar_transportista(            
            rutabuscar,
            nombre,
            apellidopat,
            apellidomat,
            fechanacimiento
            )
            # Procesa la respuesta del servicio SOAP, si es necesario

            if response == 'OK':
                return redirect('TRANSP_DATOS')
            else:
                #messages.success(request, 'Los productos fueron agregados exitosamente :) ')
                return redirect('TRANSP_DATOS')
            
        if rut:

            response = desactivarCuentaTransportista(rut)

        if response == 'OK':
            return redirect('CERRAR_SESION')
        else:
            #messages.success(request, 'SU CUENTA SE HA DESACTIVADO!! ')
            return redirect('CERRAR_SESION')
    else:

        return render(request, "core/Perfil_transportista_datos.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
def perfil_transp_domici(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    return render(request, "core/Perfil_transportista_domicilio.html",{'usuario_autenticado': usuario_autenticado, 'user_info': user_info})

# lista
@user_info_required
def perfil_transp_pedi(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    #----------------------------seccion para listar los pedidos por Transportista----------------------------------------------

    ruttransportista = user_info['Rut_usuario']

    lista_pedidos_transportista = listar_pedidosTransportista(ruttransportista)

    # Parsea la cadena JSON a una lista de diccionarios
    pedidos_transportista = json.loads(lista_pedidos_transportista)
    
    print(pedidos_transportista)

    #----ENVIO DE ID_PEDIDO para actualizar estado:
    if request.method == 'POST':
        enviado = request.POST.get('id_pedido')
        recibido = request.POST.get('id_pedido_recibido')
        rechazado_transportista = request.POST.get('id_pedido_rechazado_transp')
        rechazado_cliente = request.POST.get('id_pedido_rechazado_cliente')
        #---------------------------------------------------------

        # Inicializa response a un valor predeterminado
        response = None


        idpedido = request.POST.get('id_pedido_foto')
        #imgnueva = request.POST.get('imagen_origen')
        imgnueva = request.FILES.get('imagen_origen')

        #---------------------------------------------------------
        idpedido2 = request.POST.get('id_pedido_foto_destino')
        imgnueva2 = request.FILES.get('imagen_destino')
        
        if imgnueva:

            urlIMG = 'img/'+imgnueva.name
            print(urlIMG)
                                    
            if enviado:
                response = actualizar_pedido_Enviado(enviado)
            elif recibido:
                response = actualizar_pedido_Recibido(recibido)
            elif rechazado_transportista:
                response = actualizar_pedido_recha_transportista(rechazado_transportista)
            elif rechazado_cliente:
                response = actualizar_pedido_recha_cliente(rechazado_cliente)
            elif idpedido:
                response = actualizar_IMGinicio(idpedido, urlIMG)
                if response == 'OK':
                    return redirect('TRANSP_PEDI')
                else:
                    messages.success(request, 'Imagen subida correctamente! :) ')
                    return redirect('TRANSP_PEDI')
            elif idpedido2:
                response = actualizar_IMGfinal(idpedido2, imgnueva2)

        elif imgnueva2:

            urlIMG2 = 'img/'+imgnueva2.name
            print(urlIMG2)                      
            
            if enviado:
                response = actualizar_pedido_Enviado(enviado)
            elif recibido:
                response = actualizar_pedido_Recibido(recibido)
            elif rechazado_transportista:
                response = actualizar_pedido_recha_transportista(rechazado_transportista)
            elif rechazado_cliente:
                response = actualizar_pedido_recha_cliente(rechazado_cliente)
            elif idpedido:
                response = actualizar_IMGinicio(idpedido, urlIMG)
                if response == 'OK':
                    return redirect('TRANSP_PEDI')
                else:
                    messages.success(request, 'Imagen subida correctamente! :) ')
                    return redirect('TRANSP_PEDI')
            elif idpedido2:
                response = actualizar_IMGfinal(idpedido2, urlIMG2)       
        else:

            if enviado:
                response = actualizar_pedido_Enviado(enviado)
            elif recibido:
                response = actualizar_pedido_Recibido(recibido)
            elif rechazado_transportista:
                response = actualizar_pedido_recha_transportista(rechazado_transportista)
            elif rechazado_cliente:
                response = actualizar_pedido_recha_cliente(rechazado_cliente)
            elif idpedido:
                response = actualizar_IMGinicio(idpedido, urlIMG)
                if response == 'OK':
                    return redirect('TRANSP_PEDI')
                else:
                    messages.success(request, 'Imagen subida correctamente! :) ')
                    return redirect('TRANSP_PEDI')
            elif idpedido2:
                response = actualizar_IMGfinal(idpedido2, imgnueva2)

        if response == 'OK':
            return redirect('TRANSP_PEDI')
        else:
            messages.success(request, 'La información se ha guardado exitosamente :) ')
            return redirect('TRANSP_PEDI')
    else:                
        return render(request, "core/Perfil_transportista_pedidos.html",{
            'usuario_autenticado': usuario_autenticado,
            'user_info': user_info,
            'pedidos_transpor': pedidos_transportista})

# lista
@user_info_required
def perfil_transp_transpor(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    #----------------------------seccion para listar los pedidos por Transportista----------------------------------------------

    ruttransportista = user_info['Rut_usuario']

    lista_pedidos_finalizados_transportista = listar_pedidosTransportista_Finalizados(ruttransportista)

    # Parsea la cadena JSON a una lista de diccionarios
    pedidos_transportista = json.loads(lista_pedidos_finalizados_transportista)
    
    print(pedidos_transportista)
        
    return render(request, "core/Perfil_transportista_transportes.html",{
        'usuario_autenticado': usuario_autenticado,
        'user_info': user_info,
        'pedidos_finalizados' : pedidos_transportista})

# lista
@user_info_required
def perfil_transp_vehi(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    # Obtener los datos de las marcas utilizando la función de la API
    marcas_json = listar_marca_combobox()

    # Parsea la cadena JSON a una lista de diccionarios
    marcas_data = json.loads(marcas_json)

    #----------------------------seccion para listar los productos por productor----------------------------------------------
    rutabuscar = user_info['Rut_usuario']

    print(rutabuscar)
    lista_vehiculos_transp = listar_vehiculos_transportista(rutabuscar)

    # Parsea la cadena JSON a una lista de diccionarios
    vehiculos_transportista = json.loads(lista_vehiculos_transp)

    print(vehiculos_transportista)
    if request.method == 'POST':

        formulario_id = request.POST.get('formulario_id')  # Obtén el valor del campo oculto con el id del formulario

        if formulario_id == 'miFormularioREGISTRO_TRANSPORTE':

            patente = request.POST.get('patente')
            capacidadcarga = request.POST.get('capacidad_carga')
            frigorificotrans = request.POST.get('frigorifico')
            permisocirculacion = request.POST.get('permiso_circulacion')
            transportista_rut = user_info['Rut_usuario']
            modelo_idmodelo = request.POST.get('modelo')
            

            response = crearTransporte(
                patente,
                capacidadcarga,
                frigorificotrans,
                permisocirculacion,
                transportista_rut,
                modelo_idmodelo
            )            

            if response == 'OK':
                #messages.success(request, 'La información se ha guardado exitosamente.')
                return redirect('TRANSP_VEHI')
            else:
                messages.success(request, 'El vehiculo fue registrado con éxito! :) ')
                return redirect('TRANSP_VEHI')
            
        elif formulario_id == 'formulario_eliminarVEHICULO':

            patenteaeliminar = request.POST.get('patente_eliminar')

            response = eliminarVEHICULO(patenteaeliminar)

            if response == 'OK':
                #messages.success(request, 'La información se ha guardado exitosamente.')
                return redirect('TRANSP_VEHI')
            else:
                messages.success(request, 'El vehiculo fue registrado con éxito! :) ')
                return redirect('TRANSP_VEHI')
    else:
        return render(request, "core/Perfil_transportista_vehiculos.html",{'usuario_autenticado': usuario_autenticado,
                                                                            'user_info': user_info,
                                                                            'marcas': marcas_data,
                                                                            'vehiculos': vehiculos_transportista})

#-----------------VERIFICAR SI EL TRANSPORTISTA TIENE VEHICULOS O NO--------------------------------
def tiene_vehiculos_registrados(transportista_rut):

    # Verifica si el transportista tiene vehículos registrados
    return Transporte.objects.filter(transportista_rut=transportista_rut).exists()

#----------VERIFICAR SI ALGUNO DE SUS VEHICULOS TIENE CAPACIDAD PARA LLEGAR LA CARGA---------
def obtener_maxima_capacidad_carga(transportista_rut):
    # Consulta para obtener la máxima capacidad de carga de los vehículos del transportista
    maxima_capacidad = Transporte.objects.filter(transportista_rut=transportista_rut).aggregate(Max('capacidadcarga'))['capacidadcarga__max']

    maxima_capacidad_int = int(maxima_capacidad) if maxima_capacidad is not None else 0
    return maxima_capacidad_int
#subasta------------------------------------------------------------------------------------------------
def subasta(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    #---------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Llama a la función para obtener la lista de subastas en formato JSON
    json_data = obtener_subastas_json()

    # Parsea la cadena JSON a una lista de diccionarios
    lista_de_subastas = json.loads(json_data)

    
    #----------------------------------------------------------------------------------
    # Obtén las ofertas mínimas para cada subasta agrupadas por subasta_id_subasta
    ofertas_minimas = OfertarSubasta.objects.filter(transportista_rut=user_info['Rut_usuario']).values('subasta_id_subasta').annotate(min_oferta=Min('montosubasta'))

    print('YAPEE', ofertas_minimas)
    # Crea un diccionario para almacenar las ofertas del usuario
    
    # Crea un diccionario para almacenar las ofertas mínimas del usuario
    ofertas_minimas_dict = {oferta['subasta_id_subasta']: oferta['min_oferta'] for oferta in ofertas_minimas}
    print(ofertas_minimas_dict)
    # Itera a través de las subastas
    for subasta in lista_de_subastas:
        subasta_id = subasta['id_subasta']
        
        
        # Verifica si existe una oferta del usuario para esta subasta
        if subasta_id in ofertas_minimas_dict:

            subasta['monto_oferta'] = ofertas_minimas_dict.get(subasta_id, 0) 

        else:
            subasta['monto_oferta'] = 0  # O cualquier valor que desees mostrar si no hay oferta
            #subasta['mensaje'] = 'No hay oferta mi rey'
    #----------------------------------------------------------------------------------
    ofertas_minimas = OfertarSubasta.objects.values('subasta_id_subasta').annotate(min_oferta=Min('montosubasta'))

    # Crea un diccionario para mapear subasta_id_subasta a la oferta mínima
    ofertas_minimas_dict = {oferta['subasta_id_subasta']: oferta['min_oferta'] for oferta in ofertas_minimas}

    # Itera a través de las subastas y agrega el monto de oferta mínima si está disponible 
    for subasta in lista_de_subastas:
        subasta_id = subasta['id_subasta']
        
        if subasta_id in ofertas_minimas_dict:
            subasta['oferta_minima'] = ofertas_minimas_dict[subasta_id]
        else:
            subasta['oferta_minima'] = 'No hay oferta para esta subasta'
    #------------------------------------------------------------------------------------
    
    # Verifica si el formulario se envió mediante POST
    if request.method == 'POST':

        capacidad_carga_subasta = request.POST.get('peso_pedido')
        print('peso pedido:' , capacidad_carga_subasta)
        #la capacidad máxima de carga de los vehículos del transportista
        maxima_capacidad = obtener_maxima_capacidad_carga(user_info['Rut_usuario'])

        print(maxima_capacidad)

        # Verifica si el transportista tiene vehículos registrados
        tiene_vehiculos = tiene_vehiculos_registrados(user_info['Rut_usuario'])
        print(tiene_vehiculos)

        if not tiene_vehiculos:
            mensaje_error = 'Debes tener al menos un vehículo registrado para hacer ofertas en subastas.'
            return render(request, "core/Subastas.html", {"mensaje_error": mensaje_error,
                                                           'usuario_autenticado': usuario_autenticado,
                                                           'user_info': user_info})
        elif int(float(capacidad_carga_subasta)) > int(maxima_capacidad):
            mensaje_error = 'Ninguno de tus vehiculos registrados cuenta con la capacidad para llevar la carga del pedido.'
            return render(request, "core/Subastas.html", {"mensaje_error": mensaje_error,
                                                       'usuario_autenticado': usuario_autenticado,
                                                       'user_info': user_info})
        else:
            # Procesa la oferta
            montosubasta = request.POST.get('monto')
            subasta_id = request.POST.get('id_subasta')
            transportista_rut = user_info['Rut_usuario']
            pedido_idpedido = request.POST.get('id_pedido')

            response = crearOfertaSubasta(
                montosubasta=montosubasta,
                subasta_id_subasta=subasta_id,
                transportista_rut=transportista_rut,
                pedido_idpedido=pedido_idpedido
            )

            if response == 'OK':
                return redirect('SUBASTAS')
            else:
                return redirect('SUBASTAS')
    else:   
        return render(request, "core/Subastas.html",{"subastas": lista_de_subastas,
                                                'usuario_autenticado': usuario_autenticado,
                                                'user_info': user_info})

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

#--------------------------------------------------------------------------------------------------------
#COMBO BOXXX REGION Y COMUNA
def regiones_por_pais(request):

    idpais = request.GET.get('idpais')

    # Obtener los datos de las regiones utilizando la función de la API
    regiones_json = listar_region_por_pais(idpais)

    # Parsea la cadena JSON a una lista de diccionarios
    regiones_data = json.loads(regiones_json)

    return render(request, 'core/combobox_regiones.html',{'regiones': regiones_data})

def comunas_por_region(request):

    idregion = request.GET.get('idregion')

    # Obtener los datos de las regiones utilizando la función de la API
    comunas_json = listar_comuna_por_region(idregion)

    # Parsea la cadena JSON a una lista de diccionarios
    comunas_data = json.loads(comunas_json)

    return render(request, 'core/combobox_comunas.html',{'comunas': comunas_data})

#--------------------------------------------------------------------------------------------------------
#COMBO BOXX Modelo de vehiculo por id_marca
def modelo_por_marca(request):
    
    idmarca = request.GET.get('marca')

    # Obtener los datos de las regiones utilizando la función de la API
    modelos_json = listar_modelo_por_marca(idmarca)

    # Parsea la cadena JSON a una lista de diccionarios
    modelos_data = json.loads(modelos_json)

    return render(request, 'core/combobox_modelos.html',{'modelos': modelos_data})

#----------MERCADO PAGO--------------------------
@user_info_required
def mercado_pago(request, id_pedido, total_final):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    # Convierte total_final a un número decimal o flotante si es necesario
    total_final = float(total_final)

    #print(id_pedido)
    #print(total_final)

    # Agrega credenciales
    mp = mercadopago.SDK("TEST-2425236459265153-110720-6072014a12c4a69929615f29f8ffe128-755995052")    
    #mp = mercadopago.SDK("TEST-8830216595670397-111017-5a43b09d9f5af1773697ddbdd6758677-1540801280") 

    # Concatena el id_pedido con el título
    title = f"Pedido Número {id_pedido}"
    # Define las URLs de retorno
    success_url = urljoin(request.build_absolute_uri(), 'success/')
    pending_url = urljoin(request.build_absolute_uri(), 'pending/')
    failure_url = urljoin(request.build_absolute_uri(), 'failure/')


    # Define los detalles de la preferencia, como el ítem a vender y sus atributos
    preference_data = {
        "items": [
            {
                "title": title,
                "description": "Monto total pedido",
                "quantity": 1,
                "unit_price": total_final,
                "statement_descriptor": "Feria Virtual"
            }
        ],
        "back_urls": {
            "success": success_url,  
            "pending": pending_url,
            "failure": failure_url,         
        },
        "binary_mode": True  # Habilita el modo binario
    }

    # Crea la preferencia
    preference_response = mp.preference().create(preference_data)
    preference = preference_response["response"]

    # Pasa la preferencia a la plantilla HTML
    return render(request, "core/mercado_pago.html", {'usuario_autenticado': usuario_autenticado,
                                                      'user_info': user_info,
                                                      'preference_id': preference["id"]})


@user_info_required
@csrf_exempt
def success_view(request, id_pedido, total_final):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})


    collection_id = request.GET.get('collection_id')
    collection_status = request.GET.get('collection_status')
    payment_id = request.GET.get('payment_id')
    payment_type = request.GET.get('payment_type')
    status = request.GET.get('status')
    external_reference = request.GET.get('external_reference')
    merchant_order_id = request.GET.get('merchant_order_id')
    preference_id = request.GET.get('preference_id')
    site_id = request.GET.get('site_id')
    processing_mode = request.GET.get('processing_mode')
    merchant_account_id = request.GET.get('merchant_account_id')


    #AHORA USAMOS EL METODO PARA CREAR EL PAGO y dejar el pedido en estado '4' --> 'Pago exitoso'
    pedido_idpedido = id_pedido
    pago_exitoso = 0 #aca inicializamos la variable
    
    if status == 'approved':

        pago_exitoso = 1                               

        response = crearPago(pago_exitoso, pedido_idpedido)

    # Ahora, pasamos estos valores a la plantilla
    return render(request, 'core/success.html', {'usuario_autenticado': usuario_autenticado,
                                                 'user_info': user_info,
        'collection_id': collection_id,
        'collection_status': collection_status,
        'payment_id': payment_id,
        'payment_type': payment_type,
        'status': status,
        'external_reference': external_reference,
        'merchant_order_id': merchant_order_id,
        'preference_id': preference_id,
        'site_id': site_id,
        'processing_mode': processing_mode,
        'merchant_account_id': merchant_account_id,
        'total_pago': total_final
    })

#-----------------------------------------------------
# lista
@user_info_required
def confirmeDireccion(request):
    usuario_autenticado = request.session.get('usuario_autenticado', False)
    user_info = request.session.get('user_info', {})

    if request.method == 'POST':
        idcliente = user_info['id_cliente']
        nuevadireccion = request.POST.get('direccion_despacho')
        print('ACA EST',idcliente)
        response = actualizarDireccionDespacho(
            idcliente,
            nuevadireccion
        )

        print(response)
        if response == 'OK':
            return redirect('CLIENTE_PEDI')
        else:
            messages.success(request, 'La información se ha guardado exitosamente :) ')
            return redirect('CLIENTE_PEDI')
    else:

        return render(request, "core/Confirmar_direccion.html",
                      {'usuario_autenticado': usuario_autenticado,
                        'user_info': user_info})



