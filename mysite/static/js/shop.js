document.addEventListener('DOMContentLoaded', function() {
    const backgroundsBody = document.getElementById('shop-backgrounds');
    const titlesBody = document.getElementById('shop-titles');
    const types = {
        19: 'Title',
        23: 'Background',
    }

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
                element[key] = value
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
     * Groups titles together as they are shown in divs of two titles
     *
     * @author Jasper
     * @param titles    The array of titles to group
     * @returns {*[]}   An array of 2d arrays of titles
     */
    function groupTitles(titles) {
        const grouped = [];

        for (let i=0; i < titles.length; i+=2) {
            grouped.push(titles.slice(i, i+2));
        }

        return grouped;
    }

    /**
     * Sends a request to the endpoint to retrieve all the shop data, creating the elements and
     * setting them inside the shop table respective of the item type
     *
     * @author Jasper
     */
    function getData() {
        fetch(`/api/shop/`)
            .then(response => response.json())
            .then(data => {
                const titles = []
                const backgrounds = []
                const css_names = {
                    'First Penguin': 'penguin_one',
                    'Second Penguin': 'penguin_two',
                };

                data.forEach(item => {
                    if (item.item_type == 19) {
                        titles.push(item);
                    } else if (item.item_type == 23) {
                        backgrounds.push(item);
                    }
                });

                groupedTitles = groupTitles(titles);

                titlesBody.innerHTML = ''
                backgroundsBody.innerHTML = ''

                groupedTitles.forEach(group => {
                    const titleSection = createElement('div', {'classList': ['tt-section']}, [])

                    group.forEach(item => {
                        if (item.owned) {
                            var button = createElement('button', { disabled: true, value: `${item.item_id}-${item.item_type}`, textContent: 'OWNED', 'classList': ['tt-buy']}, [])
                        }
                        else if (item.price > USER_COINS) {
                            var button = createElement('button', { disabled: true, value: `${item.item_id}-${item.item_type}`, textContent: 'BUY', 'classList': ['tt-buy']}, [])
                        }
                        else {
                            var button = createElement('button', { value: `${item.item_id}-${item.item_type}`, textContent: 'BUY', 'classList': ['tt-buy']}, [])
                        }

                        const titleItem =
                            createElement('div', {'classList': ['tt-card']}, [
                                createElement('div', {'classList': ['tt-card-overlay']}),
                                createElement('div', {'classList': ['tt-card-inner']}, [
                                    createElement('p', {textContent: item.name.toUpperCase()}, []),
                                    createElement('p', {textContent: `${item.price}Ȼ`}, []),
                                    button,
                                ])
                            ]);

                        titleSection.appendChild(titleItem);
                    });

                    titlesBody.appendChild(titleSection);
                });

                backgrounds.forEach(item => {
                    let button = createElement('button', {textContent: 'BUY', 'classList': ['bg-buy'], value: `${item.item_id}-${item.item_type}`}, [])
                    if (item.owned || item.price > USER_COINS) {
                        if (item.owned) {
                            text = 'OWNED'
                        } else {
                            text = 'BUY'
                        }

                        button = createElement('button', { disabled: true, value: `${item.item_id}-${item.item_type}`, textContent: text, 'classList': ['bg-buy']}, [])
                    }

                    var cssName = item.name;
                    if (['First Penguin', 'Second Penguin'].includes(cssName)) {
                        cssName = css_names[cssName];
                        item.name = 'Penguin'
                    }

                    const background_item =
                        createElement('div', {'classList': ['bg-card']}, [
                            createElement('div', {'classList': ['card__image', cssName]}, []),
                            createElement('div', {'classList': ['card__content']}, [
                                createElement('div', {'classList': ['card__title']}, [
                                    createElement('p', {textContent: item.name}, []),
                                    createElement('p', {'classList': ['bg-cost'], textContent: `${item.price}Ȼ`}, [])
                                ]),
                                createElement('p', {'classList': ['card__describe']}, [
                                    button
                                ])
                            ])
                        ])

                    backgroundsBody.appendChild(background_item);
                });

            });
    }

    getData();

    /**
     * Sends a request to the endpoint for the user to purchase an item
     *
     * @author Jasper
     * @param item_id   The item and category id being purchased (in format 'item_id-cat_id'
     */
    function purchaseItem(item_id) {
        fetch(`/api/shop/`, {
            method: 'POST',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN,
            },
            body: JSON.stringify({
                item: item_id
            }),
        })
            .then(response => response.json())
            .then(data => {
                USER_COINS = data['coins'];
                document.getElementsByClassName('c-title')[0].innerHTML = `Coins: ${data['coins']}`;
                getData();
            });
    }

    /**
     * Event listener instead of direct on press functions for the buttons to allow the other
     * functions to more easily set the button types
     */
    document.addEventListener('click', function(event) {
        if (event.target.nodeName == 'BUTTON') {
            purchaseItem(event.srcElement.value);
        }
    });
});