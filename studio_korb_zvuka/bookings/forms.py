"""Формы для приложения bookings."""
from django import forms
from django.utils import timezone
from .models import Booking, Studio


class BookingForm(forms.ModelForm):
    """Форма создания брони."""

    class Meta:
        model = Booking
        fields = ['studio', 'date', 'start_time', 'duration_hours', 'comment']
        widgets = {
            'studio': forms.Select(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-input',
                                                       'min': 1, 'max': 12}),
            'comment': forms.Textarea(attrs={'class': 'form-input',
                                             'rows': 3,
                                             'placeholder':
                                             'Дополнительные пожелания…'}),
        }
        labels = {
            'studio': 'Комната студии',
            'date': 'Дата',
            'start_time': 'Время начала',
            'duration_hours': 'Длительность (часов)',
            'comment': 'Комментарий',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['studio'].queryset = Studio.objects.filter(is_active=True)

    def clean_date(self):
        d = self.cleaned_data['date']
        if d < timezone.localdate():
            raise forms.ValidationError('Дата не может быть в прошлом.')
        return d
