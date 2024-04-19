// Définition des variables de base pour le popup et le fond flou
var popup = document.querySelector(".popup");
var blurBackground = document.querySelector(".blur-background");

// Gestionnaire d'événements pour fermer la popup lorsque le fond flou est cliqué
blurBackground.addEventListener("click", function (event) {
  if (event.target === blurBackground) {
    popup.style.display = "none";
    blurBackground.style.display = "none";
  }
});

// Fonction pour ouvrir la popup
function openPopup() {
  popup.style.display = "block";
  document.body.style.overflow = "hidden";
  blurBackground.style.display = "block";
}

// Fonction pour fermer la popup
function closePopup() {
  popup.style.display = "none";
  document.body.style.overflow = "";
  blurBackground.style.display = "none";
}

// Attachement des écouteurs d'événements à des éléments de l'UI
document.getElementById("newChatButton").addEventListener("click", openPopup);
document.getElementById("searchInput").addEventListener("input", searchUsers);
document
  .querySelector(".search-container button")
  .addEventListener("click", searchUsers);
document.querySelectorAll(".invite-button").forEach((button) => {
  button.addEventListener("click", handleInviteButtonClick);
});
blurBackground.addEventListener("click", closePopup);

// Fonction pour chercher des utilisateurs et mettre à jour l'affichage des résultats
function searchUsers() {
  var searchText = document.getElementById("searchInput").value.toLowerCase();
  var users = document.querySelectorAll(".user-item");
  var searchResultDiv = document.getElementById("searchResult");
  searchResultDiv.innerHTML = ""; // Effacer les résultats précédents
  searchResultDiv.style.display = "none"; // Masquer le div en attendant

  // for (let user of users) {
  //   var name = user.querySelector(".user-name").textContent.toLowerCase();
  //   if (searchText && name.includes(searchText)) {
  //     var userClone = user.cloneNode(true); // Cloner l'élément trouvé
  //     userClone
  //       .querySelector(".invite-button")
  //       .addEventListener("click", handleInviteButtonClick);
  //     searchResultDiv.appendChild(userClone); // Ajouter le clone au div de résultat
  //     searchResultDiv.style.display = ""; // Afficher le div de résultat
  //     break; // Sortir après avoir trouvé le premier utilisateur correspondant
  //   }
  // }
}

// Gestionnaire pour les clics sur les boutons d'invitation
function handleInviteButtonClick(event) {
  const userItem = event.target.closest(".user-item");
  const userName = userItem.querySelector(".user-name").textContent;
  const isInvited = event.target.textContent === "Invite";

  event.target.textContent = isInvited ? "✖" : "Invite";
  event.target.style.backgroundColor = isInvited ? "red" : "#4CAF50";

  if (isInvited) {
    removeFromUserList(userName);
    userItem.querySelector(".invite-button").textContent = "✖";
    userItem.querySelector(".invite-button").style.backgroundColor = "red";
    document.getElementById("invitedUsers").appendChild(userItem);
  } else {
    removeFromInvitedList(userName);
    userItem.querySelector(".invite-button").textContent = "Invite";
    userItem.querySelector(".invite-button").style.backgroundColor = "#4CAF50";
    document.getElementById("user-list").appendChild(userItem);
  }
  document.getElementById("searchInput").value = ""; // Clear the search input
}

// Fonction pour retirer un utilisateur de la liste des utilisateurs non invités
function removeFromUserList(userName) {
  var items = document.querySelectorAll("#user-list .user-item");
  items.forEach(function (item) {
    if (item.querySelector(".user-name").textContent === userName) {
      item.remove();
    }
  });
}

// Fonction pour retirer un utilisateur de la liste des utilisateurs invités
function removeFromInvitedList(userName) {
  var items = document.querySelectorAll("#invitedUsers .user-item");
  items.forEach(function (item) {
    if (item.querySelector(".user-name").textContent === userName) {
      item.remove();
    }
  });
}

// stabiliser le bouton create
var createChatButton = document.querySelector(".start-button");
createChatButton.addEventListener("mousedown", function (event) {
  event.preventDefault(); // Empêche le navigateur de traiter l'interaction standard
});

createChatButton.addEventListener("click", function (event) {
  // var users = document.querySelectorAll(".user-item");
  var items = document.querySelectorAll("#invitedUsers .user-item");
  var data = { participants: ["a"] };
  items.forEach(function (item) {
    data.participants.push(item.querySelector(".user-name").textContent);
  });
  console.log(data.participants);

  fetch("/api/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(data),
  }).then((data) => {
    popup.style.display = "none";
    blurBackground.style.display = "none";
    load_chats();
  });
});

async function fetchFrom(link) {
  try {
    const response = await fetch(link);
    if (!response.ok) {
      throw new Error("Failed to fetch chats");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching messages:", error);
    return [];
  }
}

fetchFrom("/api/friends/").then((data) => {
  for (friend in data) {
    console.log("friend " + data[friend].username);

    const username = data[friend].username;
    add_user(username, "user-list", "invite", "#4CAF50");
  }
});

function add_user(username, list, text, color) {
  removeFromInvitedList(username);
  removeFromUserList(username);
  fetch("/api/profile_pic/" + username + "/")
    .then((response) => response.blob())
    .then((blob) => {
      // Convert the blob to a base64 encoded string
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
    })
    .then((data) => {
      var userItem = document.createElement("div");
      userItem.classList.add("user-item");
      var img = document.createElement("img");
      img.src = data;
      img.alt = username;
      img.classList.add("user-image");
      userItem.appendChild(img);
      var div_username = document.createElement("div");
      div_username.textContent = username;
      div_username.classList.add("user-name");
      userItem.appendChild(div_username);
      var invite_button = document.createElement("button");
      invite_button.textContent = text;
      invite_button.style.backgroundColor = color;
      invite_button.classList.add("invite-button");
      userItem.appendChild(invite_button);
      invite_button.addEventListener("click", handleInviteButtonClick);
      document.getElementById(list).appendChild(userItem);
    });
}

var searchBox = document.getElementById("searchInput");

document
  .getElementById("searchBtn")
  .addEventListener("click", function (event) {
    if (!searchBox.value) return;
    fetch("/api/exist/" + searchBox.value + "/")
      .then((response) => response.json())
      .then((data) => {
        console.log("API response:", data);
        if (data) {
          add_user(searchBox.value, "invitedUsers", "✖", "red");
        } else {
          throw new Error("User does not exist");
        }
      })
      .catch((error) => {
        displayError(error.message || "Error during the user invitation.");
      });
  });

/*
<div class="user-item">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQb2KRrG26uJLRrL55aWnKPGezf8V5ZkiHPHg&s"
        alt="Dark_Sasuke" class="user-image">
    <span class="user-name">Dark_Sasuke</span>
    <button class="invite-button">Invite</button>
</div>
*/
