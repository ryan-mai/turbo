document.addEventListener('DOMContentLoaded', function() {
    currentTime();
    setInterval(currentTime, 1000);
    getWeather();

    // Bike scroll movement
    window.addEventListener('scroll', function() {
        const bike = document.querySelector('.bike');
        // Calculate how far to move the bike (adjust multiplier for speed)
        const scrollLeft = 10 + (window.scrollY / 10); // 15vw base + scroll
        bike.style.left = `calc(${scrollLeft}vw)`;
    });

    const turboTitle = document.querySelector('.turbo-title-center');
    const turboSound = document.getElementById('turbo-sound');
    if (turboTitle && turboSound) {
        turboTitle.addEventListener('click', function() {
            turboSound.currentTime = 0;
            turboSound.play();

            // Send request to activate servo
            fetch('/activate-servo', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        console.error('Servo activation failed:', data.error);
                    }
                })
                .catch(err => {
                    console.error('Error activating servo:', err);
                });
        });
    }
});

function currentTime(){
    const now = new Date();
    let hours = now.getHours();
    let ampm = hours >= 12 ? 'PM' : 'AM';
    let minutes = now.getMinutes().toString().padStart(2, '0');
    let seconds = now.getSeconds().toString().padStart(2, '0');
    document.getElementById('time').textContent = `${Math.abs(12-hours)}:${minutes}:${seconds} ${ampm}`
}
setInterval(currentTime, 1000)
currentTime();

function getWeather() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            fetch(`/weather?lat=${lat}&lon=${lon}`)
                .then(response => response.json())
                .then(data => {
                    if (data.temp !== undefined && data.temp !== null) {
                        document.getElementById('weather').textContent = `${data.temp}°C`;
                    } else {
                        document.getElementById('weather').textContent = 'Weather unavailable';
                    }
                })
                .catch(error => {
                    document.getElementById('weather').textContent = 'Weather unavailable';
                });
        });
    } else {
        document.getElementById('weather').textContent = 'Geolocation not supported';
    }
}