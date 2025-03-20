"""
URL configuration for eafit_trade project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from products import views as products_views
from seller_profiles import views as profile_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', products_views.home, name='home'),
    path('add-product/', products_views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', products_views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', products_views.delete_product, name='delete_product'),
    
    # URLs para la autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', products_views.register, name='register'),
    
    # URLs para restablecimiento de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # URLs para comentarios
    path('comment/add/<int:product_id>/', products_views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', products_views.delete_comment, name='delete_comment'),
    
    # URLs para favoritos
    path('favorite/toggle/<int:product_id>/', products_views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', products_views.favorites_list, name='favorites_list'),
    
    # Product detail URL
    path('product/<int:product_id>/', products_views.product_detail, name='product_detail'),
    
    # URLs para perfiles de vendedor
    path('profile/', profile_views.view_profile, name='view_profile'),
    path('profile/create/', profile_views.create_profile, name='create_profile'),
    path('profile/edit/', profile_views.edit_profile, name='edit_profile'),
    path('seller/<int:user_id>/', profile_views.public_profile, name='public_profile'),
    path('sellers/', profile_views.seller_list, name='seller_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)