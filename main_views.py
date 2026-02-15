"""
Main app views for hotel project.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse

from .forms import BookingForm, ReviewForm
from .models import Room
from .models import Booking


def _apply_bootstrap(form):
    for field in form.fields.values():
        existing = field.widget.attrs.get('class', '')
        field.widget.attrs['class'] = f"{existing} form-control".strip()
    return form


def home(request):
    """Home page view."""
    return render(request, 'main/index.html')


def about(request):
    """About page view."""
    return render(request, 'main/about.html')


def calendar_view(request):
    """Render the calendar page."""
    return render(request, 'main/calendar.html')


def booking_view(request):
    """Create a booking from the website form."""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронювання успішно створено.')
            return redirect('booking')
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})


def api_bookings(request):
    """Return bookings as JSON for FullCalendar."""
    bookings = Booking.objects.all()
    events = []
    for b in bookings:
        events.append({
            'id': b.id,
            'title': f"Кімната {b.room.number} — {b.guest_name}",
            'start': b.check_in.isoformat(),
            'end': b.check_out.isoformat(),
            'extendedProps': {
                'room': b.room.number,
                'status': b.status,
            }
        })
    return JsonResponse(events, safe=False)


def login_view(request):
    """User login view."""
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == 'POST':
        form = _apply_bootstrap(AuthenticationForm(request, data=request.POST))
        if form.is_valid():
            auth_login(request, form.get_user())
            if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
                return redirect(next_url)
            return redirect('home')
    else:
        form = _apply_bootstrap(AuthenticationForm(request))
    return render(request, 'auth/login.html', {'form': form, 'next': next_url})


def register_view(request):
    """User registration view."""
    if request.method == 'POST':
        form = _apply_bootstrap(UserCreationForm(request.POST))
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = _apply_bootstrap(UserCreationForm())
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    """User logout view."""
    auth_logout(request)
    return redirect('home')


def reviews_rooms(request):
    """Список кімнат для перегляду відгуків"""
    rooms = Room.objects.all()
    return render(request, 'reviews/rooms.html', {
        'rooms': rooms
    })


def room_reviews(request, room_id):
    """Відгуки конкретної кімнати"""
    room = get_object_or_404(Room, id=room_id)
    reviews = room.reviews.select_related('user').all()
    form = ReviewForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, 'Дякуємо за відгук.')
            return redirect('room_reviews', room_id=room.id)

    return render(request, 'reviews/room_reviews.html', {
        'room': room,
        'reviews': reviews,
        'form': form,
    })
