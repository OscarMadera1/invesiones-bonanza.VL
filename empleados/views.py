from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado
from .forms import EmpleadoForm

def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'bonanza_empleados/lista_empleados.html', {'empleados': empleados})

def crear_empleado(request):
    form = EmpleadoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('empleados:lista_empleados')
    return render(request, 'bonanza_empleados/form_empleado.html', {'form': form})

def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    form = EmpleadoForm(request.POST or None, instance=empleado)
    if form.is_valid():
        form.save()
        return redirect('empleados:lista_empleados')
    return render(request, 'bonanza_empleados/form_empleado.html', {'form': form})

def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    if request.method == 'POST':
        empleado.delete()
        return redirect('empleados:lista_empleados')
    return render(request, 'bonanza_empleados/confirmar_eliminar.html', {'obj': empleado})
