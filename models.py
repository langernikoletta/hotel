"""
Models for hotel project.
"""

from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    """Hotel room model."""

    ROOM_TYPES = [
        ('single', 'Одномісна'),
        ('double', 'Двомісна'),
        ('suite', 'Люкс'),
    ]

    number = models.IntegerField(unique=True, verbose_name='Номер кімнати')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, verbose_name='Тип кімнати')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна за ніч')
    is_available = models.BooleanField(default=True, verbose_name='Доступна')
    description = models.TextField(blank=True, verbose_name='Опис')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    class Meta:
        verbose_name = 'Кімната'
        verbose_name_plural = 'Кімнати'
        ordering = ['number']

    def __str__(self):
        return f"Кімната {self.number} - {self.get_room_type_display()}"


class Booking(models.Model):
    """Hotel booking model."""

    STATUS_CHOICES = [
        ('pending', 'На розгляді'),
        ('confirmed', 'Підтверджено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Кімната')
    guest_name = models.CharField(max_length=100, verbose_name="Ім'я гостя")
    guest_email = models.EmailField(verbose_name='Email')
    guest_phone = models.CharField(max_length=20, verbose_name='Телефон')
    check_in = models.DateField(verbose_name='Заїзд')
    check_out = models.DateField(verbose_name='Виїзд')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Загальна ціна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата бронювання')

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'
        ordering = ['-created_at']

    def __str__(self):
        return f"Бронювання {self.id} - {self.guest_name}"


class Review(models.Model):
    """Room review model."""

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Кімната'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Користувач'
    )

    rating = models.PositiveSmallIntegerField(
        verbose_name='Оцінка',
        help_text='Оцінка від 1 до 5'
    )

    text = models.TextField(verbose_name='Відгук')

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        ordering = ['-created_at']

    def __str__(self):
        return f"Кімната {self.room.number} — {self.user.username}"
