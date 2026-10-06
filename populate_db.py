#!/usr/bin/env python
"""
Script to populate database with test data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Category, Product, ProductImage
from decimal import Decimal

# Clear existing data (optional)
# Product.objects.all().delete()
# Category.objects.all().delete()

# Create categories
categories_data = [
    {'name': 'Процессоры', 'slug': 'processors', 'description': 'Процессоры Intel и AMD для ПК'},
    {'name': 'Видеокарты', 'slug': 'graphics-cards', 'description': 'Графические ускорители NVIDIA и AMD'},
    {'name': 'Оперативная память', 'slug': 'ram', 'description': 'Модули памяти DDR4, DDR5'},
    {'name': 'Материнские платы', 'slug': 'motherboards', 'description': 'Материнские платы для ПК'},
    {'name': 'Накопители', 'slug': 'storage', 'description': 'SSD и HDD диски'},
    {'name': 'Источники питания', 'slug': 'power-supplies', 'description': 'Блоки питания для ПК'},
    {'name': 'Охлаждение', 'slug': 'cooling', 'description': 'Кулеры и системы охлаждения'},
]

categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={'name': cat_data['name'], 'description': cat_data['description']}
    )
    categories[cat_data['slug']] = cat
    print(f"{'Создана' if created else 'Уже существует'} категория: {cat.name}")

# Create products
products_data = [
    {
        'name': 'Intel Core i7-14700K',
        'slug': 'intel-i7-14700k',
        'category': 'processors',
        'price': Decimal('85000.00'),
        'old_price': Decimal('95000.00'),
        'stock': 12,
        'description': 'Процессор 14-го поколения, 20 ядер, 28 потоков. Socket 1700. TDP 125W. Отличное соотношение цены и производительности.',
    },
    {
        'name': 'AMD Ryzen 7 7800X3D',
        'slug': 'amd-ryzen-7-7800x3d',
        'category': 'processors',
        'price': Decimal('78000.00'),
        'old_price': Decimal('88000.00'),
        'stock': 8,
        'description': 'Процессор с 3D V-Cache, 8 ядер, 16 потоков. Socket AM5. Лучший выбор для игр и создания контента.',
    },
    {
        'name': 'Intel Core i5-14600K',
        'slug': 'intel-i5-14600k',
        'category': 'processors',
        'price': Decimal('45000.00'),
        'old_price': None,
        'stock': 20,
        'description': 'Процессор среднего уровня, 14 ядер, 20 потоков. Хороший выбор для офиса и легких игр.',
    },
    {
        'name': 'NVIDIA GeForce RTX 4090',
        'slug': 'nvidia-rtx-4090',
        'category': 'graphics-cards',
        'price': Decimal('280000.00'),
        'old_price': None,
        'stock': 3,
        'description': 'Флагманская видеокарта с 24GB GDDR6X. Для 4K гейминга и профессионального ПО. Разъемы HDMI и DP.',
    },
    {
        'name': 'NVIDIA GeForce RTX 4080',
        'slug': 'nvidia-rtx-4080',
        'category': 'graphics-cards',
        'price': Decimal('165000.00'),
        'old_price': Decimal('185000.00'),
        'stock': 6,
        'description': 'Мощная видеокарта с 16GB GDDR6X. Идеальна для 1440p Ultra и 4K гейминга.',
    },
    {
        'name': 'AMD Radeon RX 7900 XTX',
        'slug': 'amd-radeon-rx-7900-xtx',
        'category': 'graphics-cards',
        'price': Decimal('155000.00'),
        'old_price': None,
        'stock': 5,
        'description': 'Альтернатива RTX 4080 с 24GB памяти. Отличное значение на рынке.',
    },
    {
        'name': 'Kingston Fury Beast DDR5 32GB',
        'slug': 'kingston-fury-32gb',
        'category': 'ram',
        'price': Decimal('28000.00'),
        'old_price': Decimal('35000.00'),
        'stock': 25,
        'description': 'Модуль памяти DDR5 (2x16GB), частота 6000MHz, CAS 30. Отличный вариант для игр.',
    },
    {
        'name': 'G.Skill Trident Z5 32GB',
        'slug': 'gskill-trident-z5-32gb',
        'category': 'ram',
        'price': Decimal('32000.00'),
        'old_price': None,
        'stock': 18,
        'description': 'Премиум память DDR5 (2x16GB), частота 6400MHz, CAS 32. RGB подсветка.',
    },
    {
        'name': 'Corsair Vengeance DDR5 64GB',
        'slug': 'corsair-vengeance-64gb',
        'category': 'ram',
        'price': Decimal('58000.00'),
        'old_price': Decimal('68000.00'),
        'stock': 10,
        'description': 'Комплект памяти (4x16GB) DDR5 6000MHz. Идеально для рабочих станций и мощных ПК.',
    },
    {
        'name': 'ASUS ROG STRIX Z790-E',
        'slug': 'asus-rog-strix-z790-e',
        'category': 'motherboards',
        'price': Decimal('72000.00'),
        'old_price': Decimal('85000.00'),
        'stock': 7,
        'description': 'Топовая материнская плата Intel Z790. Поддержка DDR5, WiFi 6E, Thunderbolt 4.',
    },
    {
        'name': 'MSI MPG B850 Edge WiFi',
        'slug': 'msi-mpg-b850-edge',
        'category': 'motherboards',
        'price': Decimal('52000.00'),
        'old_price': None,
        'stock': 12,
        'description': 'Материнская плата AMD B850, Socket AM5. PCIe 5.0, DDR5, WiFi 6E поддержка.',
    },
    {
        'name': 'Samsung 990 Pro 1TB NVMe',
        'slug': 'samsung-990-pro-1tb',
        'category': 'storage',
        'price': Decimal('18000.00'),
        'old_price': Decimal('22000.00'),
        'stock': 30,
        'description': 'Скоростной SSD NVMe PCIe 4.0. Скорость: 7100MB/s чтение, 6000MB/s запись.',
    },
    {
        'name': 'WD Black SN850X 2TB',
        'slug': 'wd-black-sn850x-2tb',
        'category': 'storage',
        'price': Decimal('32000.00'),
        'old_price': None,
        'stock': 22,
        'description': 'Высокопроизводительный SSD для игр. 7100MB/s чтения. PCIe 4.0, NVMe.',
    },
    {
        'name': 'Seagate IronWolf 4TB HDD',
        'slug': 'seagate-ironwolf-4tb',
        'category': 'storage',
        'price': Decimal('15000.00'),
        'old_price': None,
        'stock': 0,
        'description': 'Надежный жесткий диск 4TB для хранения. 5400 RPM, SATA.',
    },
    {
        'name': 'Corsair RM1000x 1000W',
        'slug': 'corsair-rm1000x',
        'category': 'power-supplies',
        'price': Decimal('42000.00'),
        'old_price': Decimal('48000.00'),
        'stock': 14,
        'description': 'Модульный 80+ Gold блок питания 1000W. Гарантия 10 лет. Для мощных ПК.',
    },
    {
        'name': 'Seasonic Focus GX-1000',
        'slug': 'seasonic-focus-gx-1000',
        'category': 'power-supplies',
        'price': Decimal('38000.00'),
        'old_price': None,
        'stock': 9,
        'description': 'Модульный 80+ Gold блок пиания 1000W. Тихий вентилятор, отличная стабильность.',
    },
    {
        'name': 'BE Quiet! System Power 750W',
        'slug': 'be-quiet-750w',
        'category': 'power-supplies',
        'price': Decimal('28000.00'),
        'old_price': None,
        'stock': 16,
        'description': 'Надежный 80+ Bronze блок питания 750W. Простой, функциональный и экономичный.',
    },
    {
        'name': 'Noctua NH-D15',
        'slug': 'noctua-nh-d15',
        'category': 'cooling',
        'price': Decimal('22000.00'),
        'old_price': Decimal('26000.00'),
        'stock': 11,
        'description': 'Воздушный кулер, высокопроизводительный. Два вентилятора 140мм. Шум 24.6 дБ.',
    },
    {
        'name': 'Be Quiet! Dark Rock Pro 4',
        'slug': 'be-quiet-dark-rock-pro-4',
        'category': 'cooling',
        'price': Decimal('20000.00'),
        'old_price': None,
        'stock': 13,
        'description': 'Премиум воздушный кулер черного цвета. Совместим с Intel и AMD. Тихий и эффективный.',
    },
    {
        'name': 'Corsair iCUE H150i Elite',
        'slug': 'corsair-icue-h150i',
        'category': 'cooling',
        'price': Decimal('35000.00'),
        'old_price': Decimal('42000.00'),
        'stock': 6,
        'description': 'Жидкостное охлаждение 360мм. RGB подсветка, управление через программное обеспечение.',
    },
]

products = {}
for prod_data in products_data:
    category = categories[prod_data.pop('category')]
    prod_slug = prod_data['slug']
    prod, created = Product.objects.get_or_create(
        slug=prod_slug,
        defaults={**prod_data, 'category': category}
    )
    products[prod_slug] = prod
    print(f"{'Создан' if created else 'Уже существует'} товар: {prod.name}")

print("\nДанные успешно загружены!")
print(f"Категорий: {len(categories)}")
print(f"Товаров: {len(products)}")
