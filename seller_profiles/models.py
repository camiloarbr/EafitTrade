from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import re

class SellerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller_profile'
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        verbose_name='Foto de perfil',
        null=True,
        blank=True
    )
    store_name = models.CharField(
        max_length=100,
        verbose_name='Nombre de la tienda',
        help_text='Nombre que se mostrará en tu perfil de vendedor'
    )
    slogan = models.CharField(
        max_length=200,
        verbose_name='Slogan',
        help_text='Una frase corta que describa tu tienda',
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Describe tu tienda y los productos que vendes'
    )
    whatsapp = models.CharField(
        max_length=15,
        verbose_name='WhatsApp',
        help_text='Ingresa tu número de WhatsApp con código de país (ej: 573001234567)',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Perfil de vendedor'
        verbose_name_plural = 'Perfiles de vendedores'

    def __str__(self):
        return f"Tienda de {self.store_name}"

    def clean(self):
        super().clean()
        if self.whatsapp:
            # Eliminar cualquier espacio o carácter especial
            self.whatsapp = re.sub(r'[^0-9]', '', self.whatsapp)
            
            # Verificar formato
            if not re.match(r'^57[3]\d{9}$', self.whatsapp):
                raise ValidationError({
                    'whatsapp': 'El número debe comenzar con 57 seguido de un 3 y 9 dígitos más.'
                })

    def get_whatsapp_link(self):
        if not self.whatsapp:
            return None
        return f"https://wa.me/{self.whatsapp}"

class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
    ]

    profile = models.ForeignKey(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    day = models.CharField(
        max_length=20,
        choices=DAYS_OF_WEEK,
        verbose_name='Día'
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Disponible'
    )
    start_time = models.TimeField(
        verbose_name='Hora de inicio',
        null=True,
        blank=True
    )
    end_time = models.TimeField(
        verbose_name='Hora de cierre',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['day']
        unique_together = ['profile', 'day']

    def clean(self):
        if self.is_available:
            if not self.start_time or not self.end_time:
                raise ValidationError('Debe especificar hora de inicio y cierre cuando el día está disponible')
            if self.start_time >= self.end_time:
                raise ValidationError('La hora de inicio debe ser anterior a la hora de cierre')
        else:
            self.start_time = None
            self.end_time = None

    def __str__(self):
        if not self.is_available:
            return f"{self.day}: No disponible"
        return f"{self.day}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"