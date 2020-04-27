from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column
from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput
from django.forms.models import inlineformset_factory

from .models import *

from crispy_forms.layout import Layout, Submit



# Form de Productos

class ProductoForm(forms.ModelForm):


    class Meta:
        model = Producto
        fields = (
            'nombre', 'envase', 'procedencia', 'stock', 'stockCritico', 'Vencimiento', 'Observaciones', 'asterisco')

        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'envase': TextInput(attrs={'class': 'form-control'}),
            'procedencia': TextInput(attrs={'class': 'form-control'}),
            'stock': TextInput(attrs={'class': 'form-control'}),
            'stockCritico': TextInput(attrs={'class': 'form-control'}),
            'Vencimiento': TextInput(attrs={'class': 'form-control', 'placeholder':'Ingresar Fecha en formato mm/dd/aa'}),
            'asterisco': forms.Select(attrs={'class': 'form-control'}),
            'Observaciones': TextInput(attrs={'class': 'form-control'}),

        }


# Form de editar Productos

class EditProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = (
            'nombre', 'envase', 'procedencia', 'stock', 'stockCritico', 'Vencimiento', 'Observaciones', 'asterisco')

        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'envase': TextInput(attrs={'class': 'form-control'}),
            'procedencia': TextInput(attrs={'class': 'form-control'}),
            'stock': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'stockCritico': TextInput(attrs={'class': 'form-control'}),
            'Vencimiento': TextInput(attrs={'class': 'form-control'}),
            'asterisco': forms.Select(attrs={'class': 'form-control'}),
            'Observaciones': TextInput(attrs={'class': 'form-control'}),

        }


# Form de Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente_Proveedor
        fields = ('tipo', 'nombre', 'direccion', 'telefono', 'e_mail')

        widgets = {

            'nombre': TextInput(attrs={'class': 'form-control'}),
            'direccion': TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'e_mail': TextInput(attrs={'class': 'form-control'}),
            'telefono': TextInput(attrs={'class': 'form-control'}),
        }

#Form de Movientos
class MovimientosForm(forms.ModelForm):
    class Meta:
        model = Movimientos
        fields = ('tipo', 'producto', 'unidad')

        widgets = {

            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'unidad': TextInput(attrs={'class': 'form-control'}),

        }


# inline formset de movimiento en remitos
MovimientosFormset = inlineformset_factory(
    Remito, Movimientos, form=MovimientosForm, fields=('tipo', 'producto', 'unidad'), extra=5, can_delete=False
)


# Form de Remito
class RemitoForm(forms.ModelForm):

    def clean_remito(self):
        Numero = self.cleaned_data['Numero']
        if Remito.objects.filter(Numero=Numero).exists():
            raise ValidationError("Ese Numero de Remito ya existe")
        return Numero

    class Meta:
        model = Remito
        fields = (
            'Numero', 'Orden_de_Compra_Nro', 'Cliente_o_Proveedor', 'Estado', 'Lote', 'Valor_Declarado', 'Flete',
            'Retira',
            'Observaciones')
        widgets = {

            'Numero': TextInput(attrs={'class': 'form-control'}),
            'Orden_de_Compra_Nro': TextInput(attrs={'class': 'form-control'}),
            'Estado': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Elegir un Cliente'}),
            'Cliente_o_Proveedor': forms.Select(attrs={'class': 'form-control'}),
            'Lote': TextInput(attrs={'class': 'form-control'}),
            'Valor_Declarado': TextInput(attrs={'class': 'form-control'}),
            'Flete': TextInput(attrs={'class': 'form-control'}),
            'Retira': TextInput(attrs={'class': 'form-control'}),
            'Observaciones': TextInput(attrs={'class': 'form-control'}),

        }


# Form de Certificaciones
class CertificacionesForm(forms.ModelForm):

    Observaciones = forms.CharField(widget=forms.TextInput(attrs={'size': '20'}))

    def __init__(self, *args, **kwargs):
        super(CertificacionesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(

            Row(
                Column('Fecha', css_class='form-group col-md-6 mb-0'),
                Column('Numero', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'Cliente_o_Proveedor',
            'Orden_de_Compra_Nro',
            'Observaciones',

            Row(
                Column('Estado', css_class='form-group col-md-4 mb-0'),
                Column('Sistema', css_class='form-group col-md-4 mb-0'),

                # Column('remito', css_class='form-group col-md-4 mb-0'),
            ),
            PrependedText('remito', ''),
            Submit('submit', 'Crear')
        )

    class Meta:
        model = Certificaciones

        fields = (
            'Fecha', 'Numero', 'Cliente_o_Proveedor', 'Orden_de_Compra_Nro', 'Observaciones', 'Estado', 'Sistema',
            'remito')

        help_texts = {

            'Fecha': 'Ingresar Fecha con Formato MM/DD/AA',
            'remito': "Elegir mas de uno manteniendo control apretado"
        }

#form de editar certificaciones
class EditCertificacionesForm(forms.ModelForm):
    class Meta:
        model = Certificaciones

        help_texts = {

            'Fecha': 'Ingresar Fecha con Formato MM/DD/AA',
            'remito': "Elegir mas de uno manteniendo control apretado"
        }

        fields = (
            'Fecha', 'Numero', 'Cliente_o_Proveedor', 'Orden_de_Compra_Nro', 'Observaciones', 'Estado', 'Sistema',
            'remito')

        widgets = {

            'Fecha': TextInput(attrs={'class': 'form-control'}),
            'Numero': TextInput(attrs={'class': 'form-control'}),
            'Cliente_o_Proveedor': forms.Select(attrs={'class': 'form-control'}),
            'Orden_de_Compra_Nro': TextInput(attrs={'class': 'form-control'}),
            'Observaciones': TextInput(attrs={'class': 'form-control'}),
            'Estado': forms.Select(attrs={'class': 'form-control'}),
            'Sistema': forms.Select(attrs={'class': 'form-control'}),
            'remito': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
