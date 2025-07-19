from django.shortcuts import render, get_object_or_404, redirect
from .models import Zona
from .forms import ZonaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def lista_zonas(request):
    zonas = Zona.objects.all()
    return render(request, 'bonanza_zonas/lista_zonas.html', {'zonas': zonas})

@login_required
def crear_zona(request):
    if request.method == 'POST':
        form = ZonaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Zona creada correctamente.")
            return redirect('zonas:lista_zonas')
    else:
        form = ZonaForm()
    return render(request, 'bonanza_zonas/formulario_zona.html', {'form': form, 'titulo': 'Crear Zona'})

@login_required
def editar_zona(request, zona_id):
    zona = get_object_or_404(Zona, id=zona_id)
    if request.method == 'POST':
        form = ZonaForm(request.POST, instance=zona)
        if form.is_valid():
            form.save()
            messages.success(request, "Zona actualizada correctamente.")
            return redirect('zonas:lista_zonas')
    else:
        form = ZonaForm(instance=zona)
    return render(request, 'bonanza_zonas/formulario_zona.html', {'form': form, 'titulo': 'Editar Zona'})

@login_required
def eliminar_zona(request, zona_id):
    zona = get_object_or_404(Zona, id=zona_id)
    if request.method == 'POST':
        zona.delete()
        messages.success(request, "Zona eliminada correctamente.")
        return redirect('zonas:lista_zonas')
    return render(request, 'bonanza_zonas/zonas_confirm_delete.html', {'zona': zona})
