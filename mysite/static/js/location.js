
// To be handled when more functionality is made
function handleLocationError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            console.log("denied permission");
            break;
        case error.POSITION_UNAVAILABLE:
            console.log("location is unavailable.");
            break;
        case error.TIMEOUT:
            console.log("timed out.");
            break;
        case _:
            console.log("unknown error.");
            break;
    }
}

// If it can get the position of the user it sends to sendLocation otherwise the reason it cant is handled above
function getLocation() {
    navigator.geolocation.getCurrentPosition(sendLocation, handleLocationError);
}

// Sends the location to be used in the validity checks of redeeming the code, currently just displays the message response on the page
function sendLocation(position) {
    $.ajax({
        url: window.location.href,
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