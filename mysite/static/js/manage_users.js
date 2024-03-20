/**
 * Sends a request to the endpoint to retrieve all the shop data, creating the elements and
 * setting them inside the shop table respective of the item type
 *
 * @author Jasper
 */
function getUserInfo() {
    const usernameInput = document.getElementById('dataInput').value;
    fetch(`/api/data/user/${usernameInput}`)
        .then(response => response.json())
        .then(data => {
            if (Object.keys(data).length === 0) {
                document.getElementById('error').style = ''
                return
            }

            document.getElementById('username').innerHTML = data.user_username;
            coins = document.getElementById('coins').placeholder = data.coins;
            highscore = document.getElementById('highscore').placeholder = data.highscore;
            totalscore = document.getElementById('totalscore').placeholder = data.cumulativeScore;

            document.getElementById('error').style = 'display: none;'
            document.getElementsByClassName('profile-board')[0].style = ''
        });
}

/**
 * Sends a request to the endpoint for the user to purchase an item
 *
 * @author Jasper
 * @param item_id   The item and category id being purchased (in format 'item_id-cat_id'
 */
function updateValues() {
    username = document.getElementById('username').innerHTML;
    coins = document.getElementById('coins').value;
    highscore = document.getElementById('highscore').value;
    totalscore = document.getElementById('totalscore').value;
    values = {}

    if (coins) {
        values['coins'] = coins;
    };

    if (highscore) {
        values['highscore'] = highscore;
    };

    if (totalscore) {
        values['cumulativeScore'] = totalscore;
    };

    fetch(`/api/data/user/${username}`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN,
        },
        body: JSON.stringify(values),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
}