
let map;
let service;
let infowindow;

function initMap(position) {
    const userLocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };

    map = new google.maps.Map(document.getElementById("map"), {
        center: userLocation,
        zoom: 15,
    });

    infowindow = new google.maps.InfoWindow();

    // Add marker for user's location
    new google.maps.Marker({
        position: userLocation,
        map: map,
        title: "Your Location",
        icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
    });

    // Search for nearby pharmacies
    const request = {
        location: userLocation,
        radius: '1500',
        type: ['pharmacy']
    };

    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, handleSearchResults);
}

function handleSearchResults(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
        for (let place of results) {
            createMarker(place);
        }
    }
}

function createMarker(place) {
    const marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        title: place.name
    });

    google.maps.event.addListener(marker, "click", () => {
        const content = `
            <div>
                <h5>${place.name}</h5>
                <p>${place.vicinity}</p>
                <p>Rating: ${place.rating || 'N/A'}</p>
            </div>
        `;
        infowindow.setContent(content);
        infowindow.open(map, marker);
    });
}

function findNearbyPharmacies() {
    document.getElementById('pharmacy-locator').classList.remove('d-none');
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(initMap, handleLocationError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function handleLocationError(error) {
    let message = "An error occurred while retrieving your location.";
    switch(error.code) {
        case error.PERMISSION_DENIED:
            message = "Please allow location access to find nearby pharmacies.";
            break;
        case error.POSITION_UNAVAILABLE:
            message = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            message = "Location request timed out.";
            break;
    }
    alert(message);
}
