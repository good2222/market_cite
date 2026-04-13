from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва')),
                ('slug', models.SlugField(unique=True)),
                ('icon', models.CharField(default='🛒', max_length=10, verbose_name='Іконка')),
            ],
            options={'verbose_name': 'Категорія', 'verbose_name_plural': 'Категорії'},
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150, verbose_name="Повне ім'я")),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('email', models.EmailField(verbose_name='Email')),
                ('address', models.TextField(verbose_name='Адреса доставки')),
                ('notes', models.TextField(blank=True, verbose_name='Примітки')),
                ('status', models.CharField(choices=[('new', 'Нове'), ('processing', 'Обробляється'), ('delivered', 'Доставлено'), ('cancelled', 'Скасовано')], default='new', max_length=20, verbose_name='Статус')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сума')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
            ],
            options={'verbose_name': 'Замовлення', 'verbose_name_plural': 'Замовлення', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Ціна (грн)')),
                ('unit', models.CharField(default='шт', max_length=20, verbose_name='Одиниця виміру')),
                ('is_available', models.BooleanField(default=True, verbose_name='В наявності')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Популярний')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.category', verbose_name='Категорія')),
            ],
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товари', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Кількість')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Ціна на момент замовлення')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.order', verbose_name='Замовлення')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Товар')),
            ],
            options={'verbose_name': 'Позиція замовлення', 'verbose_name_plural': 'Позиції замовлення'},
        ),
    ]
