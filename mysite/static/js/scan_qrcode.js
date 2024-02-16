var qrcode;
function setCode(code) {
    qrcode = code;
}

// Gets the location of the user and then calls 'sendLocation()' with their position
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendLocation);
    } else {
        alert("Location is not supported by this browser.");
    }
}

// Sends their location and code to be used to check the validity of both
function sendLocation(position) {
    $.ajax({
        url: `/qrcodes/location/${qrcode}`,
        type: 'POST',
        data: {
            'latitude': position.coords.latitude,
            'longitude': position.coords.longitude,
            csrfmiddlewaretoken: CSRF_TOKEN,
        },
        success: function(response) {
            $('#status').html(response['message']);
        },
        error: function(error) {
            $('#status').html(response['message']);
        }
    });
}