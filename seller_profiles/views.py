from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SellerProfile, Schedule
from .forms import SellerProfileForm, ScheduleInlineFormSet
from django.db import transaction

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
