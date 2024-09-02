function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    const categoryNameInput = document.getElementById('new-category-name');
    const addCategoryBtn = document.getElementById('add-category-btn');

    addCategoryBtn.addEventListener('click', function() {
        createNewCategory();
    });

    categoryNameInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            createNewCategory();
        }
    });

    function createNewCategory() {
        const newCategoryName = categoryNameInput.value.trim();

        if (newCategoryName === "") {
            categoryNameInput.style.display = 'block';
            return;
        }

        saveCategoryToServer(newCategoryName)
            .then(success => {
                if (success) {
                    const menu = document.querySelector('.menu .item .submenu');
                    const newCategoryItem = document.createElement('div');
                    newCategoryItem.classList.add('submenu-item');

                    const newCategoryLink = document.createElement('a');
                    newCategoryLink.classList.add('submenu-link');
                    newCategoryLink.textContent = newCategoryName;

                    const newSubmenuLevel2 = document.createElement('div');
                    newSubmenuLevel2.classList.add('submenu-level-2');

                    ['Finish', 'Currently', 'Pause', 'To Begin'].forEach(function(subItemName) {
                        const formattedSubItemName = subItemName.toLowerCase().replace(/\s+/g, '-');
                        const subItem = document.createElement('div');
                        subItem.classList.add(`submenu-item-${formattedSubItemName}`);

                        const subItemLink = document.createElement('a');
                        subItemLink.classList.add('submenu-link');
                        subItemLink.textContent = subItemName;

                        subItem.appendChild(subItemLink);
                        newSubmenuLevel2.appendChild(subItem);
                    });

                    newCategoryItem.appendChild(newCategoryLink);
                    newCategoryItem.appendChild(newSubmenuLevel2);
                    menu.insertBefore(newCategoryItem, menu.querySelector('.submenu-newcategory'));

                    categoryNameInput.style.display = 'none';
                    categoryNameInput.value = '';
                } else {
                    alert('Failed to save category. You must be logged.');
                }
            });
    }
});

function saveCategoryToServer(categoryName) {
    const csrftoken = getCookie('csrftoken');

    return fetch('/create-category/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'category_name': categoryName
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            return true;
        } else {
            return false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
        return false;
    });
}