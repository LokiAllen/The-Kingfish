document.addEventListener('DOMContentLoaded', function() {
    const messagesDiv = document.getElementById('messages');
    const form = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    // Sends a GET request to get the messages
    function getMessages() {
        fetch(`/api/messages/${username}/`)
            .then(response => response.json())
            .then(data => {
                // Reverse the order (so that recent messages are at the bottom)
                data = data.reverse();
                messagesDiv.innerHTML = '';
                data.forEach(message => {
                    const messageDiv = document.createElement('div');

                    // Filters the messages to be placed by the CSS
                    if (username.toLowerCase() == message.sender_username.toLowerCase()) {
                        messageDiv.classList.add('receiver');
                    } else {
                        messageDiv.classList.add('sender');
                    }
                    messageDiv.textContent = message.content;
                    messagesDiv.appendChild(messageDiv);

                    // Set the scroll bar to the bottom (to view the recent messages)
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                });
            });
    }

    // Sends a POST request to send the message
    function sendMessage(content) {
        fetch(`/api/messages/${username}/`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN,
            },
            body: JSON.stringify({
                content: content
            }),
        })
        .then(response => response.json())
        .then(data => {
            getMessages();
        });
    }

    // Listens for sending a message
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const content = messageInput.value;
        sendMessage(content);
        messageInput.value = '';
    });

    getMessages();
});
