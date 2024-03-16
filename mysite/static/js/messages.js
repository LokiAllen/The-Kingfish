document.addEventListener('DOMContentLoaded', function() {
    const messagesDiv = document.getElementById('messages');
    const form = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    /**
     * Gets the minutes betwenen two specific dates, used to group messages send within the hour
     *
     * @param laterDate     The later data
     * @param earlierDate   The earlier data
     * @returns {number}    The minute difference
     */
    function minutesBetweenDates(laterDate, earlierDate) {
        const difference = laterDate.getTime() - earlierDate.getTime();
        console.log(difference / 1000 / 60);
        return difference / 1000 / 60;
    }

    /**
     * Used to take in all messages, and group those that were sent within an
     * hour of each other
     *
     * @param messages  The list of all messages
     * @returns {*[]}   The list of all messages including a list of grouped messages
     */
    function groupMessages(messages) {
        const grouped = [];
        let currentGroup = [];
        let lastSender = null;
        let lastTimestamp = null;

        messages.forEach(message => {
            const messageTimestamp = new Date(message.timestamp);

            if (lastSender !== message.sender ||
                (lastTimestamp !== null && minutesBetweenDates(messageTimestamp, lastTimestamp) > 60) ||
                currentGroup.length === 0) {
                if (currentGroup.length > 0) {
                    grouped.push([...currentGroup]);
                    currentGroup = [];
                }
                lastSender = message.sender;
            }

            currentGroup.push(message);
            lastTimestamp = messageTimestamp;
        });

        // Push the last group if it's not empty
        if (currentGroup.length > 0) {
            grouped.push(currentGroup);
        }
        console.log(grouped);
        return grouped;
    }

    /**
     * Fetches all the messages, creating the message elements and setting them inside
     * the document
     */
    function getMessages() {
        fetch(`/api/messages/${username}/`)
            .then(response => response.json())
            .then(data => {
                // Reverse the order (so that recent messages are at the bottom)
                data = data.reverse();
                const groupedMessages = groupMessages(data);
                messagesDiv.innerHTML = '';

                groupedMessages.forEach(group => {
                    const timestamp = document.createElement('p');
                    let temp = new Date(group[group.length-1].timestamp);
                    timestamp.textContent = temp.toLocaleTimeString().substr(0,5);

                    if (group.length > 1) {
                        const groupMessageDiv = document.createElement('div');
                        groupMessageDiv.classList.add('grouped-messages');
                        if (username.toLowerCase() == group[0].sender_username.toLowerCase()) {
                            classToAdd = 'receiver';
                            //groupMessageDiv.classList.add('receiver');
                        } else {
                            classToAdd = 'sender';
                            groupMessageDiv.id = 'group-sender'
                        }

                        group.forEach(message => {
                            const messageDiv = document.createElement('div');
                            messageDiv.textContent = message.content;
                            messageDiv.classList.add(classToAdd);
                            groupMessageDiv.appendChild(messageDiv);
                        })
                        timestamp.classList.add(classToAdd + '-time');
                        groupMessageDiv.appendChild(timestamp);
                        messagesDiv.appendChild(groupMessageDiv)
                    } else {
                        const messageDiv = document.createElement('div');
                        if (username.toLowerCase() == group[0].sender_username.toLowerCase()) {
                            messageDiv.classList.add('receiver');
                            timestamp.classList.add('receiver-time')
                        } else {
                            messageDiv.classList.add('sender');
                            timestamp.classList.add('sender-time')
                        }
                        messageDiv.textContent = group[0].content;
                        messagesDiv.appendChild(messageDiv);
                        messagesDiv.appendChild(timestamp);
                    }

                    // Set the scroll bar to the bottom (to view the recent messages)
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                })

            });
    }

    /**
     * Sends a request to the endpoint to send a message
     *
     * @param content   The message content
     */
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
