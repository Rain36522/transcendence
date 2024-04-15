var users = [
    // Utilisateurs "Friends"
    { username: "Alice", imageUrl: "https://example.com/img1.jpg", status: "friend" },
    { username: "Bob", imageUrl: "https://example.com/img2.jpg", status: "friend" },
    { username: "Charlie", imageUrl: "https://example.com/img3.jpg", status: "friend" },
    { username: "David", imageUrl: "https://example.com/img4.jpg", status: "friend" },
    { username: "Eve", imageUrl: "https://example.com/img5.jpg", status: "friend" },

    // Utilisateurs "Pending"
    { username: "Fiona", imageUrl: "https://example.com/img6.jpg", status: "pending" },
    { username: "George", imageUrl: "https://example.com/img7.jpg", status: "pending" },
    { username: "Hannah", imageUrl: "https://example.com/img8.jpg", status: "pending" },
    { username: "Ivan", imageUrl: "https://example.com/img9.jpg", status: "pending" },
    { username: "Julia", imageUrl: "https://example.com/img10.jpg", status: "pending" },

    // Utilisateurs "Blocked"
    { username: "Kevin", imageUrl: "https://example.com/img11.jpg", status: "blocked" },
    { username: "Luna", imageUrl: "https://example.com/img12.jpg", status: "blocked" },
    { username: "Mia", imageUrl: "https://example.com/img13.jpg", status: "blocked" },
    { username: "Noah", imageUrl: "https://example.com/img14.jpg", status: "blocked" },
    { username: "Olivia", imageUrl: "https://example.com/img15.jpg", status: "blocked" },

    // Utilisateurs "Waiting for Approval"
    { username: "Pablo", imageUrl: "https://example.com/img16.jpg", status: "waiting" },
    { username: "Quinn", imageUrl: "https://example.com/img17.jpg", status: "waiting" },
    { username: "Rachel", imageUrl: "https://example.com/img18.jpg", status: "waiting" },
    { username: "Sarah", imageUrl: "https://example.com/img19.jpg", status: "waiting" },
    { username: "Tom", imageUrl: "https://example.com/img20.jpg", status: "waiting" },

    // Utilisateurs sans statut spécifique (devraient apparaître dans "Users")
    { username: "Uma", imageUrl: "https://example.com/img21.jpg", status: "" },
    { username: "Vince", imageUrl: "https://example.com/img22.jpg", status: "" },
    { username: "Wendy", imageUrl: "https://example.com/img23.jpg", status: "" },
    { username: "Xavier", imageUrl: "https://example.com/img24.jpg", status: "" },
    { username: "Yolanda", imageUrl: "https://example.com/img25.jpg", status: "" }
];

displayUsers(users); // gere l'affichage des utilisateurs

var searchBox = document.querySelector('.search-box');
searchBox.addEventListener('input', function () {
    var searchText = searchBox.value.toLowerCase();
    var filteredUsers = users.filter(user => user.username.toLowerCase().includes(searchText));
    displayUsers(filteredUsers);
});

function updateExistingUserElement(li, user) {
    li.querySelector('.user-photo').style.backgroundImage = `url('${user.imageUrl}')`;
    li.querySelector('.username').textContent = user.username;
    const actionButtons = getActionButtons(user);
    const buttonContainer = li.querySelector('.action-buttons');
    if (!buttonContainer) {
        // Si l'élément des boutons n'existe pas, on le crée.
        li.innerHTML += `<div class="action-buttons">${actionButtons}</div>`;
    } else {
        // Remplace le contenu existant avec les nouveaux boutons appropriés
        buttonContainer.innerHTML = actionButtons;
    }
}

function displayUsers(users) {
    clearLists(); // Vide toutes les listes avant de les remplir

    users.forEach(function (user) {
        let li = document.querySelector(`li[data-username='${user.username}']`); // Recherche d'un élément existant
        if (!li) {
            // Si l'élément n'existe pas, créez un nouveau
            li = createUserElement(user);
        } else {
            // Mise à jour de l'élément existant
            updateExistingUserElement(li, user);
        }

        // Place l'élément dans la bonne liste selon le statut de l'utilisateur
        switch (user.status) {
            case 'friend':
                document.querySelector('.friends-list').appendChild(li);
                break;
            case 'pending':
                document.querySelector('.pending-list').appendChild(li);
                break;
            case 'blocked':
                document.querySelector('.blocked-list').appendChild(li);
                break;
            case 'waiting':
                document.querySelector('.waiting-approval-list').appendChild(li);
                break;
            default:
                document.querySelector('.users-list').appendChild(li);
                break;
        }
    });
}

function clearLists() {
    document.querySelector('.friends-list').innerHTML = '';
    document.querySelector('.pending-list').innerHTML = '';
    document.querySelector('.blocked-list').innerHTML = '';
    document.querySelector('.users-list').innerHTML = '';
}

function createUserElement(user) {
    var li = document.createElement('li');
    li.className = "user-item";
    li.setAttribute('data-username', user.username);
    li.innerHTML = `
        <div class="user-photo" style="background-image: url('${user.imageUrl}');"></div>
        <span class="username">${user.username}</span>
        <div class="action-buttons">${getActionButtons(user)}</div>
    `;
    return li;
}

function getActionButtons(user) {
    switch (user.status) {
        case 'waiting':
            return `
                <button class="button approve-button user-button" onclick="approveUser('${user.username}')">Approve</button>
                <button class="button decline-button user-button" onclick="declineUser('${user.username}')">Decline</button>
            `;
        case 'friend':
            return `<button class="button remove-button" onclick="removeFriend('${user.username}')">Remove</button>`;
        case 'pending':
            return `<button class="button request-sent-button" onclick="cancelRequest('${user.username}')">Cancel Request</button>`;
        case 'blocked':
            return `<button class="button unblock-button" onclick="unblockUser('${user.username}')">Unblock</button>`;
        default:
            return `
                <button class="button add-button user-button" onclick="addFriend('${user.username}')">Add</button>
                <button class="button block-button user-button" onclick="blockUser('${user.username}')">Block</button>
            `;
    }
}

function updateUserStatus(username, newStatus) {
    var user = users.find(u => u.username === username);
    if (user) {
        user.status = newStatus; // Met à jour le statut de l'utilisateur dans l'array
        displayUsers(users); // Rafraîchit l'affichage de tous les utilisateurs
    }
}

function approveUser(username) {
    updateUserStatus(username, 'friend');
}

function declineUser(username) {
    updateUserStatus(username, '');
}

function addFriend(username) {
    updateUserStatus(username, 'pending');
}

function blockUser(username) {
    updateUserStatus(username, 'blocked');
}

function cancelRequest(username) {
    updateUserStatus(username, '');
}

function removeFriend(username) {
    updateUserStatus(username, '');
}

function unblockUser(username) {
    updateUserStatus(username, '');
}