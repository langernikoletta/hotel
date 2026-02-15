"""
URL Configuration for hotel project.
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import main_views

urlpatterns = [
    # Адмінка
    path('admin/', admin.site.urls),

    # Основні сторінки
    path('', main_views.home, name='home'),
    path('about/', main_views.about, name='about'),
    path('booking/', main_views.booking_view, name='booking'),
    path('calendar/', main_views.calendar_view, name='calendar'),

    # Бронювання (API)
    path('api/bookings/', main_views.api_bookings, name='api_bookings'),

    # Авторизація
    path('login/', main_views.login_view, name='login'),
    path('register/', main_views.register_view, name='register'),
    path('logout/', main_views.logout_view, name='logout'),

    # ⭐ ВІДГУКИ
    path('reviews/', main_views.reviews_rooms, name='reviews_rooms'),
    path('reviews/room/<int:room_id>/', main_views.room_reviews, name='room_reviews'),
]

# Статичні та медіа файли (тільки в DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
