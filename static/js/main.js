// Main JavaScript file for hotel website

document.addEventListener('DOMContentLoaded', function() {
    console.log('Hotel website loaded');
    
    // Додайте свій JavaScript код тут
});

// Функція для завантаження кімнат
function loadRooms() {
    fetch('/api/rooms/')
        .then(response => response.json())
        .then(data => {
            console.log('Rooms:', data);
        })
        .catch(error => console.error('Error:', error));
}
