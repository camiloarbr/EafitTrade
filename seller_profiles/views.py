from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SellerProfile, Schedule
from .forms import SellerProfileForm, ScheduleInlineFormSet
from django.db import transaction
from django.contrib.auth.models import User
from django.db.models import Q
from products.models import Product
from .models import SellerProfile, ProfileClick

# Create your views here.

@login_required
def view_profile(request):
    try:
        profile = request.user.seller_profile
        return render(request, 'seller_profiles/view_profile.html', {'profile': profile})
    except SellerProfile.DoesNotExist:
        messages.warning(request, 'Necesitas crear tu perfil de vendedor primero.')
        return redirect('create_profile')

@login_required
def create_profile(request):
    if hasattr(request.user, 'seller_profile'):
        return redirect('edit_profile')

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, request.FILES)
        schedule_formset = ScheduleInlineFormSet(request.POST)
        
        if form.is_valid() and schedule_formset.is_valid():
            with transaction.atomic():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                
                schedule_formset.instance = profile
                schedule_formset.save()
                
                messages.success(request, '¡Perfil creado exitosamente!')
                return redirect('view_profile')
    else:
        form = SellerProfileForm()
        schedule_formset = ScheduleInlineFormSet()
    
    return render(request, 'seller_profiles/create_profile.html', {
        'form': form,
        'schedule_formset': schedule_formset
    })

@login_required
def edit_profile(request):
    profile = get_object_or_404(SellerProfile, user=request.user)
    
    if request.method == 'POST':
        form = SellerProfileForm(request.POST, request.FILES, instance=profile)
        schedule_formset = ScheduleInlineFormSet(request.POST, instance=profile)
        
        if form.is_valid() and schedule_formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el perfil
                    profile = form.save()
                    
                    # Guardar los horarios
                    schedules = schedule_formset.save(commit=False)
                    for schedule in schedules:
                        if not schedule.is_available:
                            schedule.start_time = None
                            schedule.end_time = None
                        schedule.save()
                    
                    messages.success(request, '¡Perfil actualizado exitosamente!')
                    return redirect('view_profile')
            except Exception as e:
                messages.error(request, f'Error al actualizar el perfil: {str(e)}')
    else:
        form = SellerProfileForm(instance=profile)
        schedule_formset = ScheduleInlineFormSet(instance=profile)
    
    return render(request, 'seller_profiles/edit_profile.html', {
        'form': form,
        'schedule_formset': schedule_formset,
        'profile': profile
    })

def has_seller_profile(user):
    return hasattr(user, 'seller_profile')

from seller_profiles.models import SellerProfile

def public_profile(request, user_id):
    seller = get_object_or_404(User, id=user_id)
    try:
        profile = seller.seller_profile

        # Redirigir si es su propio perfil
        if request.user == seller:
            return redirect('view_profile')

        # Obtener cantidad de clics
        total_clicks = profile.clicks.count()

        # Puedes también guardar un nuevo clic si quieres rastrear vistas de perfil
        ProfileClick.objects.create(profile=profile, user=request.user if request.user.is_authenticated else None)

        return render(request, 'seller_profiles/public_profile.html', {
            'profile': profile,
            'total_clicks': total_clicks
        })

    except SellerProfile.DoesNotExist:
        if request.user == seller:
            messages.warning(request, 'Necesitas crear tu perfil de vendedor primero.')
            return redirect('create_profile')
        messages.error(request, 'Este vendedor aún no ha creado su perfil.')
        return redirect('home')


# Actualizar la vista del producto para incluir el perfil del vendedor
@login_required
def add_product(request):
    # Verificar si el usuario tiene perfil de vendedor
    if not hasattr(request.user, 'seller_profile'):
        messages.warning(request, 'Necesitas crear un perfil de vendedor antes de publicar productos.')
        return redirect('create_profile')
    # ... resto del código existente ...

def seller_list(request):
    # Iniciar con todos los vendedores
    sellers = SellerProfile.objects.all()
    
    # Obtener parámetros de búsqueda
    search_query = request.GET.get('search', '').strip()
    selected_categories = request.GET.getlist('categories')
    
    # Aplicar filtro de búsqueda por nombre
    if search_query:
        sellers = sellers.filter(
            Q(store_name__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    # Aplicar filtro por categorías
    if selected_categories:
        # Filtrar vendedores que tengan productos en cualquiera de las categorías seleccionadas
        sellers = sellers.filter(
            user__products__category__in=selected_categories
        ).distinct()
    
    # Preparar los datos de los vendedores con sus categorías
    sellers_data = []
    for seller in sellers:
        # Obtener categorías únicas de los productos del vendedor
        seller_categories = seller.user.products.values_list(
            'category', flat=True
        ).distinct()
        
        sellers_data.append({
            'profile': seller,
            'categories': list(seller_categories)
        })
    
    # Preparar las categorías para el filtro
    all_categories = [choice[0] for choice in Product.CATEGORY_CHOICES]
    
    context = {
        'sellers': sellers_data,
        'all_categories': all_categories,
        'search_query': search_query,
        'selected_categories': selected_categories,
    }
    
    return render(request, 'seller_profiles/seller_list.html', context)
