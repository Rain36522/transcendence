var popup = document.querySelector('.popup');
var blurBackground = document.querySelector('.blur-background');

blurBackground.addEventListener('click', function (event) {
	if (event.target === blurBackground) {
		popup.style.display = 'none';
		blurBackground.style.display = 'none';
	}
});

function openPopup() {
	var popup = document.getElementById('popup');
	popup.style.display = 'block';
	document.body.style.overflow = 'hidden';
	document.querySelector('.blur-background').style.display = 'block';
}

function closePopup() {
	var popup = document.getElementById('popup');
	popup.style.display = 'none';
	document.body.style.overflow = '';
	document.querySelector('.blur-background').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
	const createButton = document.querySelector('.create-link');
	const blurBackground = document.querySelector('.blur-background');


	// Ecouteur d'événements pour le bouton "Create"
	createButton.addEventListener('click', function (event) {
		event.preventDefault();
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
			if (searchText && name.includes(searchText)) {
				var userClone = user.cloneNode(true); // Cloner l'élément trouvé
				userClone.addEventListener('click', handleInviteButtonClick);
				searchResultDiv.appendChild(userClone); // Ajouter le clone au div de résultat
				searchResultDiv.style.display = ''; // Afficher le div de résultat
				break; // Sortir après avoir trouvé le premier utilisateur correspondant
			}
		}
	}

	// Modifier l'écouteur d'événements pour utiliser la fonction searchUsers lors de la saisie
	document.getElementById('searchInput').addEventListener('input', searchUsers);


	document.querySelector('.search-container button').addEventListener('click', searchUsers);

	function handleInviteButtonClick(event) {
		const userItem = event.target.closest('.user-item');
		const userName = userItem.querySelector('.user-name').textContent; // Obtenir le nom d'utilisateur
		const isInvited = event.target.textContent === 'Invite';
	
		// Mettre à jour le texte du bouton et la couleur
		event.target.textContent = isInvited ? '✖' : 'Invite';
		event.target.style.backgroundColor = isInvited ? 'red' : '#4CAF50';
	
		const targetContainerId = isInvited ? 'invitedUsers' : 'user-list';
		const targetContainer = document.getElementById(targetContainerId);
		const sourceContainerId = isInvited ? 'user-list' : 'invitedUsers';
		const sourceContainer = document.getElementById(sourceContainerId);
	
		// Si on invite l'utilisateur, chercher et supprimer l'original de la liste des utilisateurs
		const sourceUserItems = sourceContainer.querySelectorAll('.user-item');
		sourceUserItems.forEach(function(item) {
			const itemUserName = item.querySelector('.user-name').textContent;
			if (itemUserName === userName) {
				item.remove(); // Enlever l'élément original du conteneur source
			}
		});
	
		// Ajouter l'utilisateur invité au conteneur cible
		targetContainer.appendChild(userItem);
	
		// Vider la barre de recherche
		document.getElementById('searchInput').value = '';
		// Masquer les résultats de recherche si nécessaire
		document.getElementById('searchResult').style.display = 'none';
		document.getElementById('searchResult').innerHTML = '';
	}
	
	document.querySelectorAll('.invite-button').forEach(button => {
		button.addEventListener('click', handleInviteButtonClick);
	});

	// Gestion du clic sur le fond flou pour fermer la popup
	blurBackground.addEventListener('click', function () {
		closePopup();
	});
});