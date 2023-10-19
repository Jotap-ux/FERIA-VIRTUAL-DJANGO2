from django import forms
from django.shortcuts import render, redirect
from .conexionWebService import crear_productor, crear_clienteNormal, crear_clienteEmpresa
#from.models import Productor, Cliente
from .models import Producto
from django.http import HttpResponse

# lista
def index(request):
    return render(request, "core/index.html")

# LISTANDO TODOS LOS PRODUCTOS DISPONIBLES EN LA BD
def productos(request):

    productos = Producto.objects.all()

    data = {
        'productos' : productos
    }

    return render(request, "core/Productos.html", data)

# lista
def nosotros(request):
    return render(request, "core/Nosotros.html")

# lista
def contacto(request):
    return render(request, "core/Formulario_contacto.html")

# lista
def inicio_sesion(request):
    return render(request, "core/Inicio_de_sesión.html")

# lista
def carrito(request):
    return render(request, "core/Carrito.html")

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
    return render(request, "core/Perfil_cliente_datos.html")

# lista
def perfil_cli_domici(request):
    return render(request, "core/Perfil_cliente_domicilio.html")

# lista
def perfil_cli_pedi(request):
    return render(request, "core/Perfil_cliente_pedidos.html")

#PRODUCTOR-------------------------------------------------------------------------------------
# lista
def perfil_pro_datos(request):
    return render(request, "core/Perfil_productor_datos.html")

# lista
def perfil_pro_domici(request):
    return render(request, "core/Perfil_productor_domicilio.html")

# lista
def perfil_pro_envios(request):
    return render(request, "core/Perfil_productor_envios.html")

# lista
def perfil_pro_pedi(request):
    return render(request, "core/Perfil_productor_pedidos.html")

# lista
def perfil_pro_productos(request):
    return render(request, "core/Perfil_productor_productos.html")

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
    return render(request, "core/Producto_detalle.html")