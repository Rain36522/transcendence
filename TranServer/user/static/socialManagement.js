var users = [
  { username: "Lolita564", imageUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzO65Lpx5OR_-M92O1otaGdIt6nsTKfii_Bg&usqp=CAU", online: true, blocked: false },
  { username: "Famacito", imageUrl: "https://risibank.fr/cache/medias/0/13/1326/132676/full.png", online: false, blocked: true },
  { username: "Mania_xLeaderz", imageUrl: "https://cdn.gonzague.me/wp-content/uploads/2012/06/146646811-1200x900.gif", online: true, blocked: false }
];

document.addEventListener('DOMContentLoaded', function () {
  // Attacher les événements pour la recherche et le bouton Go!
  var searchButton = document.querySelector('.search-area button');
  var searchInput = document.getElementById('search-box');

  searchButton.addEventListener('click', searchUser);  // Écouteur pour le bouton Go!
  searchInput.addEventListener('input', searchUser);  // Écouteur pour la saisie

  displayUsers(users); // Affiche tous les utilisateurs au chargement initial
});

// Fonction pour chercher des utilisateurs basée sur le texte saisi
function searchUser() {
  var searchText = document.getElementById('search-box').value.toLowerCase();
  var filteredUsers = users.filter(user => user.username.toLowerCase().includes(searchText));
  displayUsers(filteredUsers);
}

// Fonction pour afficher les utilisateurs dans la liste
function displayUsers(filteredUsers) {
  var userList = document.querySelector('.user-list');
  userList.innerHTML = ''; // Nettoie la liste existante

  filteredUsers.forEach(user => {
    var userElement = document.createElement('li');
    userElement.className = 'user-item';
    userElement.innerHTML = `
          <div class="user-info">
              <img src="${user.imageUrl}" alt="${user.username}" class="user-image">
              <span class="user-name">${user.username}</span>
              <button onclick="toggleBlock('${user.username}')">${user.blocked ? 'Unblock' : 'Block'}</button>
          </div>
      `;
    userList.appendChild(userElement);
  });
}

// Fonction pour basculer l'état de blocage des utilisateurs
function toggleBlock(username) {
  var user = users.find(u => u.username === username);
  user.blocked = !user.blocked;
  searchUser(); // Rafraîchir l'affichage après modification de l'état
}
