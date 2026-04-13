# FreshMart — Магазин продуктів

Django-проект інтернет-магазину продуктів харчування.

## Структура

```
grocery/
├── manage.py
├── db.sqlite3           # створюється автоматично
├── market/              # головний пакет (налаштування)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── static/css/style.css
│   └── templates/
│       ├── base.html
│       └── store/
│           ├── product_list.html
│           ├── cart.html
│           ├── checkout.html
│           └── order_success.html
└── store/               # додаток магазину
    ├── models.py        # Category, Product, Order, OrderItem
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── migrations/
    └── fixtures/
        └── initial_data.json   # тестові дані (23 товари)
```

## Встановлення та запуск

### 1. Встановити залежності

```bash
pip install django
```

### 2. Перейти в папку проекту

```bash
cd grocery
```

### 3. Застосувати міграції (створити базу даних)

```bash
python manage.py migrate
```

### 4. Завантажити тестові дані

```bash
python manage.py loaddata store/fixtures/initial_data.json
```

### 5. Створити адміна (необов'язково)

```bash
python manage.py createsuperuser
```

### 6. Запустити сервер

```bash
python manage.py runserver
```

Відкрити браузер: **http://127.0.0.1:8000/**

Адмін-панель: **http://127.0.0.1:8000/admin/**

## Функціонал

- Головна сторінка з каталогом товарів
- Фільтрація за категоріями (6 категорій, 23 товари)
- Кошик (додавання, зміна кількості, видалення)
- Оформлення замовлення (ім'я, телефон, email, адреса доставки)
- Сторінка підтвердження замовлення
- Адмін-панель для керування товарами та замовленнями

## Категорії товарів

- 🥦 Фрукти та овочі
- 🥩 М'ясо та риба
- 🥛 Молочні продукти
- 🍞 Хліб та випічка
- 🧃 Напої
- 🫙 Бакалія
