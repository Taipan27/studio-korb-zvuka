"""Создание демонстрационных данных для прототипа."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studio_korb_zvuka.settings')
django.setup()

from datetime import date, time, timedelta
from django.contrib.auth.models import User
from bookings.models import Studio, Booking

# Студии
Studio.objects.all().delete()
s1 = Studio.objects.create(
    name='Зал А — «Vintage»',
    description='Аналоговый микшерный пульт SSL, ламповые предусилители.',
    hourly_rate=2500,
    equipment='SSL 4000, Neumann U87, монитор Yamaha NS-10M',
)
s2 = Studio.objects.create(
    name='Зал Б — «Digital»',
    description='Современный цифровой комплекс для трекинга и сведения.',
    hourly_rate=1800,
    equipment='Pro Tools HDX, RME UCX, Genelec 8030',
)
Studio.objects.create(
    name='Зал В — «Vocal»',
    description='Кабина для вокала с минимальной реверберацией.',
    hourly_rate=1200,
    equipment='Shure SM7B, Cloudlifter, ноутбук с DAW',
)

# Пользователь
User.objects.filter(username='roman').delete()
u = User.objects.create_user(
    username='roman', email='roman@studio.test',
    password='demo1234', first_name='Роман',
)

# Брони
today = date.today()
Booking.objects.create(user=u, studio=s1,
                       date=today + timedelta(days=3),
                       start_time=time(15, 0), duration_hours=3,
                       comment='Запись вокальной партии.', status='active')
Booking.objects.create(user=u, studio=s2,
                       date=today + timedelta(days=7),
                       start_time=time(11, 0), duration_hours=4,
                       comment='Сведение трека.', status='active')
Booking.objects.create(user=u, studio=s1,
                       date=today - timedelta(days=10),
                       start_time=time(14, 0), duration_hours=2,
                       status='completed')
Booking.objects.create(user=u, studio=s2,
                       date=today - timedelta(days=20),
                       start_time=time(18, 0), duration_hours=2,
                       status='cancelled')

# Админ
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@studio.test', 'admin1234')

print('Демо-данные созданы.')
