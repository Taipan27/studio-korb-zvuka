# STУDИЯ КОRБ.ЗVУКА — прототип системы бронирования

Прототип веб-приложения для студии звукозаписи, разработанный в рамках
лабораторной работы №3 по дисциплине «Управление IT-проектами».

**Студент:** Скопцов Б. А., группа 23ИВ1б
**Преподаватель:** ст. преп. каф. «Программирование» Зупарова В. В.
**Год:** 2026

## Реализованные функции (инкремент 1+2)

| № | Функция | Модуль | URL |
|---|---------|--------|-----|
| 1 | Регистрация пользователя | accounts | `/accounts/register/` |
| 2 | Авторизация | accounts | `/accounts/login/` |
| 3 | Личный кабинет | dashboard | `/dashboard/` |
| 4 | Бронирование студии | bookings | `/bookings/new/` |
| 5 | Отмена брони | bookings | `/bookings/<id>/cancel/` |

## Технологический стек

- **Python 3.12** — язык разработки
- **Django 6.0** — веб-фреймворк (MTV-архитектура)
- **SQLite 3** — встроенная СУБД для прототипа
- **HTML / CSS** — клиентская часть, шаблоны Django

## Структура проекта

```
studio_korb_zvuka/
├── manage.py                  # Управляющий скрипт Django
├── seed_data.py               # Скрипт демо-данных
├── db.sqlite3                 # База данных SQLite
├── studio_korb_zvuka/         # Конфигурация проекта
│   ├── settings.py            # Настройки
│   ├── urls.py                # Корневой роутинг
│   └── wsgi.py
├── accounts/                  # Регистрация и авторизация
│   ├── models.py              # (стандартный User)
│   ├── forms.py               # RegisterForm, LoginForm
│   ├── views.py               # register_view, StudioLoginView, StudioLogoutView
│   └── urls.py
├── bookings/                  # Бронирование и отмена
│   ├── models.py              # Studio, Booking
│   ├── forms.py               # BookingForm
│   ├── views.py               # booking_create, booking_cancel
│   ├── admin.py               # Регистрация в админ-панели
│   └── urls.py
├── dashboard/                 # Личный кабинет
│   ├── views.py               # index
│   └── urls.py
├── templates/                 # HTML-шаблоны
│   ├── base.html
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   ├── bookings/
│   │   ├── booking_form.html
│   │   └── booking_cancel.html
│   └── dashboard/
│       └── index.html
└── static/css/main.css        # Стили
```

## Запуск проекта

### Требования
- Python 3.10 или выше
- pip

### Установка и запуск

```bash
# Установить Django
pip install django

# Применить миграции
python manage.py migrate

# Загрузить демонстрационные данные
python seed_data.py

# Запустить сервер
python manage.py runserver
```

Открыть в браузере: <http://127.0.0.1:8000/>

### Демонстрационные учётные записи

| Логин | Пароль | Роль |
|-------|--------|------|
| `roman` | `demo1234` | Клиент с тестовыми бронями |
| `admin` | `admin1234` | Администратор (доступ к `/admin/`) |
