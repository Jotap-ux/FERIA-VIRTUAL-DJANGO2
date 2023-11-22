# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

#ok
class Administrador(models.Model):
    idusuario = models.CharField(primary_key=True, max_length=30)  # The composite primary key (idusuario, nombreusuario) found, that is not supported. The first column is selected.
    nombreusuario = models.CharField(max_length=50)
    contrasenausuario = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'administrador'
        unique_together = (('idusuario', 'nombreusuario'),)

#ok
class Bodegamp(models.Model):
    idbodega = models.CharField(primary_key=True, max_length=300)
    ubicacionbodega = models.CharField(max_length=300)
    comuna_idcomuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='comuna_idcomuna')

    class Meta:
        managed = False
        db_table = 'bodegamp'

#ok
class Calibre(models.Model):
    idcalibre = models.CharField(primary_key=True, max_length=50)
    desccalibre = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'calibre'

#ok
class Categoria(models.Model):
    idcategoria = models.CharField(primary_key=True, max_length=50)
    desccategoria = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'categoria'

#ok
class Cliente(models.Model):
    id_cliente = models.CharField(primary_key=True, max_length=50)
    rut = models.BigIntegerField(blank=True, null=True)
    dv = models.CharField(max_length=1, blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellidopat = models.CharField(max_length=50, blank=True, null=True)
    apellidomat = models.CharField(max_length=50, blank=True, null=True)
    estadoactivo = models.CharField(max_length=1)
    direccion = models.CharField(max_length=300)
    fechanacimiento = models.DateField(blank=True, null=True)
    correoelectronico = models.CharField(max_length=300)
    contrasena = models.CharField(max_length=300)
    identificadorempresa = models.CharField(max_length=300, blank=True, null=True)
    razonsocial = models.CharField(max_length=300, blank=True, null=True)
    comuna_idcomuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='comuna_idcomuna', blank=True, null=True)
    tipocliente_idcliente = models.ForeignKey('Tipocliente', models.DO_NOTHING, db_column='tipocliente_idcliente')

    class Meta:
        managed = False
        db_table = 'cliente'

#ok
class Comuna(models.Model):
    idcomuna = models.CharField(primary_key=True, max_length=300)
    nombrecomuna = models.CharField(max_length=300)
    region_idregion = models.ForeignKey('Region', models.DO_NOTHING, db_column='region_idregion')

    class Meta:
        managed = False
        db_table = 'comuna'

#ok
class Consultor(models.Model):
    idusuario = models.CharField(primary_key=True, max_length=30)  # The composite primary key (idusuario, nombreusuario) found, that is not supported. The first column is selected.
    nombreusuario = models.CharField(max_length=50)
    contrasenausuario = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'consultor'
        unique_together = (('idusuario', 'nombreusuario'),)

#ok
class ContratoClienteEx(models.Model):
    idcontrato = models.CharField(primary_key=True, max_length=50)
    fechainiciocontrato = models.DateField()
    fechaterminocontrato = models.DateField()
    cliente_id_cliente = models.OneToOneField(Cliente, models.DO_NOTHING, db_column='cliente_id_cliente')

    class Meta:
        managed = False
        db_table = 'contrato_cliente_ex'

#ok(modificado)
class ContratoTransporte(models.Model):
    id_contrato = models.CharField(primary_key=True, max_length=300)
    fechacontrato = models.DateField()
    orden_transporte_idordent = models.OneToOneField('OrdenTransporte', models.DO_NOTHING, db_column='orden_transporte_idordent')

    class Meta:
        managed = False
        db_table = 'contrato_transporte'

#ok(ahora pasamos el idcalibre)
class DetallePedido(models.Model):
    cantidad = models.BigIntegerField()
    idproducto = models.BigIntegerField(primary_key=True)
    productor_rut = models.ForeignKey('ProductorProducto', models.DO_NOTHING, db_column='productor_rut', to_field='productor_rut', related_name='detallepedido_productor_rut_set')
    pedido_idpedido = models.ForeignKey('Pedido', models.DO_NOTHING, db_column='pedido_idpedido')
    idcalibre = models.ForeignKey('ProductorProducto', models.DO_NOTHING, db_column='idcalibre', to_field='calibre_idcalibre', related_name='detallepedido_idcalibre_set')

    class Meta:
        managed = False
        db_table = 'detalle_pedido'
        unique_together = (('idproducto', 'productor_rut', 'idcalibre', 'pedido_idpedido'),)

