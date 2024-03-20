const itemTypes = {
    19: 'Title',
    23: 'Background'
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
 * setting them inside the shop table respective of the item type
 *
 * @author Jasper
 */
function getShopInfo() {
    fetch(`/api/data/shop/`)
        .then(response => response.json())
        .then(data => {
            const shopTable = document.getElementById('shop-container');
            shopTable.innerHTML = ''
            data.forEach(item => {
                const row = createElement('tr', {}, [
                    createElement('td', { classList: ['type-update'], textContent: itemTypes[item.item_type] }, []),
                    createElement('td', { classList: ['name-update'] }, [
                        createElement('span', { classList: ['input-info'], textContent: item.name }),
                        createElement('input', { type: 'text', placeholder: item.name })
                    ]),
                    createElement('td', { classList: ['description-update'] }, [
                        createElement('span', { classList: ['input-info'], textContent: item.description }),
                        createElement('input', { type: 'text', placeholder: item.description }),
                    ]),
                    createElement('td', { classList: ['price-update'] }, [
                        createElement('span', { classList: ['input-info'], textContent: item.price }),
                        createElement('input', { type: 'text', placeholder: item.price })
                    ]),
                    createElement('td', {}, [
                        createElement('button', { value: `${item.item_id}-${item.item_type}`, textContent: 'Update' }, []),
                    ]),
                ]);
                shopTable.appendChild(row);
            })
        });
}

/**
 * Sends a request to the endpoint for the user to purchase an item
 *
 * @author Jasper
 * @param item_id   The item and category id being purchased (in format 'item_id-cat_id'
 */
function updateValues(button) {
    const row = button.closest('tr');
    const type_id = button.value;
    const name = row.querySelector('.name-update input').value;
    const description = row.querySelector('.description-update input').value;
    const price = row.querySelector('.price-update input').value;

    const values = {}

    if (name) {
        values['name'] = name;
    };

    if (description) {
        values['description'] = description;
    };

    if (price) {
        values['price'] = price;
    };

    if (Object.keys(values).length === 0) {
        return
    }

    fetch(`/api/data/shop/${type_id}`, {
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


document.addEventListener('click', function (event) {
    if (event.target.nodeName == 'BUTTON' && event.target.innerHTML == 'Update') {
        updateValues(event.target);
    }
});