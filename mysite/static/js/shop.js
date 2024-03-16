document.addEventListener('DOMContentLoaded', function() {
    const tableBody = document.getElementById('shop-table');
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
                element.classList.add(value);
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
     * Sends a request to the endpoint to retrieve all the shop data, creating the elements and
     * setting them inside the shop table
     *
     * @author Jasper
     */
    function getData() {
        fetch(`/api/shop/`)
            .then(response => response.json())
            .then(data => {
                tableBody.innerHTML = '';

                data.forEach(item => {
                    let button = createElement('button', { value: `${item.item_id}-${item.item_type}`, textContent: 'Buy' }, [])
                    if (item.price > USER_COINS) {
                        button = createElement('button', { disabled: true, value: `${item.item_id}-${item.item_type}`, textContent: 'Cannot afford' }, [])
                    }

                    var item_shop_name = `${item.name} ${types[item.item_type]}`
                    const row =
                        createElement('tr', {}, [
                            createElement('td', {}, [
                                createElement('b', { textContent: item_shop_name})
                            ]),
                            createElement('td', {}, [
                                createElement('b', { textContent: item.price})
                            ]),
                            button
                        ]);

                    tableBody.appendChild(row);
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
                console.log(data['coins']);
                USER_COINS = data['coins'];
                document.getElementsByClassName('coins-title')[0].innerHTML = `COINS: ${data['coins']}`;
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