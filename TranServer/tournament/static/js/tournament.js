const users = [
    { id: 1, name: 'Alice', status: 'Invited' },
    { id: 2, name: 'Bob', status: 'Not Invited' },
    { id: 3, name: 'Charlie', status: 'Invited' },
    { id: 4, name: 'Diana', status: 'Not Invited' }
];

function updatePlayerAmountOptions() {
    var gameModeSelect = document.getElementById('gamesettings');
    var playerAmountSelect = document.getElementById('playerNumber');
    playerAmountSelect.innerHTML = '';
    let options = gameModeSelect.value === '2' ? [4, 8, 16, 32] : gameModeSelect.value === '4' ? [8, 16, 32] : [];
    if (gameModeSelect.value === '1') {
        for (var i = 6; i <= 32; i += 2) options.push(i);
    }
    options.forEach(option => {
        let newOption = document.createElement('option');
        newOption.value = option;
        newOption.textContent = option;
        playerAmountSelect.appendChild(newOption);
    });
}

function displayUsersInPopup(users) {
    const userListContainer = document.getElementById('user-list'); // Assurez-vous que cet ID existe dans votre HTML.
    userListContainer.innerHTML = ''; // Clear existing users
    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.className = 'user-item';
        userDiv.innerHTML = `
                <span>${user.name}</span>
                <button class="invite-button" data-user-id="${user.id}">${user.status}</button>
            `;
        userListContainer.appendChild(userDiv);
    });
}

function updateSliderValue(sliderId, valueId) {
    var slider = document.getElementById(sliderId);
    var output = document.getElementById(valueId);
    if (slider && output) { // Check if elements exist
        output.innerHTML = slider.value;
        slider.oninput = function () {
            output.innerHTML = this.value;
        }
    }
}

// Initialize sliders
updateSliderValue('ballwidth', 'ballwidth-value');
updateSliderValue('planksize', 'planksize-value');
updateSliderValue('speed', 'speed-value');  // Corrected from 'Speed'
updateSliderValue('acceleration', 'acceleration-value');
updateSliderValue('winpoint', 'winpoint-value');

updatePlayerAmountOptions();
document.getElementById('gamesettings').addEventListener('change', updatePlayerAmountOptions);

// Handle Create button click
document.querySelector('.create-button').addEventListener('click', function (event) {
    event.preventDefault();
    var tournamentSettings = {
        ballwidth: document.getElementById('ballwidth').value,
        planksize: document.getElementById('planksize').value,
        speed: document.getElementById('speed').value, // Corrected from 'Speed'
        acceleration: document.getElementById('acceleration').value,
        playerNumber: document.getElementById('playerNumber').value,
        winpoint: document.getElementById('winpoint').value,
        gamesettings: document.getElementById('gamesettings').value,
    };
    console.log(JSON.stringify(tournamentSettings));
    openPopup(); // Call popup function directly here
});

var popup = document.querySelector('.popup');
var blurBackground = document.querySelector('.blur-background');

function openPopup() {
    console.log("Opening popup");
    displayUsersInPopup(users); // Update the popup with user data
    popup.style.display = 'block';
    document.body.style.overflow = 'hidden';
    blurBackground.style.display = 'block';
}

function closePopup() {
    popup.style.display = 'none';
    document.body.style.overflow = '';
    blurBackground.style.display = 'none';
}

blurBackground.addEventListener('click', function () {
    closePopup();
});