from django.shortcuts import render, get_object_or_404, redirect
from .models import Empleado
from .forms import EmpleadoForm

def empleado_list(request):
    empleados = Empleado.objects.all()
    return render(request, 'bonanza_empleados/empleado_list.html', {'empleados': empleados})

def empleado_create(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empleado_list')
    else:
        form = EmpleadoForm()
    return render(request, 'bonanza_empleados/empleado_form.html', {'form': form})

def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    form = EmpleadoForm(request.POST or None, instance=empleado)
    if form.is_valid():
        form.save()
        return redirect('empleado_list')
    return render(request, 'bonanza_empleados/empleado_form.html', {'form': form})

def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        return redirect('empleado_list')
    return render(request, 'bonanza_empleados/empleado_confirm_delete.html', {'empleado': empleado})
