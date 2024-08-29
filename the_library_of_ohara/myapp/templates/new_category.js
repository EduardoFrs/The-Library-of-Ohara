document.getElementById('add-category-btn').addEventListener('click', function() {
    var inputField = document.getElementById('new-category-name');

    // Affiche le champ d'entrée
    inputField.style.display = 'block';

    // Ajoute un événement pour ajouter la catégorie quand l'utilisateur appuie sur "Enter"
    inputField.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            var categoryName = inputField.value.trim();

            if (categoryName !== '') {
                // Créer un nouvel élément de sous-menu
                var newCategoryItem = document.createElement('div');
                newCategoryItem.classList.add('submenu-item');

                var newLink = document.createElement('a');
                newLink.classList.add('submenu-link');
                newLink.href = '#';
                newLink.textContent = categoryName;

                newCategoryItem.appendChild(newLink);

                // Ajouter le nouvel élément au menu
                var submenu = document.querySelector('.menu .submenu');
                submenu.insertBefore(newCategoryItem, submenu.lastElementChild);

                // Efface le champ d'entrée et le cache
                inputField.value = '';
                inputField.style.display = 'none';
            }
        }
    });
});