#tabla nueva(direccion entrega pedido)
class Direccion(models.Model):
    direccion_nueva = models.CharField(max_length=300)
    cliente_id_cliente = models.OneToOneField(Cliente, models.DO_NOTHING, db_column='cliente_id_cliente', primary_key=True, related_name='direccion_cliente')

    class Meta:
        managed = False
        db_table = 'direccion'

#ok
class Estadopago(models.Model):
    idpago = models.CharField(primary_key=True, max_length=50)
    descestadopago = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'estadopago'

#ok
class Estadopedido(models.Model):
    idestado = models.CharField(primary_key=True, max_length=300)
    descripcionestado = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'estadopedido'

#ok
class Marca(models.Model):
    idmarca = models.CharField(primary_key=True, max_length=300)
    descmarca = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'marca'

#ok
class Modelo(models.Model):
    idmodelo = models.CharField(primary_key=True, max_length=300)
    descmodelo = models.CharField(max_length=300)
    marca_idmarca = models.ForeignKey(Marca, models.DO_NOTHING, db_column='marca_idmarca')

    class Meta:
        managed = False
        db_table = 'modelo'

#ok - se agrego despues tambien.
class OfertarSubasta(models.Model):
    montosubasta = models.BigIntegerField()
    subasta_id_subasta = models.OneToOneField('Subasta', models.DO_NOTHING, db_column='subasta_id_subasta', primary_key=True)  # The composite primary key (subasta_id_subasta, transportista_rut) found, that is not supported. The first column is selected.
    transportista_rut = models.ForeignKey('Transportista', models.DO_NOTHING, db_column='transportista_rut')

    class Meta:
        managed = False
        db_table = 'ofertar_subasta'
        unique_together = (('subasta_id_subasta', 'transportista_rut'),)

#ok (se agrega imagen de origen y destino)
class OrdenTransporte(models.Model):
    idordent = models.CharField(primary_key=True, max_length=30)
    descordent = models.CharField(max_length=200)
    fechatransporte = models.DateField()
    diasdespacho = models.BigIntegerField()
    direccionorigen = models.CharField(max_length=300)
    direcciondestino = models.CharField(max_length=300)
    pedido_idpedido = models.OneToOneField('Pedido', models.DO_NOTHING, db_column='pedido_idpedido')
    transportista_rut = models.ForeignKey('Transportista', models.DO_NOTHING, db_column='transportista_rut')
    img_url_inicio = models.CharField(max_length=300, blank=True, null=True)
    img_url_termino = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orden_transporte'


#ok (se elimina el estadopago)
class Pago(models.Model):
    idpago = models.CharField(primary_key=True, max_length=30)
    fechapago = models.DateField()
    pedido_idpedido = models.OneToOneField('Pedido', models.DO_NOTHING, db_column='pedido_idpedido')
    estadopago_idpago = models.ForeignKey(Estadopago, models.DO_NOTHING, db_column='estadopago_idpago')

    class Meta:
        managed = False
        db_table = 'pago'

#ok
class Pais(models.Model):
    idpais = models.CharField(primary_key=True, max_length=50)
    nombrepais = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'pais'

#ok
class Parametricaproduc(models.Model):
    idproduc = models.CharField(primary_key=True, max_length=300)  # The composite primary key (idproduc, idcalibre) found, that is not supported. The first column is selected.
    idcalibre = models.CharField(max_length=300)
    pesoproducaprox = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'parametricaproduc'
        unique_together = (('idproduc', 'idcalibre'),)

#ok
class Pedido(models.Model):
    idpedido = models.CharField(primary_key=True, max_length=50)
    fechapedido = models.DateField()
    totalpedido = models.BigIntegerField()
    iva = models.BigIntegerField()
    comisionmaipogrande = models.BigIntegerField()
    totaltransporte = models.BigIntegerField()
    totalfinal = models.BigIntegerField()
    pesototalpedido = models.FloatField()
    estadopedido_idestado = models.ForeignKey(Estadopedido, models.DO_NOTHING, db_column='estadopedido_idestado')
    bodegamp_idbodega = models.ForeignKey(Bodegamp, models.DO_NOTHING, db_column='bodegamp_idbodega')
    tiposeguro_idtiposeguro = models.ForeignKey('Tiposeguro', models.DO_NOTHING, db_column='tiposeguro_idtiposeguro')
    cliente_id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente_id_cliente')

    class Meta:
        managed = False
        db_table = 'pedido'

