from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .forms import *
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test


##########___Funcion para chequear a que grupo pertenece________#########

def is_member(user):
    return user.groups.filter(name='Change').exists()


####Vistas de pagina web##########

@login_required(login_url='/admin/login/?next=/admin/')
def index(request):
    return render(request, 'index.html')


####################--------------------VISTAS PARA MOSTRAR OBJECTOS----------------------------###################

# display products
@login_required(login_url='/admin/login/?next=/admin/')
def display_products(request):
    items = Producto.objects.all()
    context = {
        'items': items,
        'header': 'Productos',
    }
    return render(request, 'display_products.html', context)  # 3 arguments


# display clients
@login_required(login_url='/admin/login/?next=/admin/')
def display_clients(request):
    items = Cliente_Proveedor.objects.all()
    context = {
        'items': items,
        'header': 'Clientes_Proveedores',
    }
    return render(request, 'display_clients.html', context)  # 3 arguments


# display movimientos
@login_required(login_url='/admin/login/?next=/admin/')
def display_movimientos(request):
    items = Movimientos.objects.all()
    context = {
        'items': items,
        'header': 'Movimientos',
    }
    return render(request, 'display_movimientos.html', context)


# display remitos
@login_required(login_url='/admin/login/?next=/admin/')
def display_remitos(request):
    items = Remito.objects.all()
    context = {
        'items': items,
        'header': 'Remito',
    }
    return render(request, 'display_remitos.html', context)

    # display certificaciones
@login_required(login_url='/admin/login/?next=/admin/')
def display_certificaciones(request):
    items = Certificaciones.objects.all()
    context = {
        'items': items,
        'header': 'Remito',
    }
    return render(request, 'display_certificaciones.html', context)


##################___________________________VISTAS PARA AÑADIR OBJETOS________________________________############################

# add products
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def add_products(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('display_products')

    else:
        form = ProductoForm()
    return render(request, "add_products.html", {'form': form})


# add clients
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def add_clients(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('display_clients')

    else:
        form = ClienteForm()
    return render(request, "add_clients.html", {'form': form})


# add remito:
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test, name='dispatch')
class RemitoCreate(CreateView):
    model = Remito
    template_name = 'add_remitos.html'
    form_class = RemitoForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(RemitoCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['movimientos'] = MovimientosFormset(self.request.POST)
        else:
            data['movimientos'] = MovimientosFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        movimientos = context['movimientos']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if movimientos.is_valid():
                movimientos.instance = self.object
                movimientos.save()
        return super(RemitoCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('display_remitos')


# add certificacion:

@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def add_certificaciones(request):
    if request.method == "POST":
        form = CertificacionesForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('display_certificaciones')

    else:
        form = CertificacionesForm()
    return render(request, "add_certificaciones.html", {'form': form})


##############_____________________________VISTAS PARA EDITAR OBJETOS_________________________________######################

# edit products
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def edit_producto(request, pk):
    item = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = AddProductoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('display_products')
    else:
        form = AddProductoForm(instance=item)

    return render(request, 'edit_producto.html', {'form': form})


# edit clients
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def edit_clients(request, pk):
    item = get_object_or_404(Cliente_Proveedor, pk=pk)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('display_clients')
    else:
        form = ClienteForm(instance=item)

    return render(request, 'edit_clients.html', {'form': form})


# edit remitos
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def edit_remito(request, pk):
    item = get_object_or_404(Remito, pk=pk)

    if request.method == "POST":
        form = RemitoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('display_remitos')
    else:
        form = RemitoForm(instance=item)

    return render(request, 'edit_remito.html', {'form': form})


# edit certificaciones
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def edit_certificacion(request, pk):
    item = get_object_or_404(Certificaciones, pk=pk)

    if request.method == "POST":
        form = EditCertificacionesForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('display_certificaciones')
    else:
        form = EditCertificacionesForm(instance=item)

    return render(request, 'edit_certificacion.html', {'form': form})


########___________________________VISTAS PARA ELIMINAR OBJETOS_____________________#######

# eliminar productos
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def delete_producto(request, pk):
    Producto.objects.filter(id=pk).delete()
    items = Producto.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'display_products.html', context)


# eliminar clientes
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def delete_clients(request, pk):
    Cliente_Proveedor.objects.filter(id=pk).delete()

    items = Cliente_Proveedor.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'display_clients.html', context)


# eliminar remitos
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def delete_remito(request, pk):
    Remito.objects.filter(id=pk).delete()

    items = Remito.objects.all()

    context = {
        'items': items,

    }

    return render(request, 'display_remitos.html', context)


# eliminar Certificaciones
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def delete_certificacion(request, pk):
    Certificaciones.objects.filter(id=pk).delete()

    items = Certificaciones.objects.all()

    context = {
        'items': items,

    }

    return render(request, 'display_certificaciones.html', context)


######################-----------IMPRESION DEL REMITO--------------------#############################
@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def imprimir(request, pk):
    item = get_object_or_404(Remito, pk=pk)

    movimientos = item.movimientos_set.all()

    bultos = movimientos.aggregate(Sum('unidad'))

    context = {

        'item': item,
        'movimientos': movimientos,
        'bultos': bultos,
    }

    return render(request, 'imprimir_remitos.html', context)


####################-------------MOSTRAR REMITOS DE CERTIFICACIONES-------------#########################

@login_required(login_url='/admin/login/?next=/admin/')
@user_passes_test(is_member, login_url='index')
def mostrar_remitos_certificacion(request, pk):
    item = get_object_or_404(Certificaciones, pk=pk)

    remitos = item.remito.all()

    movimientos = Movimientos.objects.filter(Remito__certificaciones__id=item.id)

    context = {

        'item': item,
        'remitos': remitos,
        'movimientos': movimientos,

    }

    return render(request, 'mostrar_remitos_certificacion.html', context)
