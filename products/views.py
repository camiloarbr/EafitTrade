from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm

def home(request):
    products = Product.objects.filter(available=True).order_by('-published_at')
    return render(request, 'products/home.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, '¡Producto agregado exitosamente!')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProductForm()
    
    return render(request, 'products/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Verificar que el usuario sea el dueño del producto
    if product.seller != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este producto.")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto actualizado exitosamente!')
            return redirect('home')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/edit_product.html', {
        'form': form,
        'product': product
    })

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Verificar que el usuario sea el dueño del producto
    if product.seller != request.user:
        return HttpResponseForbidden("No tienes permiso para eliminar este producto.")
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, '¡Producto eliminado exitosamente!')
        return redirect('home')
    
    return render(request, 'products/confirm_delete.html', {'product': product})

# Create your views here.