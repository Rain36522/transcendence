var users = [];

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

async function update_all() {
  update_user(await fetchFrom("/api/friends/"), "friend");
  update_user(await fetchFrom("/api/blocked/"), "blocked");
  update_user(await fetchFrom("/api/invite/"), "waiting");
  update_user(await fetchFrom("/api/pending_invite/"), "pending");
}

function update_user(data, type) {
  for (var user in data) {
    console.log(data[user]); // Log the actual user object
    users.push({ username: data[user].username, status: type });
  }
}

function refresh_view() {
  users = [];
  update_all().then((data) => {
    console.log(users);
    displayUsers(users);
  });
}
refresh_view();

var searchBox = document.querySelector(".search-box");
var dropdownMenu = document.createElement("div");
dropdownMenu.classList.add("dropdown-menu");
document.querySelector(".search-selection").appendChild(dropdownMenu);

function update_search_box() {
  var searchText = searchBox.value.toLowerCase();
  if (!searchText) {
    dropdownMenu.innerHTML = "";
    return;
  }
  fetchFrom("/api/search/" + searchText + "/")
    .then((data) => {
      // Clear previous dropdown items
      dropdownMenu.innerHTML = "";
      // Loop through fetched data and create dropdown items
      data.usernames.forEach((item) => {
        const autocompleteItem = document.createElement("div");
        autocompleteItem.classList.add("autocomplete-item");
        autocompleteItem.textContent = item;
        autocompleteItem.addEventListener("click", function () {
          // Set search bar value to the selected item
          searchBox.value = item;
          // Clear autocomplete dropdown
          dropdownMenu.innerHTML = "";
        });
        dropdownMenu.appendChild(autocompleteItem);
      });
    })
    .catch((error) => {
      console.error("Error fetching data: ", error);
    });
}

document.getElementById("invite_btn").addEventListener("click", function () {
  if (searchBox.value == "") return;
  fetch("/api/exist/" + searchBox.value + "/")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      if (data) {
        addFriend(searchBox.value);
        refresh_view();
      } else console.log("user does not exist");
    });
});

document.getElementById("block_btn").addEventListener("click", function () {
  if (searchBox.value == "") return;
  fetch("/api/exist/" + searchBox.value + "/")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (data) {
        blockUser(searchBox.value);
        refresh_view();
      } else console.log("user does not exist");
    });
});

searchBox.addEventListener("input", function () {
  update_search_box();
});
searchBox.addEventListener("click", function () {
  update_search_box();
});

function updateExistingUserElement(li, user) {
  //   li.querySelector(
  //     ".user-photo"
  //   ).style.backgroundImage = `url('${user.imageUrl}')`;
  li.querySelector(".username").textContent = user.username;
  const actionButtons = getActionButtons(user);
  const buttonContainer = li.querySelector(".action-buttons");
  if (!buttonContainer) {
    // Si l'élément des boutons n'existe pas, on le crée.
    li.innerHTML += `<div class="action-buttons">${actionButtons}</div>`;
  } else {
    buttonContainer.innerHTML = actionButtons;
  }
}

function displayUsers(users) {
  clearLists();
  users.forEach(function (user) {
    let li = document.querySelector(`li[data-username='${user.username}']`); // Recherche d'un élément existant
    if (!li) {
      // Si l'élément n'existe pas, créez un nouveau
      li = createUserElement(user);
    } else {
      // Mise à jour de l'élément existant
      updateExistingUserElement(li, user);
    }
    switch (user.status) {
      case "friend":
        document.querySelector(".friends-list").appendChild(li);
        break;
      case "pending":
        document.querySelector(".pending-list").appendChild(li);
        break;
      case "blocked":
        document.querySelector(".blocked-list").appendChild(li);
        break;
      case "waiting":
        document.querySelector(".waiting-approval-list").appendChild(li);
        break;
    }
  });
}

function clearLists() {
  document.querySelector(".friends-list").innerHTML = "";
  document.querySelector(".pending-list").innerHTML = "";
  document.querySelector(".blocked-list").innerHTML = "";
}

function createUserElement(user) {
  var li = document.createElement("li");
  li.className = "user-item";
  li.setAttribute("data-username", user.username);
  /*
<div class="user-photo" style="background-image: url('${
          user.imageUrl
        }');"></div>
  */
  li.innerHTML = `
        
        <span class="username">${user.username}</span>
        <div class="action-buttons">${getActionButtons(user)}</div>
    `;
  return li;
}

function getActionButtons(user) {
  switch (user.status) {
    case "waiting":
      return `
                <button class="button approve-button user-button" onclick="approveUser('${user.username}')">Approve</button>
                <button class="button decline-button user-button" onclick="declineUser('${user.username}')">Decline</button>
            `;
    case "friend":
      return `<button class="button remove-button" onclick="removeFriend('${user.username}')">Remove</button>`;
    case "pending":
      return `<button class="button request-sent-button" onclick="cancelRequest('${user.username}')">Cancel Request</button>`;
    case "blocked":
      return `<button class="button unblock-button" onclick="unblockUser('${user.username}')">Unblock</button>`;
    default:
      return `
                <button class="button add-button user-button" onclick="addFriend('${user.username}')">Add</button>
                <button class="button block-button user-button" onclick="blockUser('${user.username}')">Block</button>
            `;
  }
}

function approveUser(username) {
  doRequest("friends", "POST", username);
}

function declineUser(username) {
  doRequest("invite", "DELETE", username);
}

function addFriend(username) {
  doRequest("invite", "POST", username);
}

function doRequest(path, method, username) {
  console.log("THIS RUNS");
  fetch("/api/" + path + "/" + username + "/", {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  }).then((data) => {
    refresh_view();
  });
}

function blockUser(username) {
  doRequest("blocked", "POST", username);
}

function cancelRequest(username) {
  doRequest("undo_invite", "DELETE", username);
}

function removeFriend(username) {
  doRequest("friends", "DELETE", username);
}

function unblockUser(username) {
  doRequest("blocked", "DELETE", username);
}