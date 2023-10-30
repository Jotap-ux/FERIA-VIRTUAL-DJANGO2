from django import forms
from django.shortcuts import render, redirect
#import zeep
from zeep import Client
import json
from datetime import datetime


URL_WEBSERVICE = 'http://localhost:8080/WSFERIAVIRTUAL/WSFERIAVIRTUAL?WSDL'

#CREACIÓN DE USUARIOS --------------------------------------------------------------------------------------
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

def crear_clienteEmpresa(direccion, correoelectronico, contrasena, identificadorempresa, razonsocial, comuna_idcomuna):

    client = Client(URL_WEBSERVICE)

    response = client.service.agregarClienteEmp(direccion=direccion, correoelectronico=correoelectronico,contrasena=contrasena,
                                                identificadorempresa=identificadorempresa,razonsocial=razonsocial, comuna_idcomuna=comuna_idcomuna)

    return response

def crear_transportista(rut, dv, nombre, apellidopat, apellidomat, fechanacimiento, direccion, correoelectronico, contrasena):
    client = Client(URL_WEBSERVICE)

    response = client.service.agregarTransportista(rut=rut, dv=dv, nombre=nombre, apellidopat=apellidopat, apellidomat=apellidomat,
                                               fechanacimiento=fechanacimiento, direccion=direccion, correoelectronico=correoelectronico,
                                               contrasena=contrasena)

    return response

#--------------------------------------------------------------------------------------------------------
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
            'calibre_id': producto.idcalibre,
            'img': producto.img,
            'nombre_productor': producto.nombre_productor,
            'nombre_producto': producto.nombreproducto,
            'precio': producto.precio,
            'id_producto' : producto.producto_idproducto,            
            'rut_productor': producto.productor_rut,
            'stock': producto.stock   
        }
        productos_data.append(producto_data)
    
    # Convierte la lista de productos a una cadena JSON
    json_data = json.dumps(productos_data, indent=4)
    
    return json_data

def autenticar_usuario(correoelectronico, contrasena):
    
    client = Client(URL_WEBSERVICE)
    
    peticion_login = client.service.listarlogin1(correoelectronico, contrasena)
    
    if peticion_login is None:
        # El usuario no existe, devuelve un valor especial o mensaje de error
        return json.dumps({'error': 'El usuario no existe'}, indent=4)
    
    
    response_data = {
        'Rut_usuario': peticion_login.identificador,
        'Tipo_usuario': peticion_login.tipousuario
    }
    
    # Convierte el diccionario a una cadena JSON
    json_data = json.dumps(response_data, indent=4)
    
    return json_data

def agregar_productos(precio, stock, calibre_idcalibre, producto_idproducto, productor_rut, img):

    client = Client(URL_WEBSERVICE)

    response = client.service.agregarNuevoProducto(precio=precio, stock=stock, calibre_idcalibre=calibre_idcalibre,
                                                   producto_idproducto=producto_idproducto, productor_rut=productor_rut, img=img)

    return response   

def listar_calibres():
    
    # Crea un cliente SOAP con la URL del servicio web
    client = Client(URL_WEBSERVICE)

    # Realizamos la petición al servicio web
    peticion_listar_calibres = client.service.listarCalibre()

    # Inicializa una lista para almacenar los datos de los calibres
    calibres_data = []

    # Itera a través de la lista de calibres en la respuesta
    for calibre in peticion_listar_calibres:
        calibre_data = {
            'desc_calibre': calibre.desccalibre,
            'id_calibre': calibre.idcalibre,
        }
        calibres_data.append(calibre_data)

    # Convierte la lista de calibres a una cadena JSON
    json_data = json.dumps(calibres_data, indent=4)

    return json_data

def listar_productos_combobox():
    
    # Crea un cliente SOAP con la URL del servicio web
    client = Client(URL_WEBSERVICE)

    # Realizamos la petición al servicio web
    peticion_listar_productos_combobox = client.service.listarProductosxIdyNombre()

    # Inicializa una lista para almacenar los datos de los productos
    productos_data = []

    # Itera a través de la lista de calibres en la respuesta
    for productos in peticion_listar_productos_combobox:
        producto_data = {
            'id_producto': productos.idproducto,
            'nombre_producto': productos.nombreproducto,
        }
        productos_data.append(producto_data)

    # Convierte la lista de calibres a una cadena JSON
    json_data = json.dumps(productos_data, indent=4)

    return json_data
