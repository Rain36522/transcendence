// Définition des variables de base pour le popup et le fond flou
var popup = document.querySelector('.popup');
var blurBackground = document.querySelector('.blur-background');

// Gestionnaire d'événements pour fermer la popup lorsque le fond flou est cliqué
blurBackground.addEventListener('click', function (event) {
    if (event.target === blurBackground) {
        popup.style.display = 'none';
        blurBackground.style.display = 'none';
    }
});

// Fonction pour ouvrir la popup
function openPopup() {
    popup.style.display = 'block';
    document.body.style.overflow = 'hidden';
    blurBackground.style.display = 'block';
}

// Fonction pour fermer la popup
function closePopup() {
    popup.style.display = 'none';
    document.body.style.overflow = '';
    blurBackground.style.display = 'none';
}

// Attachement des écouteurs d'événements à des éléments de l'UI
document.getElementById('newChatButton').addEventListener('click', openPopup);
document.getElementById('searchInput').addEventListener('input', searchUsers);
document.querySelector('.search-container button').addEventListener('click', searchUsers);
document.querySelectorAll('.invite-button').forEach(button => {
    button.addEventListener('click', handleInviteButtonClick);
});
blurBackground.addEventListener('click', closePopup);

// Fonction pour chercher des utilisateurs et mettre à jour l'affichage des résultats
function searchUsers() {
    var searchText = document.getElementById('searchInput').value.toLowerCase();
    var users = document.querySelectorAll('.user-item');
    var searchResultDiv = document.getElementById('searchResult');
    searchResultDiv.innerHTML = ''; // Effacer les résultats précédents
    searchResultDiv.style.display = 'none'; // Masquer le div en attendant

    for (let user of users) {
        var name = user.querySelector('.user-name').textContent.toLowerCase();
        if (searchText && name.includes(searchText)) {
            var userClone = user.cloneNode(true); // Cloner l'élément trouvé
            userClone.querySelector('.invite-button').addEventListener('click', handleInviteButtonClick);
            searchResultDiv.appendChild(userClone); // Ajouter le clone au div de résultat
            searchResultDiv.style.display = ''; // Afficher le div de résultat
            break; // Sortir après avoir trouvé le premier utilisateur correspondant
        }
    }
}

// Gestionnaire pour les clics sur les boutons d'invitation
function handleInviteButtonClick(event) {
    const userItem = event.target.closest('.user-item');
    const userName = userItem.querySelector('.user-name').textContent;
    const isInvited = event.target.textContent === 'Invite';

    event.target.textContent = isInvited ? '✖' : 'Invite';
    event.target.style.backgroundColor = isInvited ? 'red' : '#4CAF50';

    if (isInvited) {
        removeFromUserList(userName);
        userItem.querySelector('.invite-button').textContent = '✖';
        userItem.querySelector('.invite-button').style.backgroundColor = 'red';
        document.getElementById('invitedUsers').appendChild(userItem);
    } else {
        removeFromInvitedList(userName);
        userItem.querySelector('.invite-button').textContent = 'Invite';
        userItem.querySelector('.invite-button').style.backgroundColor = '#4CAF50';
        document.getElementById('user-list').appendChild(userItem);
    }
    document.getElementById('searchInput').value = ''; // Clear the search input
}

// Fonction pour retirer un utilisateur de la liste des utilisateurs non invités
function removeFromUserList(userName) {
    var items = document.querySelectorAll('#user-list .user-item');
    items.forEach(function (item) {
        if (item.querySelector('.user-name').textContent === userName) {
            item.remove();
        }
    });
}

// Fonction pour retirer un utilisateur de la liste des utilisateurs invités
function removeFromInvitedList(userName) {
    var items = document.querySelectorAll('#invitedUsers .user-item');
    items.forEach(function (item) {
        if (item.querySelector('.user-name').textContent === userName) {
            item.remove();
        }
    });
}

// stabiliser le bouton create
const createChatButton = document.querySelector('.start-button');
createChatButton.addEventListener('mousedown', function (event) {
    event.preventDefault(); // Empêche le navigateur de traiter l'interaction standard
});
