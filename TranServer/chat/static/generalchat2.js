var popup = document.querySelector(".popup");
var blurBackground = document.querySelector(".blur-background");

blurBackground.addEventListener("click", function(event) {
    if (event.target === blurBackground) {
        popup.style.display = "none";
        blurBackground.style.display = "none";
    }
});

function openPopup() {
    popup.style.display = "block";
    document.body.style.overflow = "hidden";
    blurBackground.style.display = "block";
}

function closePopup() {
    popup.style.display = "none";
    document.body.style.overflow = "";
    blurBackground.style.display = "none";
}

document.getElementById("newChatButton").addEventListener("click", openPopup);
document.getElementById("searchInput").addEventListener("input", searchUsers);
document.querySelector(".search-container button").addEventListener("click", searchUsers);
document.querySelectorAll(".invite-button").forEach((button) => {
    button.addEventListener("click", handleInviteButtonClick);
});
blurBackground.addEventListener("click", closePopup);

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

function handleInviteButtonClick(event) {
    const userItem = event.target.closest(".user-item");
    const userName = userItem.querySelector(".user-name").textContent;
    const isInvited = event.target.textContent === "Invite";

    event.target.textContent = isInvited ? "✖" : "Invite";
    event.target.style.backgroundColor = isInvited ? "red" : "#4CAF50";

    if (isInvited) {
        removeFromUserList(userName);
        document.getElementById("invitedUsers").appendChild(userItem);
    } else {
        removeFromInvitedList(userName);
        document.getElementById("user-list").appendChild(userItem);
    }
    document.getElementById("searchInput").value = "";
}

function removeFromUserList(userName) {
    var items = document.querySelectorAll("#user-list .user-item");
    items.forEach(function(item) {
        if (item.querySelector(".user-name").textContent === userName) {
            item.remove();
        }
    });
}

function removeFromInvitedList(userName) {
    var items = document.querySelectorAll("#invitedUsers .user-item");
    items.forEach(function(item) {
        if (item.querySelector(".user-name").textContent === userName) {
            item.remove();
        }
    });
}

// Send the list to the server.
document.querySelector(".start-button").addEventListener("click", function() {
    var invitedUsers = document.querySelectorAll("#invitedUsers .user-item");
    var playerNames = Array.from(invitedUsers).map(user => user.querySelector(".user-name").textContent);

    var data = {
        players: playerNames
    };

    fetch('TODO: path-to-your-endpoint', { // To modify
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        closePopup(); 
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
