from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente
from .forms import ClienteForm

def cliente_list(request):
    clientes = Cliente.objects.select_related('zona', 'municipio')
    return render(request, 'bonanza_clientes/cliente_list.html', {'clientes': clientes})

def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('bonanza_clientes:cliente_list')
    return render(request, 'bonanza_clientes/cliente_form.html', {'form': form})

def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect('bonanza_clientes:cliente_list')
    return render(request, 'bonanza_clientes/cliente_form.html', {'form': form})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('bonanza_clientes:cliente_list')
    return render(request, 'bonanza_clientes/cliente_confirm_delete.html', {'cliente': cliente})
