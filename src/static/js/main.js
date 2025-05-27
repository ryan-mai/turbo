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

// Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
function getWeather() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const apiKey = 'YOUR_API_KEY';
            const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=metric&appid=${apiKey}`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    // Example: display temperature and weather description
                    const temp = data.main.temp;
                    const desc = data.weather[0].description;
                    document.getElementById('weather').textContent = `${temp}°C, ${desc}`;
                })
                .catch(error => {
                    document.getElementById('weather').textContent = 'Weather unavailable';
                });
        });
    } else {
        document.getElementById('weather').textContent = 'Geolocation not supported';
    }
}

// Call this function after the page loads
getWeather();