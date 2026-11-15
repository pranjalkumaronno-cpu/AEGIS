
const cityInput = document.getElementById("cityInput");
const searchButton = document.getElementById("searchButton");


const map = L.map("map").setView([20, 0], 2);

const streetLayer = L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution: "&copy; OpenStreetMap contributors",
        maxZoom: 19
    }
);

const satelliteLayer = L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    {
        attribution: "Tiles &copy; Esri",
        maxZoom: 18
    }
);

streetLayer.addTo(map);

const baseMaps = {
    "Street Map": streetLayer,
    "Satellite": satelliteLayer
};

let radarLayer = null;

const overlayMaps = {};

const layerControl = L.control.layers(baseMaps, overlayMaps).addTo(map);

async function loadRadarLayer() {
    try {
        const response = await fetch(
            "https://api.rainviewer.com/public/weather-maps.json"
        );

        if (!response.ok) {
            throw new Error("Radar service unavailable.");
        }

        const radarData = await response.json();
        const frames = radarData.radar.past;

        if (!frames || frames.length === 0) {
            throw new Error("No radar frames available.");
        }

        const latestFrame = frames[frames.length - 1];

        if (radarLayer) {
            map.removeLayer(radarLayer);
            layerControl.removeLayer(radarLayer);
        }

        radarLayer = L.tileLayer(
            radarData.host + latestFrame.path + "/256/{z}/{x}/{y}/2/1_1.png",
            {
                opacity: 0.7,
                maxNativeZoom: 7,
                maxZoom: 19,
                attribution: 'Radar: <a href="https://www.rainviewer.com/">RainViewer</a>'
            }
        );

        layerControl.addOverlay(radarLayer, "Precipitation Radar");
        radarLayer.addTo(map);

    } catch (error) {
        console.error("Radar layer:", error);
    }
}

loadRadarLayer();


let cityMarker = null;

function displayText(elementId, value) {
    document.getElementById(elementId).textContent = value;
}

function showError(message) {
    displayText("condition", message);
    displayText("riskLevel", "ERROR");
    displayText("riskScore", "--");
    displayText("riskNote", "The analysis could not be completed.");
    document.getElementById("hazardList").textContent = message;
    document.getElementById("recommendations").textContent = "Please try another city or check your connection.";
}

function displayRisks(intelligence) {
    const hazardList = document.getElementById("hazardList");
    const recommendations = document.getElementById("recommendations");

    hazardList.replaceChildren();
    recommendations.replaceChildren();

    const risks = intelligence.identified_risks || [];

    if (risks.length === 0) {
        const message = document.createElement("p");
        message.className = "empty-state";
        message.textContent = "No risks identified by the current screening rules.";
        hazardList.appendChild(message);
    }

    risks.forEach(risk => {
        const item = document.createElement("div");
        item.className = "hazard-item";

        const title = document.createElement("strong");
        title.textContent = risk.type + " — " + risk.level;

        const details = document.createElement("span");
        details.textContent = risk.recommendation || "Follow local official guidance.";

        item.append(title, details);
        hazardList.appendChild(item);

        if (risk.recommendation) {
            const recommendation = document.createElement("div");
            recommendation.className = "recommendation-item";
            recommendation.textContent = risk.recommendation;
            recommendations.appendChild(recommendation);
        }
    });

    if (risks.length === 0) {
        const message = document.createElement("p");
        message.className = "empty-state";
        message.textContent = "Continue monitoring local conditions and official advisories.";
        recommendations.appendChild(message);
    }
}

function updateRiskDisplay(intelligence) {
    const level = intelligence.overall_level || "UNKNOWN";
    const score = intelligence.risk_score ?? "--";
    const riskCircle = document.getElementById("riskCircle");

    displayText("riskLevel", level);
    displayText("riskScore", score + " / 3");
    displayText("riskNote", intelligence.warning || "Experimental weather screening indicator.");

    const riskColors = {
        LOW: "#54d6a0",
        MODERATE: "#e8c45a",
        HIGH: "#ff994d",
        CRITICAL: "#ff5364"
    };

    const color = riskColors[level] || "#7896b5";
    riskCircle.style.borderColor = color;
    riskCircle.style.boxShadow = "0 0 25px " + color + "55";
    document.getElementById("riskLevel").style.color = color;

    displayRisks(intelligence);
}


function displayForecast(data) {
    const grid = document.getElementById("forecastGrid");
    const daily = data.daily_forecast;

    grid.replaceChildren();

    daily.time.forEach((date, index) => {
        const day = document.createElement("div");
        day.className = "forecast-day";

        const heading = document.createElement("h4");
        heading.textContent = new Date(date + "T12:00:00").toLocaleDateString(
            "en-IN",
            { weekday: "short", day: "numeric", month: "short" }
        );

        const temperature = document.createElement("div");
        temperature.className = "forecast-temp";
        temperature.textContent =
            Math.round(daily.temperature_2m_max[index]) + "°C";

        const minimum = document.createElement("p");
        minimum.textContent =
            "Low: " + Math.round(daily.temperature_2m_min[index]) + "°C";

        const rain = document.createElement("p");
        rain.textContent =
            "Rain chance: " + daily.precipitation_probability_max[index] + "%";

        const wind = document.createElement("p");
        wind.textContent =
            "Max wind: " + daily.wind_speed_10m_max[index] + " km/h";

        day.append(heading, temperature, minimum, rain, wind);
        grid.appendChild(day);
    });
}


async function analyzeCity() {
    const city = cityInput.value.trim();

    if (!city) {
        showError("Please enter a city name.");
        return;
    }

    searchButton.disabled = true;
    searchButton.textContent = "ANALYZING...";

    try {
        const weatherResponse = await fetch("/weather/" + encodeURIComponent(city));
        const weatherData = await weatherResponse.json();

        if (!weatherResponse.ok) {
            throw new Error(weatherData.detail || "Could not retrieve weather data.");
        }

        const riskResponse = await fetch("/risk/" + encodeURIComponent(city));
        const riskData = await riskResponse.json();

        if (!riskResponse.ok) {
            throw new Error(riskData.detail || "Could not complete risk analysis.");
        }

        const weather = weatherData.weather;
        const location = weatherData.location;

        displayText("temperature", weather.temperature + "°" + (weather.units === "fahrenheit" ? "F" : weather.units === "kelvin" ? "K" : "C"));
        displayText("condition", weather.condition);
        displayText("humidity", weather.humidity + "%");
        displayText("wind", weather.wind_speed_kmh);
        displayText("precipitation", weather.precipitation);

        const latitude = location.latitude;
        const longitude = location.longitude;

        map.setView([latitude, longitude], 8);

        if (cityMarker) {
            map.removeLayer(cityMarker);
        }

        cityMarker = L.marker([latitude, longitude])
            .addTo(map)
            .bindPopup("<strong>" + location.city + ", " + (location.country || "") + "</strong>")
            .openPopup();

        displayText("mapCaption", location.city + ", " + (location.country || ""));

        updateRiskDisplay(riskData.intelligence);
const forecastResponse = await fetch(
    "/forecast/" + encodeURIComponent(city)
);

const forecastData = await forecastResponse.json();

if (!forecastResponse.ok) {
    throw new Error(forecastData.detail || "Forecast unavailable.");
}

displayForecast(forecastData);

    } catch (error) {
        showError(error.message);
    } finally {
        searchButton.disabled = false;
        searchButton.textContent = "ANALYZE";
    }
}

searchButton.addEventListener("click", analyzeCity);

cityInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        analyzeCity();
       
displayForecast(forecastData);
    }
});
