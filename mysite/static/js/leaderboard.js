document.addEventListener('DOMContentLoaded', function () {
    const th_score_type = document.getElementById('th-score-type');
    const tableBody = document.getElementById('leaderboard-table');
    const leaderboard_types = ['global', 'friends'];
    const score_types = ['coins', 'cumulativeScore', 'highscore'];

    /**
     * To reduce repetitive code, creates a given element with corresponding
     * properties and child elements assigned to it
     *
     * @author Jasper
     * @param type          The element type to create
     * @param properties    The properties for the element, including a List of classes
     * @param children      The children elements to nest inside the created element
     * @returns             The created element alongside with its nested child elements
     * */
    function createElement(type, properties = {}, children = []) {
        const element = document.createElement(type);
        Object.entries(properties).forEach(([key, value]) => {
            if (key === 'textContent') {
                element.textContent = value;
            } else if (key === 'classList') {
                element.classList.add(...value);
            } else {
                element[key] = value;
            }
        });
        children.forEach(child => {
            if (typeof child === 'string') {
                element.appendChild(document.createTextNode(child));
            } else {
                element.appendChild(child);
            }
        });
        return element;
    }

    /**
     * Gets the leaderboard data relative to the parameters, creates the required elements
     * and sets them inside the leaderboard table
     *
     * @author Jasper, Daniel Banks
     * @param leaderboard_type  The leaderboard type to show (global/friends)
     * @param score_type        The score type to show (I.E highscore)
     */
    function getData(leaderboard_type, score_type) {
        fetch(`/api/data/leaderboard/${leaderboard_type}/${score_type}/`)
            .then(response => response.json())
            .then(data => {
                if (score_type == 'cumulativeScore') {
                    score_type = 'Cumulative Score';
                }

                th_score_type.textContent = score_type[0].toUpperCase() + score_type.slice(1);
                tableBody.innerHTML = '';

                data.forEach(user => {
                    const row =
                        createElement('tr', {}, [
                            createElement('td', {}, [
                                createElement('h5', { textContent: user.position })
                            ]),
                            createElement('td', { classList: ['name-box'] }, [
                                createElement('img', { src: user.picture }),
                                createElement('div', {}, [
                                    createElement('a', { href: `../accounts/profile/${user.user_username}` }, [
                                        createElement('h5', { textContent: user.user_username }),
                                        createElement('h6', { textContent: user.title_name })
                                    ])
                                ])
                            ]),
                            createElement('td', {}, [
                                createElement('h3', { textContent: user.value })
                            ])
                        ]);

                    tableBody.appendChild(row);
                });

            });
    }

    if (!(localStorage.getItem('leaderboard_type'))) {
        localStorage.setItem('leaderboard_type', 'global');
    }

    if (!(localStorage.getItem('score_type'))) {
        localStorage.setItem('score_type', 'coins');
    }
    getData('global', 'coins');

    /**
     * Event listener instead of direct on press functions for the buttons to allow the other
     * functions to more easily set the button types
     */
    document.addEventListener('click', function (event) {

        var value = event.srcElement.value;

        // Checks whether it is setting the score type or leaderboard type value
        if (score_types.includes(value)) {
            var leaderboard_type = localStorage.getItem('leaderboard_type');
            var score_type = value;
            localStorage.setItem('score_type', value);

        } else if (leaderboard_types.includes(value)) {
            var score_type = localStorage.getItem('score_type');
            var leaderboard_type = value;
            localStorage.setItem('leaderboard_type', value);

        } else {
            return
        }

        getData(leaderboard_type, score_type);
    });
});
