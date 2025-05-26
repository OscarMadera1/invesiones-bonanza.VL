from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import Producto, Categoria, Municipio, Bodega, InventarioBodega
from .forms import (
    ProductoForm, CategoriaForm, MunicipioForm,
    BodegaForm, InventarioBodegaForm
)

# --- Productos ---
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'bonanza_inventario/productos/lista.html', {'productos': productos})

def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto creado exitosamente.')
        return redirect('lista_productos')
    return render(request, 'bonanza_inventario/productos/formulario.html', {'form': form})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    form = ProductoForm(request.POST or None, instance=producto)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('lista_productos')
    return render(request, 'bonanza_inventario/productos/formulario.html', {'form': form})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado correctamente.')
    return redirect('lista_productos')


# --- Categorías ---
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'bonanza_inventario/categorias/lista.html', {'categorias': categorias})

def crear_categoria(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada exitosamente.')
        return redirect('lista_categorias')
    return render(request, 'bonanza_inventario/categorias/formulario.html', {'form': form})

def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría actualizada correctamente.')
        return redirect('lista_categorias')
    return render(request, 'bonanza_inventario/categorias/formulario.html', {'form': form})

def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    messages.success(request, 'Categoría eliminada correctamente.')
    return redirect('lista_categorias')


# --- Municipios ---
def lista_municipios(request):
    municipios = Municipio.objects.all()
    return render(request, 'bonanza_inventario/municipios/lista.html', {'municipios': municipios})

def crear_municipio(request):
    form = MunicipioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Municipio creado exitosamente.')
        return redirect('lista_municipios')
    return render(request, 'bonanza_inventario/municipios/formulario.html', {'form': form})

def editar_municipio(request, municipio_id):
    municipio = get_object_or_404(Municipio, id=municipio_id)
    form = MunicipioForm(request.POST or None, instance=municipio)
    if form.is_valid():
        form.save()
        messages.success(request, 'Municipio actualizado correctamente.')
        return redirect('lista_municipios')
    return render(request, 'bonanza_inventario/municipios/formulario.html', {'form': form})

def eliminar_municipio(request, municipio_id):
    municipio = get_object_or_404(Municipio, id=municipio_id)
    municipio.delete()
    messages.success(request, 'Municipio eliminado correctamente.')
    return redirect('lista_municipios')


# --- Bodegas ---
def lista_bodegas(request):
    bodegas = Bodega.objects.select_related('municipio').all()
    return render(request, 'bonanza_inventario/bodegas/lista.html', {'bodegas': bodegas})

def crear_bodega(request):
    form = BodegaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Bodega creada exitosamente.')
        return redirect('lista_bodegas')
    return render(request, 'bonanza_inventario/bodegas/formulario.html', {'form': form})

def editar_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)
    form = BodegaForm(request.POST or None, instance=bodega)
    if form.is_valid():
        form.save()
        messages.success(request, 'Bodega actualizada correctamente.')
        return redirect('lista_bodegas')
    return render(request, 'bonanza_inventario/bodegas/formulario.html', {'form': form})

def eliminar_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)
    bodega.delete()
    messages.success(request, 'Bodega eliminada correctamente.')
    return redirect('lista_bodegas')


# --- Inventario por bodega ---
def inventario_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)
    inventario = InventarioBodega.objects.filter(bodega=bodega).select_related('producto')
    return render(request, 'bonanza_inventario/inventario/lista.html', {
        'bodega': bodega,
        'inventario': inventario
    })

def crear_inventario_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)
    form = InventarioBodegaForm(request.POST or None)
    if form.is_valid():
        inventario_item = form.save(commit=False)
        inventario_item.bodega = bodega
        inventario_item.save()
        messages.success(request, 'Inventario agregado correctamente.')
        return redirect('inventario_bodega', bodega_id=bodega.id)
    return render(request, 'bonanza_inventario/inventario/formulario.html', {'form': form, 'bodega': bodega})

def editar_inventario_bodega(request, bodega_id, item_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)
    item = get_object_or_404(InventarioBodega, id=item_id, bodega=bodega)
    form = InventarioBodegaForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.success(request, 'Inventario actualizado correctamente.')
        return redirect('inventario_bodega', bodega_id=bodega.id)
    return render(request, 'bonanza_inventario/inventario/formulario.html', {'form': form, 'bodega': bodega})

def eliminar_inventario_bodega(request, bodega_id, item_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)
    item = get_object_or_404(InventarioBodega, id=item_id, bodega=bodega)
    item.delete()
    messages.success(request, 'Inventario eliminado correctamente.')
    return redirect('inventario_bodega', bodega_id=bodega.id)
