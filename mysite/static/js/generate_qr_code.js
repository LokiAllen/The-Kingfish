/*
    Sends a GET request with the QR code to generate, and then will output the QR code
    generated onto the '#qrCodeContainer' element
    - Cleans the code input for the reasons:
        - This is called either by getting the QR code of existing QR codes or where no code is provided
        - So it allows it to be used in different contexts
*/
function generateQRCode(code=null) {
    if (code === null) {
        var code = $('#dataInput').val();
        if (code == "") {
            code = random_code();
        }
    }

    $.ajax({
        url: `/admin/manageqr/generate/${code}`,
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            $('#qrCodeContainer').html(`<img src="${response.qr_code_data}" alt="QR Code">`);
            $('#qrCodeContainer').append(`<br>`);
            $('#qrCodeContainer').append(`<button onclick=add_to_database('${code}')>Add to database</button>`);
            refresh_values();
        },
        error: function(error) {
            console.error('Error fetching QR code:', error);
        }
    });
}

// Generates a strong random QR code value - Was done on the JS instead of the Python side as complexities were found somewhere
// Format of the code can also be edited
function random_code() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Sends a POST request to delete the QR code from the database
function deleteQRCode(code) {
    console.log(CSRF_TOKEN);
    $.ajax({
        url: `/admin/manageqr/delete/${code}`,
        type: 'POST',
        data: {
            data: code,
            csrfmiddlewaretoken: CSRF_TOKEN,
        },
        success: function(response) {
            refresh_values();
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

// Sends a GET request to retrieve all the current QR codes and fills the 'qrContainer' with those
function refresh_values() {
    var qrContainer = $('.qr-container');

    $.ajax({
        url: '/admin/manageqr/get_codes',
        type: 'GET',
        success: function(data) {
            // Update the values list with the new data
            qrContainer.html('');
            data.values.forEach(function(value) {
                qrContainer.append('<li> ' + value.id + ' - ' + value.expired + ' - ' + value.address + ' ' +
                    '<button onclick="generateQRCode(\'' + value.id + '\')">Get QR Code</button>' + ' ' +
                    '<button onclick="deleteQRCode(\'' + value.id + '\')">Delete</button>');
            });
        },
        error: function(error) {
            console.error(error);
        }
    });
}

// Sends a POST request to add a new QR code to the database
function add_to_database(code) {
    $.ajax({
        url: `/admin/manageqr/add/${code}`,
        type: 'POST',
        data: {
            data: code,
            csrfmiddlewaretoken: CSRF_TOKEN,
        },
        success: function(response) {
            refresh_values();
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

// Just toggles whether you can see the list of QR codes
function showQRCodes() {
    var qrContainer = document.querySelector('.qr-container');
    if (qrContainer.style.display === 'none') {
        qrContainer.style.display = 'block'
    } else {
        qrContainer.style.display = 'none'
    }
}