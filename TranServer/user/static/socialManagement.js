var users = [
	{ username: "Lolita564", imageUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzO65Lpx5OR_-M92O1otaGdIt6nsTKfii_Bg&usqp=CAU", online: true, blocked: false },
	{ username: "Famacito", imageUrl: "https://risibank.fr/cache/medias/0/13/1326/132676/full.png", online: false, blocked: true },
	{ username: "Mania_xLeaderz", imageUrl: "https://cdn.gonzague.me/wp-content/uploads/2012/06/146646811-1200x900.gif", online: true, blocked: false }
];

function toggleBlock(index) {
users[index].blocked = !users[index].blocked;
updateUserStatusOnServer(users[index]); // Appel de la fonction pour mettre à jour sur le serveur
displayUsers(users); // Mise à jour de l'affichage
}

function updateUserStatusOnServer(user) {
fetch('/api/update-user-status', {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json',
		// Assurez-vous d'inclure des headers pour l'authentification si nécessaire
	},
	body: JSON.stringify({
		username: user.username,
		blocked: user.blocked
	})
})
.then(response => response.json())
.then(data => {
	console.log('Success:', data);
	// Vous pouvez également gérer la mise à jour de l'interface utilisateur ici si nécessaire
})
.catch((error) => {
	console.error('Error:', error);
});
}

function sendAllUserStatusesToServer() {
fetch('/api/bulk-update-user-status', {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json',
		// Assurez-vous d'inclure des headers pour l'authentification si nécessaire
	},
	body: JSON.stringify(users)  // Envoie de l'ensemble des utilisateurs avec leur statut bloqué/débloqué
})
.then(response => response.json())
.then(data => {
	console.log('Bulk update success:', data);
	// Ici vous pouvez afficher un message de confirmation ou autre feedback visuel
})
.catch((error) => {
	console.error('Bulk update error:', error);
});
}

function displayUsers(displayedUsers) {
	var userList = document.querySelector('.user-list');
	userList.innerHTML = ''; // Effacer la liste existante

	displayedUsers.forEach(function(user, index) {
		var li = document.createElement('li');
		var blockButtonLabel = user.blocked ? 'Unblock' : 'Block';
		li.innerHTML = `
			<div class="user-info">
				<div class="user-photo" style="background-image: url('${user.imageUrl}');"></div>
				<span class="username">${user.username}</span>
			</div>
			<button class="block-button" onclick="toggleBlock(${index})">${blockButtonLabel}</button>
		`;
		userList.appendChild(li);
	});
}

function filterAndDisplayUsers(query) {
	var filteredUsers = users.filter(function(user) {
		return user.username.toLowerCase().includes(query.toLowerCase());
	});
	displayUsers(filteredUsers); // Affiche uniquement les utilisateurs filtrés
}

document.addEventListener('DOMContentLoaded', function() {
	displayUsers(users); // Affiche tous les utilisateurs au chargement de la page

	var searchBox = document.querySelector('.search-box');
	var goButton = document.querySelector('.search-area button');

	// Écouter les entrées dans le champ de recherche
	searchBox.addEventListener('input', function() {
		filterAndDisplayUsers(searchBox.value);
	});

	// Écouter les clics sur le bouton Go!
	goButton.addEventListener('click', function() {
		filterAndDisplayUsers(searchBox.value);
	});
});