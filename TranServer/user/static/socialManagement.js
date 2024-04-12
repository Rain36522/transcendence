var users = [{ username: "Lolita564", imageUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzO65Lpx5OR_-M92O1otaGdIt6nsTKfii_Bg&usqp=CAU", online: true }, { username: "Famacito", imageUrl: "https://risibank.fr/cache/medias/0/13/1326/132676/full.png", online: false }, { username: "Mania_xLeaderz", imageUrl: "https://cdn.gonzague.me/wp-content/uploads/2012/06/146646811-1200x900.gif", online: true }];

var userList = document.querySelector('.user-list');
userList.innerHTML = ''; // Clear existing list items

users.forEach(function (user) {
  var li = document.createElement('li');
  li.innerHTML = `
            <div class="user-info">
                <div class="user-photo" style="background-image: url('${user.imageUrl}');">
                    <span class="status-indicator" style="background-color: ${user.online ? 'green' : 'red'};"></span>
                </div>
                <span class="username">${user.username}</span>
            </div>
            <button class="block-button">${user.online ? 'Block' : 'Unblock'}</button>`;
  userList.appendChild(li);
});