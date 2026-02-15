"""
Forms for hotel project.
"""

from django import forms
from django.core.exceptions import ValidationError

from .models import Booking, Review


class BookingForm(forms.ModelForm):
    """Booking form with date/availability validation."""

    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'room', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-select' if field_name == 'room' else 'form-control'
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing} {css_class}".strip()

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')

        if check_in and check_out and check_in >= check_out:
            self.add_error('check_out', 'Дата виїзду має бути пізніше за дату заїзду.')

        if room and check_in and check_out:
            overlaps = (
                Booking.objects
                .filter(room=room, status__in=['pending', 'confirmed'])
                .exclude(check_out__lte=check_in)
                .exclude(check_in__gte=check_out)
            )
            if self.instance.pk:
                overlaps = overlaps.exclude(pk=self.instance.pk)

            if overlaps.exists():
                raise ValidationError('Ця кімната вже заброньована на обрані дати.')

        return cleaned_data

    def save(self, commit=True):
        booking = super().save(commit=False)
        nights = max((booking.check_out - booking.check_in).days, 1)
        booking.total_price = booking.room.price * nights
        if commit:
            booking.save()
        return booking


class ReviewForm(forms.ModelForm):
    """Review form for room feedback."""

    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f"{existing} form-control".strip()

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise ValidationError('Оцінка має бути від 1 до 5.')
        return rating
