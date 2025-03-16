from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Comida', 'Comida'),
        ('Ropa', 'Ropa'),
        ('Tecnología', 'Tecnología'),
        ('Libros', 'Libros'),
        ('Otros', 'Otros'),
    ]
    
    CONDITION_CHOICES = [
        ('Nuevo', 'Nuevo'),
        ('Usado', 'Usado'),
        ('Buen estado', 'Buen estado'),
    ]
    
    FOOD_TYPE_CHOICES = [
        ('Panadería', 'Panadería'),
        ('Galletas', 'Galletas'),
        ('Repostería', 'Repostería'),
        ('Frutas', 'Frutas'),
        ('Frituras', 'Frituras'),
        ('Dulces', 'Dulces'),
        ('Helados', 'Helados'),
        ('Snacks', 'Snacks'),
        ('Comida rápida', 'Comida rápida'),
        ('Otros', 'Otros'),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name='Nombre',
        help_text='Nombre del producto'
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name='Categoría'
    )
    food_type = models.CharField(
        max_length=50,
        choices=FOOD_TYPE_CHOICES,
        verbose_name='Tipo de Comida',
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Describe tu producto detalladamente'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Precio',
        help_text='Precio en pesos colombianos'
    )
    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha de publicación'
    )
    condition = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        verbose_name='Estado',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Imagen',
        help_text='Imagen del producto'
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Vendedor',
        related_name='products'
    )
    available = models.BooleanField(
        default=True,
        verbose_name='Disponible'
    )

    def clean(self):
        # Lógica de validación
        if self.category == 'Comida':
            self.condition = None  # No aplica estado para comida
        else:
            self.food_type = None  # No aplica tipo de comida para otras categorías

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['available']),
        ]

    @property
    def average_rating(self):
        comments = self.comments.all()
        if not comments:
            return 0
        return round(sum(comment.rating for comment in comments) / len(comments), 1)

    @property
    def total_ratings(self):
        return self.comments.count()
    
    # También mantener el resto de las clases Comment y Favorite sin cambios