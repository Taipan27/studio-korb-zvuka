"""Модели приложения bookings."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Studio(models.Model):
    """Комната студии звукозаписи."""
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    hourly_rate = models.DecimalField('Стоимость за час, ₽',
                                      max_digits=8, decimal_places=2,
                                      default=1500)
    equipment = models.CharField('Оборудование', max_length=255, blank=True)
    is_active = models.BooleanField('Доступна для брони', default=True)

    class Meta:
        verbose_name = 'Студия'
        verbose_name_plural = 'Студии'

    def __str__(self):
        return self.name


class Booking(models.Model):
    """Бронирование студии."""
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('cancelled', 'Отменена'),
        ('completed', 'Завершена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='bookings',
                             verbose_name='Клиент')
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE,
                               related_name='bookings',
                               verbose_name='Студия')
    date = models.DateField('Дата')
    start_time = models.TimeField('Время начала')
    duration_hours = models.PositiveIntegerField('Длительность, ч', default=2)
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=20,
                              choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField('Создана', default=timezone.now)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f'{self.studio.name} — {self.date} {self.start_time}'

    @property
    def total_cost(self):
        return self.duration_hours * self.studio.hourly_rate

    def can_be_cancelled(self):
        """Бронь можно отменить, если она активна."""
        if self.status != 'active':
            return False
        return True
