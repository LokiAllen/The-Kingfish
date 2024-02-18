// Generates a strong random QR code value
function random_code() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}


/*
   Generates a QR code relative to what it is generating and renders it
    - 'code' is cleaned so it can be used for either random code, user inputted code or existing code
*/
function generateQRCode(code=null) {
    if (code === null) {
        var code = $('#dataInput').val();
        if (code == "") {
            code = random_code();
        }
    }

    $.ajax({
        url: `/siteadmin/manageqr/${code}/`,
        type: 'GET',
        data: {
            'method': 'generate'
        },
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

// Sends a POST request to add the new QR code to the database
function add_to_database(code) {
    $.ajax({
        url: `/siteadmin/manageqr/${code}/`,
        type: 'POST',
        data: {
            data: code,
            csrfmiddlewaretoken: CSRF_TOKEN,
            'method': 'add'
        },
        success: function(response) {
            refresh_values();
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

// Sends a POST request to delete the QR code from the database
function deleteQRCode(code) {
    console.log(CSRF_TOKEN);
    $.ajax({
        url: `/siteadmin/manageqr/${code}/`,
        type: 'POST',
        data: {
            data: code,
            csrfmiddlewaretoken: CSRF_TOKEN,
            'method': 'delete',
        },
        success: function(response) {
            refresh_values();
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

// Sends a GET request to retrieve all the current QR codes and fills the table with those
function refresh_values() {
    var qrContainer = $('.qr-container');

    $.ajax({
        url: '/siteadmin/manageqr/',
        type: 'GET',
        data: {
            'method': 'refresh'
        },
        success: function(data) {
            qrContainer.html('');
            data.values.forEach(function(value) {
                qrContainer.append('<tr>' +
                    '<td>' + value.id + '</td>' +
                    '<td>' + value.expired + '</td>' +
                    '<td>' + value.longitude + '</td>' +
                    '<td>' + value.latitude + '</td>' +
                    '<td>' +
                    '<button onclick="generateQRCode(\'' + value.id + '\')">Get QR Code</button>' +
                    '<button onclick="deleteQRCode(\'' + value.id + '\')">Delete</button>' +
                    '</td>' +
                    '</tr>');
            });
        },
        error: function(error) {
            console.error(error);
        }
    });
}

// Just toggles whether you can see the table of QR codes
function showQRCodes() {
    var qrContainer = $('.qr-container');
    var qrTableHead = $('.qr-table-head');

    if (qrContainer.css('display') === 'none') {
        qrContainer.css('display', 'table-row-group');
        qrTableHead.css('display', 'table-row-group');
    } else {
        qrContainer.css('display', 'none');
        qrTableHead.css('display', 'none');
    }
}