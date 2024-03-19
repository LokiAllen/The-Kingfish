/**
 * Sends a request to the endpoint to retrieve users data, setting their values
 * inside the table and making it visible
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
            document.getElementById('coins').placeholder = data.coins;
            document.getElementById('highscore').placeholder = data.highscore;
            document.getElementById('totalscore').placeholder = data.cumulativeScore;
            document.getElementById('gamekeeper').checked = data.is_staff;
            document.getElementById('admin').checked = data.is_superuser;
            document.getElementById('error').style = 'display: none;'
            document.getElementsByClassName('profile-board')[0].style = ''
        });
}

/**
 * Sends a request to the endpoint to update the values
 *
 * @author Jasper
 * @param item_id   The item and category id being purchased (in format 'item_id-cat_id'
 */
function updateValues() {
    const username = document.getElementById('username').innerHTML;
    const coins = document.getElementById('coins').value;
    const highscore = document.getElementById('highscore').value;
    const totalscore = document.getElementById('totalscore').value;
    const game_keeper = document.getElementById('gamekeeper').checked;
    const super_user = document.getElementById('admin').checked;

    const values = {'is_staff': game_keeper, 'is_superuser': super_user}

    if (coins) {
        values['coins'] = coins;
    };

    if (highscore) {
        values['highscore'] = highscore;
    };

    if (totalscore) {
        values['cumulativeScore'] = totalscore;
    };

    if (Object.keys(values).length === 0) {
        return
    }

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