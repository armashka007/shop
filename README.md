# Интернет-магазин на Django

Полнофункциональный интернет-магазин с каталогом товаров, корзиной, аутентификацией и возможностью оформления заказов.

## 📋 Требования

- Python 3.8+
- Django 6.0+
- PostgreSQL (опционально, используется SQLite по умолчанию)

## 🚀 Установка и запуск

### 1. Клонирование проекта
```bash
git clone <repository-url>
cd shop
```

### 2. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Подготовка базы данных
```bash
python manage.py migrate
```

### 4. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 5. Загрузка тестовых данных (опционально)
```bash
python populate_db.py
```

### 6. Запуск сервера
```bash
python manage.py runserver
```

Сайт будет доступен по адресу: **http://localhost:8000**

## 🔐 Админ-панель

Доступ к админ-панели: **http://localhost:8000/admin**

### Учетные данные тестового суперпользователя:
- **Логин:** admin или arman
- **Пароль:** запросите у разработчика

## 📦 Функциональность

### Каталог товаров
- ✅ Просмотр категорий товаров
- ✅ Фильтрация по категориям
- ✅ Поиск по названию и описанию
- ✅ Сортировка (по названию, цене, новинкам)
- ✅ Пагинация (по 8 товаров на странице)

### Товары
- ✅ Галерея изображений
- ✅ Цена и старая цена (скидки)
- ✅ Бейджи наличия/отсутствия
- ✅ Детальное описание
- ✅ Информация о количестве на складе

### Корзина
- 🔄 Хранение в сессии (без регистрации)
- ✅ Добавление товаров
- ✅ Изменение количества
- ✅ Удаление товаров
- ✅ Расчет итоговой суммы

### Аутентификация
- ✅ Регистрация пользователей
- ✅ Вход/Выход
- ✅ Профиль пользователя

### Заказы
- ✅ Оформление заказа
- ✅ История заказов ("Мои заказы")
- ✅ Фильтрация заказов по статусу
- ✅ Отслеживание статуса заказа

## 🛠️ Структура проекта

```
shop/
├── config/              # Основные настройки Django
│   ├── settings.py     # Параметры проекта
│   ├── urls.py         # Маршруты проекта
│   └── wsgi.py
├── catalog/            # Приложение каталога
│   ├── models.py       # Модели (Category, Product, ProductImage)
│   ├── views.py        # Представления
│   ├── urls.py         # Маршруты каталога
│   └── admin.py        # Админ-интерфейс
├── orders/             # Приложение заказов
│   ├── models.py       # Модели (Order, OrderItem)
│   ├── views.py        # Представления
│   └── admin.py        # Админ-интерфейс
├── accounts/           # Приложение аккаунтов
│   ├── views.py        # Представления (регистрация, профиль)
│   ├── urls.py         # Маршруты
│   └── forms.py        # Формы
├── templates/          # HTML-шаблоны
│   ├── base.html       # Базовый шаблон
│   └── catalog/        # Шаблоны каталога
├── manage.py           # Команды Django
├── populate_db.py      # Скрипт заполнения БД тестовыми данными
└── requirements.txt    # Зависимости проекта
```

## 🗂️ Моделк данных

### Category (Категория)
```
- name: CharField (максимум 200 символов)
- slug: SlugField (уникальный URL-дружественный идентификатор)
- description: TextField (опционально)
```

### Product (Товар)
```
- category: ForeignKey → Category
- name: CharField
- slug: SlugField (уникальный)
- description: TextField
- price: DecimalField (максимум 10 символов, 2 знака после запятой)
- old_price: DecimalField (опционально, для скидок)
- stock: PositiveIntegerField (количество на складе)
- is_active: BooleanField (активен/неактивен)
- created_at: DateTimeField (дата создания)
- updated_at: DateTimeField (дата обновления)
```

### ProductImage (Изображение товара)
```
- product: ForeignKey → Product
- image: ImageField (путь: products/)
- alt_text: CharField (текст при недоступности изображения)
- is_main: BooleanField (главное изображение)
```

### Order (Заказ)
```
- user: ForeignKey → User (опционально)
- full_name: CharField
- phone: CharField
- address: TextField
- status: CharField (pending, processing, shipped, delivered, cancelled)
- created_at: DateTimeField
- updated_at: DateTimeField
```

### OrderItem (Позиция заказа)
```
- order: ForeignKey → Order
- product: ForeignKey → Product
- quantity: PositiveIntegerField
- price: DecimalField (цена в момент заказа)
```

## ⚙️ Переменные окружения (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database engine: 'sqlite' или 'postgresql'
DB_ENGINE=sqlite

# PostgreSQL settings (если используется)
DB_NAME=shop
DB_USER=shop_user
DB_PASSWORD=StrongPass123
DB_HOST=localhost
DB_PORT=5432
```

## 📝 Примеры использования

### Добавление товара через админ-панель
1. Перейти на http://localhost:8000/admin
2. Войти с учетными данными суперпользователя
3. В разделе "Products" нажать "Add Product"
4. Заполнить поля и нажать "Save"
5. Добавить изображения в разделе "Product Images"

### Поиск товаров
- Перейти на главную страницу
- Использовать поле поиска для поиска по названию
- Применить фильтры (цена, наличие)
- Выбрать сортировку

## 🔗 Основные URL-ы

- `/` - Главная страница
- `/categories/` - Список всех категорий
- `/category/<slug>/` - Товары в категории
- `/product/<slug>/` - Карточка товара
- `/admin/` - Админ-панель

## 📱 Тестовые товары

После запуска `python populate_db.py` в БД добавятся:

### Электроника (15 товаров)
- Мобильный телефон XPhone 15 (со скидкой)
- Ноутбук ProBook X1
- Наушники SoundMax Pro (нет в наличии)

### Одежда
- Спортивная футболка Active
- Джинсы ClassicFit (со скидкой)
- Кроссовки RunLimit

### Книги
- Война и мир - Толстой
- Преступление и наказание - Достоевский (нет в наличии)
- Йога для начинающих

### Спорт
- Гантели 10кг пара
- Коврик для йоги Premium (со скидкой)

### Дом
- Кастрюля 5л с крышкой
- Набор постельного белья (со скидкой)
- Люстра современный дизайн

## 🐛 Проблемы и решения

### Ошибка: "No module named 'psycopg2'"
Решение: Установите `psycopg2-binary`
```bash
pip install psycopg2-binary
```

### Ошибка при подключении к PostgreSQL
Убедитесь, что:
1. PostgreSQL установлен и запущен
2. Верны учетные данные в `.env`
3. База данных существует

### Изображения не загружаются
Убедитесь, что:
1. Установлена библиотека Pillow: `pip install pillow`
2. Директория `media/` существует и доступна для записи
3. DEBUG=True в settings.py

## 📄 Лицензия

MIT License

## 👤 Разработчик

Для вопросов и предложений обращайтесь к разработчику проекта.
