var popup = document.querySelector(".popup");
var blurBackground = document.querySelector(".blur-background");

blurBackground.addEventListener("click", function (event) {
  if (event.target === blurBackground) {
    popup.style.display = "none";
    blurBackground.style.display = "none";
  }
});

function openPopup() {
  var popup = document.getElementById("popup");
  popup.style.display = "block";
  document.body.style.overflow = "hidden";
  document.querySelector(".blur-background").style.display = "block";
}

function closePopup() {
  var popup = document.getElementById("popup");
  popup.style.display = "none";
  document.body.style.overflow = "";
  document.querySelector(".blur-background").style.display = "none";
}

var createButton = document.querySelector(".create-link");

createButton.addEventListener("click", function (event) {
  event.preventDefault();
  openPopup();
});

function searchUsers() {
  var searchText = document.getElementById("searchInput").value.toLowerCase();
  var users = document.querySelectorAll(".user-item");
  var searchResultDiv = document.getElementById("searchResult");
  searchResultDiv.innerHTML = "";
  searchResultDiv.style.display = "none";

  for (let user of users) {
    var name = user.querySelector(".user-name").textContent.toLowerCase();
    if (searchText && name.includes(searchText)) {
      var userClone = user.cloneNode(true);
      userClone.addEventListener("click", handleInviteButtonClick);
      searchResultDiv.appendChild(userClone);
      searchResultDiv.style.display = "";
      break;
    }
  }
}

document.getElementById("searchInput").addEventListener("input", searchUsers);

document
  .querySelector(".search-container button")
  .addEventListener("click", searchUsers);

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

document.querySelectorAll(".invite-button").forEach((button) => {
  button.addEventListener("click", handleInviteButtonClick);
});

blurBackground.addEventListener("click", function () {
  closePopup();
});


// To modify : user list created for testing!
const usersData = [
  {
    name: "Famacito",
    image: "https://media1.tenor.com/m/xK38NWayRnoAAAAC/dog-eyes.gif"
  },
  {
    name: "Dark_Sasuke",
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQb2KRrG26uJLRrL55aWnKPGezf8V5ZkiHPHg&s"
  }
];

function createUserItem(user) {
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

function populateUserList() {
  const userListContainer = document.getElementById("user-list");
  userListContainer.innerHTML = ""; // Clear previous entries
  usersData.forEach(user => {
    userListContainer.appendChild(createUserItem(user));
  });
}

document.addEventListener("DOMContentLoaded", populateUserList); // Populate users when the document is loaded