#ok (se le agrega la url de la imagen)
class Producto(models.Model):
    idproducto = models.CharField(primary_key=True, max_length=30)
    nombreproducto = models.CharField(max_length=50)
    descproducto = models.CharField(max_length=100)
    categoria_idcategoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='categoria_idcategoria')
    img = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'producto'

#ok
class Productor(models.Model):
    rut = models.BigIntegerField(primary_key=True)
    dv = models.CharField(max_length=1)
    nombre = models.CharField(max_length=30)
    apellidopat = models.CharField(max_length=50)
    apellidomat = models.CharField(max_length=50)
    estadoactivo = models.CharField(max_length=1)
    fechanacimiento = models.DateField()
    direccion = models.CharField(max_length=300)
    correoelectronico = models.CharField(max_length=300)
    contrasena = models.CharField(max_length=300)
    comuna_idcomuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='comuna_idcomuna')

    class Meta:
        managed = False
        db_table = 'productor'

#ok (se elimina la url de la imagen)
class ProductorProducto(models.Model):
    precio = models.BigIntegerField()
    stock = models.BigIntegerField()
    producto_idproducto = models.OneToOneField(Producto, models.DO_NOTHING, db_column='producto_idproducto', primary_key=True)  # The composite primary key (producto_idproducto, productor_rut, calibre_idcalibre) found, that is not supported. The first column is selected.
    productor_rut = models.ForeignKey(Productor, models.DO_NOTHING, db_column='productor_rut', unique=True)
    calibre_idcalibre = models.ForeignKey(Calibre, models.DO_NOTHING, db_column='calibre_idcalibre', unique=True)

    class Meta:
        managed = False
        db_table = 'productor_producto'
        unique_together = (('producto_idproducto', 'productor_rut', 'calibre_idcalibre'),)

#ok
class Region(models.Model):
    idregion = models.CharField(primary_key=True, max_length=300)
    nombreregion = models.CharField(max_length=300)
    pais_idpais = models.ForeignKey(Pais, models.DO_NOTHING, db_column='pais_idpais')

    class Meta:
        managed = False
        db_table = 'region'

#ok
class Seguro(models.Model):
    idseguro = models.CharField(primary_key=True, max_length=300)
    nombreaseguradora = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'seguro'


#ok - se agrego despues
class Subasta(models.Model):
    id_subasta = models.CharField(primary_key=True, max_length=50)
    fechasubasta = models.DateField()
    horainiciosubasta = models.DateTimeField()
    horaterminosubasta = models.DateTimeField()
    estadodelasubasta = models.CharField(max_length=1)
    pedido_idpedido = models.OneToOneField(Pedido, models.DO_NOTHING, db_column='pedido_idpedido')

    class Meta:
        managed = False
        db_table = 'subasta'

#ok (tabla nueva para los errores)
class TablaError(models.Model):
    id_error = models.CharField(primary_key=True, max_length=250)
    desc_errores = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'tabla_error'

#ok
class Tipocliente(models.Model):
    idcliente = models.CharField(primary_key=True, max_length=300)
    descripciontipo = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'tipocliente'

#ok
class Tiposeguro(models.Model):
    primaseguro = models.BigIntegerField()
    seguro_idseguro = models.ForeignKey(Seguro, models.DO_NOTHING, db_column='seguro_idseguro')
    idtiposeguro = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'tiposeguro'

#ok
class Transporte(models.Model):
    patente = models.CharField(primary_key=True, max_length=300)
    capacidadcarga = models.BigIntegerField()
    frigorificotrans = models.CharField(max_length=1)
    permisocirculacion = models.CharField(max_length=1)
    transportista_rut = models.ForeignKey('Transportista', models.DO_NOTHING, db_column='transportista_rut')
    modelo_idmodelo = models.ForeignKey(Modelo, models.DO_NOTHING, db_column='modelo_idmodelo')

    class Meta:
        managed = False
        db_table = 'transporte'

#ok
class Transportista(models.Model):
    rut = models.BigIntegerField(primary_key=True)
    dv = models.CharField(max_length=1)
    nombre = models.CharField(max_length=30)
    apellidopat = models.CharField(max_length=50)
    apellidomat = models.CharField(max_length=50)
    estadoactivo = models.CharField(max_length=1)
    fechanacimiento = models.DateField()
    direccion = models.CharField(max_length=300)
    correoelectronico = models.CharField(max_length=300)
    contrasena = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'transportista'

#32 total------------------------------------------------------------------------------------------