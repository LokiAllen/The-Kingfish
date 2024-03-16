function addFriend(username) {
    $.ajax({
        url: window.location.href,
        type: 'POST',
        data: {
            'method': 'add',
            csrfmiddlewaretoken: CSRF_TOKEN,
        },
        success: function(response) {
            location.reload();
        },
        error: function(error) {
            console.error('error');
        }
    });
}

function removeFriend(username) {
    $.ajax({
        url: window.location.href,
        type: 'POST',
        data: {
            'method': 'remove',
            csrfmiddlewaretoken: CSRF_TOKEN,
        },
        success: function(response) {
            location.reload();
        },
        error: function(error) {
            console.error('error');
        }
    });
}