from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .models import Product, Comment, Favorite
from seller_profiles.models import SellerProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm, CommentForm, CustomUserCreationForm
from django.views.decorators.http import require_POST
from django.conf import settings
import urllib.parse
from django.http import JsonResponse
from seller_profiles.models import SellerProfile, ProfileClick
from django.contrib.auth.models import User

def home(request):
    products = Product.objects.all()
    
    # Búsqueda por nombre
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Filtro por categoría
    category = request.GET.get('category', '')
    if category:
        products = products.filter(category=category)
    
    # Filtro por tipo de comida
    food_type = request.GET.get('food_type', '')
    if category == 'Comida' and food_type:
        products = products.filter(food_type=food_type)
    
    # Filtro por rango de precios
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    if min_price:
        try:
            min_price = float(min_price)
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass
    
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass
    
    # Ordenar por fecha de publicación
    products = products.order_by('-published_at')
    
    # Obtener favoritos del usuario
    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    
    context = {
        'products': products,
        'user_favorites': user_favorites,
        'search_query': search_query,
        'selected_category': category,
        'selected_food_type': food_type,
        'min_price': min_price,
        'max_price': max_price,
        'categories': Product.CATEGORY_CHOICES,
        'food_types': Product.FOOD_TYPE_CHOICES,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'products/home.html', context)

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

@login_required
@require_POST
def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CommentForm(request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.product = product
        comment.user = request.user
        comment.save()
        messages.success(request, '¡Comentario agregado exitosamente!')
    else:
        messages.error(request, 'Error al agregar el comentario. Por favor, inténtalo de nuevo.')
    
    return redirect('product_detail', product_id=product_id)

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user != request.user:
        messages.error(request, 'No tienes permiso para eliminar este comentario.')
        return redirect('product_detail', product_id=comment.product.id)
    
    product_id = comment.product.id
    comment.delete()
    messages.success(request, 'Comentario eliminado exitosamente.')
    
    return redirect('product_detail', product_id=product_id)

@login_required
@require_POST
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    
    return JsonResponse({'status': 'added'})

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'products/favorites.html', {
        'favorites': favorites
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments.all().order_by('-created_at')
    comment_form = CommentForm() if request.user.is_authenticated else None
    
    # Verify if product is in favorites
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    
    # Get seller profile and prepare WhatsApp link if available
    seller_profile = None
    whatsapp_link = None
    try:
        seller_profile = product.seller.seller_profile
        if seller_profile and seller_profile.whatsapp:
            # Usar el método get_whatsapp_link del modelo SellerProfile
            whatsapp_link = seller_profile.get_whatsapp_link(product.name)
    except SellerProfile.DoesNotExist:
        pass
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'comments': comments,
        'comment_form': comment_form,
        'is_favorite': is_favorite,
        'seller_profile': seller_profile,
        'whatsapp_link': whatsapp_link
    })

def register_whatsapp_click(request):
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        try:
            profile = SellerProfile.objects.get(id=profile_id)
            ProfileClick.objects.create(
                profile=profile,
                user=request.user if request.user.is_authenticated else None
            )
            return JsonResponse({'success': True})
        except SellerProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Perfil no encontrado'}, status=404)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


# Create your views here.