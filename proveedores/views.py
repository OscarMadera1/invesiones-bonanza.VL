from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from .forms import ProveedorForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def lista_provedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'bonanza_proveedores/proveedor_list.html', {'proveedores': proveedores})

@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "proveedor creado correctamente.")
            return redirect('proveedores:lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'bonanza_proveedores/proveedor_form.html', {'form': form, 'titulo': 'Crear proveedor'})

def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado correctamente.")
            return redirect('proveedores:lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'bonanza_proveedores/proveedor_form.html', {'form': form, 'titulo': 'Editar Proveedor'})

@login_required
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect('proveedores:lista_proveedores')
    return render(request, 'bonanza_proveedores/proveedor_confirm_delete.html', {'proveedor': proveedor})
