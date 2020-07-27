from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


######--------------------PRODUCTO----------------------------####

# Clase que define el producto
class Producto(models.Model):  #Producto Clase

    id = models.AutoField(primary_key=True) #id del Producto
    nombre = models.CharField(max_length=100, blank=False)  # Nombre del Producto
    envase = models.IntegerField(null=True, blank=False)
    procedencia = models.CharField(max_length=3, blank=False)
    producto = models.CharField(max_length=100, unique=True) #nombre*envase* procedencia (para hacer el producto unico)
    stock = models.IntegerField(blank=True, null=True) #cantidad en stock de ese producto
    stockCritico = models.IntegerField(blank=False)  # minimun stock
    kg = models.IntegerField(default=1, editable=False)  #envase*stock
    Observaciones = models.TextField(max_length=100, blank=True)  # Observaciones inherentes al producto
    Vencimiento = models.DateField(auto_now_add=False)  #Fecha de vencimiento del producto
    Critico = models.CharField(max_length=30, editable=False, default=1)#Estado que define si el stock es critico o no.
    asteriscos = (("X", "X"), (".", ".")) #Opciones de Asterisco (para impresion del remito)
    asterisco = models.CharField(max_length=2, null=True, choices=asteriscos) #campo que define las opciones de asterisco

    # Metodos de la CLase Producto
    # String Class
    def __str__(self):
        return "{}, Stock: {} ".format(self.producto, self.stock)


    #Metodo que define el metodo de guardado : (campo prducto y campo kg)
    def save(self, *args, **kwargs):  # forma de guardado que analiza si el stock es critico, actualiza su estado
        self.producto = self.nombre + " " + str(self.envase) + " " + self.procedencia
        self.kg = self.envase * self.stock
        #si el stock es menor al stock critico, entonces es "Critico"
        if (self.stock <= self.stockCritico):
            self.Critico = "Critico"
        else:
            self.Critico = "No Critico"
        super().save(*args, **kwargs)


    #Orden de representacion de los objectos de la clase:
    class Meta:
        ordering = ['producto']


#######------------------CLIENTE_PROVEEDOR----------------######


class Cliente_Proveedor(models.Model):
    # modelo que define al proveedor o cliente
    id = models.AutoField(primary_key=True) #campo que define el id del cliente/proveedor
    tipos = (("Cliente", "Cliente"), ("Proveedor", "Proveedor")) #campo de opciones del proveedro
    tipo = models.CharField(max_length=20, blank=True, choices=tipos) #campo que define los tipos seleccionables del tipo de cliente del modelo
    nombre = models.CharField(max_length=50, blank=False)# campo que define el nombre del Cliente/Proveedor
    direccion = models.CharField(max_length=50, blank=False) #idem direccion
    telefono = models.CharField(blank=False, max_length=20)#idem telefono
    e_mail = models.CharField(max_length=30)#idem email


    #metodo de representacion del modelo
    def __str__(self):
        return self.nombre

    # clase que ordena los clientes por nombre
    class Meta:
        ordering = ['nombre']


##########------------------REMITO--------------------------####################

class Remito(models.Model):
    # modelo que define a los Remitos
    id = models.AutoField(primary_key=True) #id de cada remito
    Numero = models.CharField(max_length=30, unique=True) #numero unico del remito
    Orden_de_Compra_Nro = models.CharField(max_length=40) #numero de orden de compra del remito
    Estado = (("PREPARANDO REMITO", "PREPARANDO REMITO"),
              ("RETIRADO", "RETIRADO"),
              ("ENTREGADO", "ENTREGADO"),
              ("FACTURADO", "FACTURADO"),
              ("COBRADO", "COBRADO"),
              ("AJUSTE STOCK", "AJUSTE STOCK"),
              ("INGRESO RECIBIDO", "INGRESO RECIBIDO"))  # posibilidades del Estado

    Cliente_o_Proveedor = models.ForeignKey(Cliente_Proveedor, on_delete=models.CASCADE) #llave foranea a Cliente Proveddor 1M
    Estado = models.CharField(max_length=20, blank=True, choices=Estado)#campo que define el estado sobre las posibildades definidas antes
    Fecha = models.DateTimeField(auto_now_add=True) #Fecha de creacion del remito (automatica)
    Lote = models.CharField(max_length=20, blank=True)#lote del remito
    Valor_Declarado = models.CharField(max_length=100)#valor declarado del remito
    Flete = models.CharField(max_length=20, verbose_name=" Flete a Cargo")#Flete a cargo del remito
    Retira = models.CharField(max_length=20)#Persona o entidad que retira el pedido
    Observaciones = models.TextField(max_length=70, blank=True)#Comentarios sobre el remito

    #metodo que define la representacion del modelo
    def __str__(self):  # retorna los strings de:
        return ' Remito : {}  , {} '.format(self.Numero,
                                            self.Cliente_o_Proveedor)
    #Clase que define el orden de representacion del modelo, el nombre en singular y plurar del modelo
    class Meta:
        ordering = ['-Fecha']
        verbose_name_plural = "Remitos"
        verbose_name = "Remito"