#client = zeep.Client(URL_WEBSERVICE) -- listarProductos()
#---------------------------------------------------
def crearPedido(cliente_id_cliente):
    
    client = Client(URL_WEBSERVICE)

    response = client.service.crearNuevoPedido(cliente_id_cliente=cliente_id_cliente)

    id_pedido = int(response)  # Convierte la respuesta a un entero
    id_pedido_str = str(id_pedido)  # Convierte el entero a una cadena

    # Resto de tu lógica
    #print(id_pedido_str)

    return id_pedido_str

def crearDetalle_pedido(cantidad, idproducto, productor_rut, pedido_idpedido, calibre_idcalibre):

    client = Client(URL_WEBSERVICE)

    response = client.service.crearNuevoDetallePedido(cantidad=cantidad, idproducto=idproducto, productor_rut=productor_rut, pedido_idpedido=pedido_idpedido, calibre_idcalibre=calibre_idcalibre)

    return response

def obtener_subastas_json():

     # Crea un cliente SOAP con la URL del servicio web
    client = Client(URL_WEBSERVICE)
    
    # Realizamos la petición al servicio web
    peticion_listar_subastas = client.service.listarSubastas()
    
    # Inicializa una lista para almacenar los datos de las subastas
    subastas_data = []
    
    # Itera a través de la lista de subastas
    for subasta in peticion_listar_subastas:
        subasta_data = {
            'cantidad_productos': subasta.cantidadTotal,
            'comuna_destino': subasta.comunaDestino,
            'comuna_origen': subasta.comunaOrigen,
            'direccion_destino': subasta.direccionDestino,
            'direccion_origen': subasta.direccionOrigen,
            'fecha_subasta': datetime.strptime(subasta.fechaSubasta, "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y"),
            'hora_termino': subasta.horarioTermino,
            'id_pedido': subasta.idPedido,
            'id_subasta' : subasta.idSubasta,    
            'nombre_cliente': subasta.nombreCliente,
            'nombre_clienteEmpresa': subasta.nombreClienteEmp,        
            'total_transporte': subasta.totalTransporte
        }
        subastas_data.append(subasta_data)
    
    # Convierte la lista de productos a una cadena JSON
    json_data = json.dumps(subastas_data, indent=4)
    
    return json_data

#COMBO-BOX PAIS, REGION Y COMUNA

def listar_pais_combobox():
     # Crea un cliente SOAP con la URL del servicio web
    client = Client(URL_WEBSERVICE)

    # Realizamos la petición al servicio web
    peticion_listar_pais_combobox = client.service.listarPais()

    # Inicializa una lista para almacenar los datos de los productos
    paises_data = []

    # Itera a través de la lista de calibres en la respuesta
    for pais in peticion_listar_pais_combobox:
        pais_data = {
            'id_pais': pais.idpais,
            'nombre_pais': pais.nombrepais,
        }
        paises_data.append(pais_data)

    # Convierte la lista de calibres a una cadena JSON
    json_data = json.dumps(paises_data, indent=4)

    return json_data

def listar_region_por_pais(idpais):

    client = Client(URL_WEBSERVICE)

    peticion_region = client.service.listarRegionesPorIDPais(arg0=idpais)

    # Inicializa una lista para almacenar los datos de los productos
    regiones_data = []

    # Itera a través de la lista de calibres en la respuesta
    for region in peticion_region:
        region_data = {
            'id_region': region.idregion,
            'nombre_region': region.nombreregion,
        }
        regiones_data.append(region_data)

    # Convierte la lista de calibres a una cadena JSON
    json_data = json.dumps(regiones_data, indent=4)

    #print(json_data)
    return json_data

def listar_comuna_por_region(idregion):

    client = Client(URL_WEBSERVICE)

    peticion_comuna = client.service.listarComuna(arg0=idregion)

    # Inicializa una lista para almacenar los datos de los productos
    comunas_data = []

    # Itera a través de la lista de calibres en la respuesta
    for comuna in peticion_comuna:
        comuna_data = {
            'id_comuna': comuna.idcomuna,
            'nombre_comuna': comuna.nombrecomuna,
        }
        comunas_data.append(comuna_data)

    # Convierte la lista de calibres a una cadena JSON
    json_data = json.dumps(comunas_data, indent=4)

    #print(json_data)
    return json_data





    #id_pedido = int(response)  # Convierte la respuesta a un entero
    #id_pedido_str = str(id_pedido)  # Convierte el entero a una cadena

    # Resto de tu lógica
    #print(id_pedido_str)


    #return response
    #return id_pedido_str


#---------------------FIN SECCION DE COMBOBOX-------------------------------------------------

def listarProductos_Productor(rut_productor):
    client = Client(URL_WEBSERVICE)

    peticion_productos_productor = client.service.listarproductosporrutproductor(arg0=rut_productor)

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

    #print(json_data)
    return json_data


