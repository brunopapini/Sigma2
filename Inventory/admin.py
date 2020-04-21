from django.contrib import admin
#import models
from .models import Producto, Certificaciones, Cliente_Proveedor, Movimientos, Remito



#import resource for Export_import excel.
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields

#tools for inlines
from django.shortcuts import redirect



########---------------CLASE CLIENTE PROVEEDOR DE ADMIN------------#########
@admin.register(Cliente_Proveedor)
class Cliente_ProveedorAdmin(admin.ModelAdmin):
    search_fields = ['nombre']

#######---------------CLASE PRODUCTO DE ADMIN----------------------########
@admin.register(Producto)
class ViewAdminProducto(ImportExportModelAdmin):
    fields= ('nombre',
             'envase',
             'procedencia',
             'stock',
             'stockCritico',
             'Observaciones',
             'Vencimiento',
             'asterisco')
    search_fields = ['producto', 'stock']
    readonly_fields = ['stock']

class MovimientosResource(resources.ModelResource):
### CLASE PARA EXPORTAR Movimientos Model Resource ####

   class Meta:
        model = Movimientos
        fields = ('tipo',
                  'producto__producto',
                  'unidad',
                  'Cantidad',
                  'Remito__Fecha',
                  'Remito__Numero',
                  'Remito__Orden_de_Compra_Nro',
                  'Remito__Estado',
                  'Remito__Cliente_o_Proveedor__nombre',
                  'Remito__Lote',
                  'Remito__Valor_Declarado',
                  'Remito__Flete',
                  'Remito__Retira',
                  'Remito__Observaciones')

@admin.register(Movimientos)



class ViewAdminMovimientos(ImportExportModelAdmin):

    def has_add_permission(self,request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    fields = ('tipo', 'producto', 'unidad')
    resource_class = MovimientosResource
    search_fields = ['producto__producto','tipo','unidad']


class MovimientosInline(admin.TabularInline):

    model = Movimientos
    extra = 0


    def has_delete_permission(self, request, obj=None):
        return False


############----------------------------CLASE REMITOS ADMIN-------------------##########


#######################-----------clase Remitos para exportar----------##################
class RemitosResource(resources.ModelResource):


    class Meta:
        model = Remito

        #aqui registro los movimientos y linkeo la opcion de exportacion con la clase definida arriba Movimientos Resource.
        fields = ('Fecha',
                  'Numero',
                  'Orden_de_Compra_Nro',
                  'Estado',
                  'Cliente_o_Proveedor__nombre',
                  'Lote',
                  'Valor_Declarado',
                  'Flete',
                  'Retira',
                  'Observaciones')#'Cliente_o_Proveedor__nombre', ,'Fecha','Remito','Lote','Valor_Declarado','Flete','Retira','Observaciones')

##################---------------Clase Admin de Remitos-------------######################
@admin.register(Remito)
class ViewAdminRemito(ImportExportModelAdmin):

    resource_class = RemitosResource

    fields = ('Numero',
              'Orden_de_Compra_Nro',
              'Estado',
              'Cliente_o_Proveedor',
              'Lote',
              'Valor_Declarado',
              'Flete','Retira','Observaciones')

    search_fields = ['Numero',
                     'Orden_de_Compra_Nro',
                     'Estado',
                     'Cliente_o_Proveedor__nombre',
                     'Lote',
                     'Valor_Declarado',
                     'Flete',
                     'Retira',
                     'Observaciones']

    inlines = [
       MovimientosInline,
    ]



    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('Numero',
                                           'Orden_de_Compra_Nro',
                                           'Cliente_o_Proveedor',
                                           'Lote',
                                           'Valor_Declarado',
                                           'Flete',
                                           'Retira',
                                           'Observaciones')
        return self.readonly_fields



##############--------------------------ADMIN CERTIFICACIONES-----------------------######################

########----------CLASE RESOURCE PARA EXPORTAR CERTIFICACIONES---------------##########

class CertificacionesResource(resources.ModelResource):


	class Meta:

		model = Certificaciones

		fields = ('Fecha',
                  'Numero',
                  'Orden_de_Compra_Nro',
                  'Estado',
                  'Cliente_o_Proveedor__nombre',
                  'Observaciones',
                  'Sistema',
                  'remito')

#######---------------------------------------------------------#########

#######----------CLASE ADMIN DE CERTIFICACIONES-----------------#########


@admin.register(Certificaciones)
class ViewAdminCertificaciones(ImportExportModelAdmin):

    resource_class = CertificacionesResource


    search_fields = ['Fecha',
                     'Numero',
                     'Orden_de_Compra_Nro',
                     'Estado',
                     'Cliente_o_Proveedor__nombre',
                     'Observaciones','Sistema']


######____________________________________CUSTOMIZACION ADMIN_____________________________######


admin.site.site_header = ' ADMINISTRACION DE SIGMA'