#########---------------------CCERTIFICACIONES----------------------############

class Certificaciones(models.Model):
    # modelo que define a las Certificaciones

    id = models.AutoField(primary_key=True) #numero de identificacion unico de la certificacion
    Fecha = models.DateField(help_text= "Ingresar Fecha con Formato MM/DD/AA") #Fecha a la que corresponde la certificacion
    Numero = models.CharField(max_length=30, unique=True) #numero de certificacion
    Cliente_o_Proveedor = models.ForeignKey(Cliente_Proveedor, on_delete=models.CASCADE) #llave foranea al cliente al que corresponde la certificacion 1M
    Orden_de_Compra_Nro = models.CharField(max_length=40) #Numero de OC de la certificacion
    Observaciones = models.TextField(max_length=30, blank=True) #comentarios adicionales de la certificacion
    Estados = (("PREPARANDO CERTIFICACION", "PREPARANDO CERTIFICACION"),
               ("FIRMADO", "FIRMADO"),
               ("FACTURADO", "FACTURADO"),
               ("COBRADO", "COBRADO")) #posibles estados de la certificacion
    Sistemas = (("CALDERA", "CALDERA"),
                ("ENFRIAMIENTO", "ENFRIAMIENTO"),
                ("CALDERA/ENFRIAMIENTO", "CALDERA/ENFRIAMIENTO")) #sistemas al que pertenece la certificacion
    Estado = models.CharField(max_length=40, blank=True, choices=Estados)
    Sistema = models.CharField(max_length=20, blank=True, choices=Sistemas)
    remito = models.ManyToManyField(Remito, help_text="Elegir mas de uno manteniendo apretado Ctrl") #relacion mucho a muchos con los remitos. 1 Certificacion puede tener muchos remitos y visceversa

    #metodo que define la representacion de la certificacion
    def __str__(self):  # retorna los strings de:

        return 'id: {} , Cliente: {} , ' \
               'Numero de Certificacion: {}, Fecha: {}, remitos: {} '.format(self.id,
                                                                                                    self.Cliente_o_Proveedor,
                                                                                                    self.Numero,
                                                                                                    self.Fecha,
                                                                                                    self.remito)

    #Clase que define el orden de display de los objectos de la clase
    class Meta:
        ordering = ['-Fecha']


#####------------------MOVIMIENTOS-----------------#####


class Movimientos(models.Model):
    # Modelo que define a los movimientos.
    tipos = (("Ingreso", "Ingreso"), ("Egreso", "Egreso"))  # Posiblidades del tipo de movimiento
    tipo = models.CharField(max_length=20, blank=True, choices=tipos) #campo que representa el tipo de movimiento
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE) #llave foranea al producto
    unidad = models.IntegerField() #numero de unidades en este movimiento
    Cantidad = models.IntegerField(editable=False) #es la cantidad en kg del movimiento ==> cantidad = envase del producto * unidades del movimiento

    Remito = models.ForeignKey(Remito, on_delete=models.CASCADE)

    #Metodo que retorna los strings de la clase Movimientos
    def __str__(self):
        return ' tipo: {} , Producto: {}, Unidades: {}, '.format(self.tipo, self.producto, self.unidad)

    # Clase que define el orden de display de los objectos de la clase Movimientos
    class Meta:
        ordering = ['-id']



    def save(self, *args, **kwargs):
        #	Metodo que guarda la cantidad del producto
        self.Cantidad = self.producto.envase * self.unidad
        super().save(*args, **kwargs)


#########--------------------------SEÑALES------------------------------#########

# Señal que actualiza el stock cuando se crea un  nuevo movimiento

@receiver(pre_save, sender=Movimientos, dispatch_uid="actualizar_stock_producto")
def update_stock(sender, instance, **kwargs):
    #
    movimiento = Movimientos.objects.filter(id=instance.id).exists()
    if (movimiento == False):
        #
        if (instance.tipo == "Ingreso"):
            instance.producto.stock += instance.unidad
            instance.producto.save()
        #
        else:
            #
            instance.producto.stock -= instance.unidad
            instance.producto.save()
    else:
        pass


#####------------------------------------------------------------------############
# Señal que actualiza el stock cuando se elimina un movimiento

@receiver(post_delete, sender=Movimientos, dispatch_uid="actualizar_stock_producto")
def update_stock_eliminado(sender, instance, **kwargs):
    if (instance.tipo == "Ingreso"):
        instance.producto.stock -= instance.unidad
        instance.producto.save()
    else:

        instance.producto.stock += instance.unidad
        instance.producto.save()
