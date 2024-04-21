setupInitialPlayerAmountOptions();
populateUserListTournament();  // Initialisation des listes d'utilisateurs pour le tournoi, si nécessaire
disableCreateButton();  // Désactive le bouton Create au chargement initial

document.getElementById("gamesettings").addEventListener("change", function() {
  updatePlayerAmountOptions();  // Met à jour les options de Player Amount
  enableCreateButtonIfNeeded();  // Active le bouton Create si les conditions sont remplies
});

function setupInitialPlayerAmountOptions() {
  var playerNumberSelect = document.getElementById("playerNumber");
  playerNumberSelect.innerHTML = "";  // Efface les options précédentes
  playerNumberSelect.appendChild(new Option("Select Player Amount", "", false, true));  // Ajoute une option par défaut désactivée
}

function populateUserListTournament() {
  const usersDataTournament = [
    {
      name: "Famacito",
      image: "https://media1.tenor.com/m/xK38NWayRnoAAAAC/dog-eyes.gif"
    },
    {
      name: "Dark_Sasuke",
      image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQb2KRrG26uJLRrL55aWnKPGezf8V5ZkiHPHg&s"
    }
  ];

  const userListContainer = document.getElementById("user-list");
  userListContainer.innerHTML = "";

  usersDataTournament.forEach(user => {
    userListContainer.appendChild(createUserItemTournament(user));
  });
}

function createUserItemTournament(user) {
  const userItem = document.createElement("div");
  userItem.className = "user-item";
  userItem.innerHTML = `
    <img src="${user.image}" alt="${user.name}" class="user-image">
    <span class="user-name">${user.name}</span>
    <button class="invite-button">Invite</button>
  `;
  userItem.querySelector(".invite-button").addEventListener("click", handleInviteButtonClick);
  return userItem;
}

function handleInviteButtonClick(event) {
  const userItem = event.target.closest(".user-item");
  const userName = userItem.querySelector(".user-name").textContent;
  const isInvited = event.target.textContent === "Invite";

  event.target.textContent = isInvited ? "✖" : "Invite";
  event.target.style.backgroundColor = isInvited ? "red" : "#4CAF50";

  const targetContainerId = isInvited ? "invitedUsers" : "user-list";
  const targetContainer = document.getElementById(targetContainerId);
  const sourceContainerId = isInvited ? "user-list" : "invitedUsers";
  const sourceContainer = document.getElementById(sourceContainerId);

  const sourceUserItems = sourceContainer.querySelectorAll(".user-item");
  sourceUserItems.forEach(function (item) {
    const itemUserName = item.querySelector(".user-name").textContent;
    if (itemUserName === userName) {
      item.remove();
    }
  });

  targetContainer.appendChild(userItem);

  document.getElementById("searchInput").value = "";
  document.getElementById("searchResult").style.display = "none";
  document.getElementById("searchResult").innerHTML = "";
}

function updatePlayerAmountOptions() {
  var gameSettings = document.getElementById("gamesettings");
  var playerNumberSelect = document.getElementById("playerNumber");
  var selectedGameMode = gameSettings.value;

  playerNumberSelect.innerHTML = "";
  var options = [];
  if (selectedGameMode === "2") {
    options = ["4", "8", "16"];
  } else if (selectedGameMode === "4") {
    options = ["8", "16"];
  } else if (selectedGameMode === "1") {
    options = ["4", "6", "8", "10", "12", "14", "16"];
  }

  options.forEach(function(option) {
    playerNumberSelect.appendChild(new Option(option, option));
  });

  playerNumberSelect.disabled = options.length === 0;
}

function disableCreateButton() {
    var createButton = document.querySelector(".create-button");
    createButton.classList.add('disabled'); // Ajoute une classe pour le style
    createButton.onclick = function(event) { event.preventDefault(); } // Empêche la navigation
}


function enableCreateButtonIfNeeded() {
  var gameSettings = document.getElementById("gamesettings");
  var createButton = document.querySelector(".create-button");
  if (gameSettings.value && gameSettings.value !== "") {
    createButton.disabled = false;
    createButton.classList.remove('disabled'); // Retire la classe pour réactiver le style visuel
  } else {
    createButton.disabled = true;
    createButton.classList.add('disabled'); // Ajoute la classe si nécessaire
  }
}
