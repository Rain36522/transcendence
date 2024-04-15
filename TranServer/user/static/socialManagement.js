var users = [
    { username: "Lolita564", imageUrl: "https://example.com/img1.jpg", status: "friend" },
    { username: "Famacito", imageUrl: "https://example.com/img2.jpg", status: "pending" },
    { username: "Mania_xLeaderz", imageUrl: "https://example.com/img3.jpg", status: "blocked" },
    { username: "Bob", imageUrl: "https://example.com/img3.jpg", status: "blocked" },
    { username: "Dorian", imageUrl: "https://example.com/img3.jpg", status: "pending" },
    { username: "Zefou", imageUrl: "https://example.com/img3.jpg", status: "blocked" },
    { username: "Nohan", imageUrl: "https://example.com/img3.jpg", status: "friend" },
    { username: "Eve", imageUrl: "https://example.com/img4.jpg", status: "" } // Un utilisateur sans statut défini
];

displayUsers(users);
var searchBox = document.querySelector('.search-box');
searchBox.addEventListener('input', function() {
    var searchText = searchBox.value.toLowerCase();
    var filteredUsers = users.filter(user => user.username.toLowerCase().includes(searchText));
    displayUsers(filteredUsers);
});

function displayUsers(users) {
    clearLists(); // Vide toutes les listes avant de les remplir

    users.forEach(function(user) {
        var li = createUserElement(user);
        switch(user.status) {
            case 'friend':
                document.querySelector('.friends-list').appendChild(li);
                break;
            case 'pending':
                document.querySelector('.pending-list').appendChild(li);
                break;
            case 'blocked':
                document.querySelector('.blocked-list').appendChild(li);
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
    li.innerHTML = `
        <div class="user-photo" style="background-image: url('${user.imageUrl}');"></div>
        <span class="username">${user.username}</span>
        ${getActionButtons(user)}
    `;
    return li;
}

function getActionButtons(user) {
    switch(user.status) {
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
        user.status = newStatus;
        displayUsers(users);
    }
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
