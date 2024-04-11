
var popup = document.querySelector('.popup');
var blurBackground = document.querySelector('.blur-background');

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
function closePopup() {
	let popup = document.getElementById('popup');
	popup.style.display = 'none';
	document.body.style.overflow = '';
	document.querySelector('.blur-background').style.display = 'none';
}

var newChatButton = document.getElementById('newChatButton');
var inviteButtons = document.querySelectorAll('.invite-button');
var popup = document.getElementById('popup');
var blurBackground = document.querySelector('.blur-background');
var searchInput = document.getElementById('searchInput');
var searchButton = document.querySelector('.search-container button');
var userItems = document.querySelectorAll('.user-item');

newChatButton.addEventListener('click', function (event) {
	openPopup();
});

function searchUsers() {
	var searchText = document.getElementById('searchInput').value.toLowerCase();
	var users = document.querySelectorAll('.user-item');
	var searchResultDiv = document.getElementById('searchResult');
	searchResultDiv.innerHTML = ''; // Effacer les résultats précédents
	searchResultDiv.style.display = 'none'; // Masquer le div en attendant

	for (let user of users) {
		var name = user.querySelector('.user-name').textContent.toLowerCase();
		if (name.includes(searchText)) {
			var userClone = user.cloneNode(true); // Cloner l'élément trouvé
			searchResultDiv.appendChild(userClone); // Ajouter le clone au div de résultat
			searchResultDiv.style.display = ''; // Afficher le div de résultat
			break; // Sortir après avoir trouvé le premier utilisateur correspondant
		}
	}
}

// Modifier l'écouteur d'événements pour utiliser la fonction searchUsers lors de la saisie
document.getElementById('searchInput').addEventListener('input', searchUsers);


document.querySelector('.search-container button').addEventListener('click', searchUsers);

// Ecouteur d'événements pour les boutons "Invite"
function handleInviteButtonClick(event) {
    const userItem = event.target.closest('.user-item');
    const clonedUserItem = userItem.cloneNode(true);
    const userName = userItem.querySelector('.user-name').textContent; // Get the username
    const isInvited = event.target.textContent === 'Invite';

    // Update the button text and color
    event.target.textContent = isInvited ? '✖' : 'Invite';
    event.target.style.backgroundColor = isInvited ? 'red' : '#4CAF50';

    const targetContainerId = isInvited ? 'invitedUsers' : 'user-list';
    const targetContainer = document.getElementById(targetContainerId);

    if (isInvited && targetContainerId === 'invitedUsers') {
        // If inviting the user, search for and remove the original from the user list
        const originalUserItems = document.querySelectorAll('#user-list .user-item');
        originalUserItems.forEach(function (item) {
            const itemUserName = item.querySelector('.user-name').textContent;
            if (itemUserName === userName) {
                item.remove(); // Remove the original item from the user list
            }
        });
    }

    targetContainer.appendChild(userItem); // Add the invited user to the target container
}

// Attach the event listener directly to each invite-button
document.querySelectorAll('.invite-button').forEach(button => {
    button.addEventListener('click', handleInviteButtonClick);
});

// Gestion du clic sur le fond flou pour fermer la popup
blurBackground.addEventListener('click', function () {
	closePopup();
});


function updateScrollbars() {
	const userListContainer = document.getElementById('user-list');
	const invitedUsersContainer = document.getElementById('invitedUsers');

	if (userListContainer.children.length === 0) {
		userListContainer.style.overflowY = 'hidden';
	} else {
		userListContainer.style.overflowY = 'auto';
	}

	if (invitedUsersContainer.children.length === 0) {
		invitedUsersContainer.style.overflowY = 'hidden';
	} else {
		invitedUsersContainer.style.overflowY = 'auto';
	}
}

// Appelez cette fonction après toute opération qui modifie le nombre d'utilisateurs invités
updateScrollbars();
