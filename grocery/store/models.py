from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва')
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, default='🛒', verbose_name='Іконка')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категорія'
    )
    name = models.CharField(max_length=200, verbose_name='Назва')
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна (грн)')
    unit = models.CharField(max_length=20, default='шт', verbose_name='Одиниця виміру')
    is_available = models.BooleanField(default=True, verbose_name='В наявності')
    is_featured = models.BooleanField(default=False, verbose_name='Популярний')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нове'),
        ('processing', 'Обробляється'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]

    full_name = models.CharField(max_length=150, verbose_name="Повне ім'я")
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    address = models.TextField(verbose_name='Адреса доставки')
    notes = models.TextField(blank=True, verbose_name='Примітки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Сума')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'Замовлення #{self.pk} — {self.full_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Замовлення'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна на момент замовлення')

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    def subtotal(self):
        return self.price * self.quantity
