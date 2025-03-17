from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

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

    class Meta:
        verbose_name = 'Perfil de vendedor'
        verbose_name_plural = 'Perfiles de vendedores'

    def __str__(self):
        return f"Tienda de {self.store_name}"

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