from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Product(models.Model):
    PAYMENT_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
    ]
    
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

    ACCOUNT_TYPE_CHOICES = [
        ('Nequi', 'Nequi'),
        ('Bancolombia', 'Bancolombia'),
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
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Describe tu producto detalladamente'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad',
        help_text='Debe ser mayor a 0'
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
        verbose_name='Estado'
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Ubicación',
        help_text='Lugar de entrega en el campus'
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
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name='Método de pago'
    )
    account_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Número de cuenta',
        validators=[
            RegexValidator(
                regex=r'^\d{10,20}$',
                message='Ingrese un número de cuenta válido'
            )
        ]
    )
    account_type = models.CharField(
        max_length=50,
        choices=ACCOUNT_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name='Tipo de cuenta'
    )
    qr_code = models.ImageField(
        upload_to='qr_codes/',
        blank=True,
        null=True,
        verbose_name='Código QR'
    )
    available = models.BooleanField(
        default=True,
        verbose_name='Disponible'
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Etiquetas',
        help_text='Separa las etiquetas con comas'
    )

    def clean(self):
        if self.payment_method == 'Transferencia':
            if not self.account_number:
                raise ValidationError({
                    'account_number': 'El número de cuenta es obligatorio para pagos por transferencia'
                })
            if not self.account_type:
                raise ValidationError({
                    'account_type': 'El tipo de cuenta es obligatorio para pagos por transferencia'
                })
            if not self.qr_code:
                raise ValidationError({
                    'qr_code': 'El código QR es obligatorio para pagos por transferencia'
                })
        elif self.payment_method == 'Efectivo':
            self.account_number = None
            self.account_type = None
            self.qr_code = None

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

class Comment(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        max_length=500,
        verbose_name='Comentario'
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Calificación',
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text='Calificación de 0 a 5 estrellas'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de publicación'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'Comentario de {self.user.username} en {self.product.name}'

class Favorite(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de agregado'
    )

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'

    def __str__(self):
        return f'{self.user.username} ♥ {self.product.name}'