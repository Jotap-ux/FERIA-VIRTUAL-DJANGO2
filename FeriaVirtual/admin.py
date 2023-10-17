from django.contrib import admin

# Register your models here.

from .models import Bodegamp, Administrador, Calibre, Categoria, Cliente, Comuna, Consultor, ContratoClienteEx
from .models import ContratoTransporte, DetallePedido, Estadopago, Estadopedido, Marca, Modelo, OrdenTransporte
from .models import Pago, Pais, Parametricaproduc, Pedido, Producto, Productor, ProductorProducto, Region
from .models import Seguro, Tipocliente, Tiposeguro, Transporte, Transportista

#para ver las tablas desde django admin...
admin.site.register(Productor)