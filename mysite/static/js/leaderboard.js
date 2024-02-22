// Gets the leaderboard data and writes it to the table relative to how many users to show
function get_leaderboard_data() {
    var leaderboard_table = $('#leaderboard-table');
    var num_users = $('#dataInput').val();

    $.ajax({
        url: '/leaderboard/',
        type: 'GET',
        data: {'num_users': num_users, 'page_loaded': true},
        success: function(data) {
            leaderboard_table.html('');
            data.top_n_users.forEach(function(user, index, array) {
                if (index === array.length - 1) {
                    leaderboard_table.append('<tr class="importantrow"><td><b>' + user.position + '</b></td><td><b>' + user.username + '</b></td><td><b>' + user.coins + '</tr>');
                } else {
                    leaderboard_table.append('<tr><td>' + user.position + '</td><td>' + user.username + '</td><td>' + user.coins + '</td></tr>');
                }
            });
        },
        error: function(error) {
            console.error(error);
        }
    });
}