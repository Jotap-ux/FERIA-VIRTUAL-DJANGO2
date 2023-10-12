from django.shortcuts import render

# lista
def index(request):
    return render(request, "core/index.html")

# lista
def productos(request):
    return render(request, "core/Productos.html")

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

# lista
def regis_clien_em(request):
    return render(request, "core/Registro_cliente_empresa.html")

# lista
def regis_clien_per(request):
    return render(request, "core/Registro_cliente_persona.html")

# lista
def regis_prod(request):
    return render(request, "core/Registro_productor.html")

# lista
def regis_transp(request):
    return render(request, "core/Registro_transportista.html")

# lista
def regis_transp2(request):
    return render(request, "core/Registro_transportista2.html")

#PERFILES DE CADA USUARIO
#CLIENTE

# falta!
def perfil_cli_datos(request):
    return render(request, "core/Perfil_cliente_datos.html")

# falta!
def perfil_cli_domici(request):
    return render(request, "core/Perfil_cliente_domicilio.html")

# falta!
def perfil_cli_pedi(request):
    return render(request, "core/Perfil_cliente_pedidos.html")