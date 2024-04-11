// Fonction pour mettre à jour les options du sélecteur playerNumber
function updatePlayerAmountOptions() {
    var gameModeSelect = document.getElementById('gamesettings');
    var playerAmountSelect = document.getElementById('playerNumber');

    // Effacer les options actuelles
    playerAmountSelect.innerHTML = '';

    // Ajouter les nouvelles options en fonction du mode de jeu sélectionné
    if (gameModeSelect.value === '2') {
        [4, 8, 16, 32].forEach(function (option) {
            var newOption = document.createElement('option');
            newOption.value = option;
            newOption.textContent = option;
            playerAmountSelect.appendChild(newOption);
        });
    } else if (gameModeSelect.value === '4') {
        [8, 16, 32].forEach(function (option) {
            var newOption = document.createElement('option');
            newOption.value = option;
            newOption.textContent = option;
            playerAmountSelect.appendChild(newOption);
        });
    } else if (gameModeSelect.value === '1') { // Mix mode
        for (var i = 6; i <= 32; i += 2) {
            var newOption = document.createElement('option');
            newOption.value = i;
            newOption.textContent = i;
            playerAmountSelect.appendChild(newOption);
        }
    }
}

// Appeler la fonction lors du chargement de la page
updatePlayerAmountOptions();

// Appeler la fonction à chaque changement du mode de jeu
document.getElementById('gamesettings').addEventListener('change', updatePlayerAmountOptions);

// Fonction pour mettre à jour la valeur d'un slider et l'afficher
function updateSliderValue(sliderId, valueId) {
    var slider = document.getElementById(sliderId);
    var output = document.getElementById(valueId);
    output.innerHTML = slider.value; // Initialise la valeur au chargement
    slider.oninput = function () {
        output.innerHTML = this.value; // Met à jour la valeur lors du changement du slider
    }
}

// Mise à jour des valeurs des sliders
updateSliderValue('ballwidth', 'ballwidth-value');
updateSliderValue('planksize', 'planksize-value');
updateSliderValue('Speed', 'Speed-value');
updateSliderValue('acceleration', 'acceleration-value');
updateSliderValue('winpoint', 'winpoint-value'); // Ajouté pour gérer le slider Win Point

// Gestion de l'envoi des données au clic sur le bouton "CREATE"
document.querySelector('.create-button').addEventListener('click', function () {
    var tournamentSettings = {
        ballwidth: document.getElementById('ballwidth').value,
        planksize: document.getElementById('planksize').value,
        Speed: document.getElementById('Speed').value,
        acceleration: document.getElementById('acceleration').value,
        playerNumber: document.getElementById('playerNumber').value,
        winpoint: document.getElementById('winpoint').value,
        gamesettings: document.getElementById('gamesettings').value,
    };
    console.log(JSON.stringify(tournamentSettings));

    // Exemple d'envoi des données, remplacez l'URL par la vôtre
    fetch('', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(tournamentSettings),
    })
        .then(response => {
            if (!response.ok)
                throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            if (data.gameLink)
                window.location.href = data.gameLink;
            else
                console.error('No game link received from server');
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

// Pop up

var popup = document.querySelector('.popup');
var blurBackground = document.querySelector('.blur-background');

blurBackground.addEventListener('click', function (event) {
    if (event.target === blurBackground) {
        popup.style.display = 'none';
        blurBackground.style.display = 'none';
    }
});

function openPopup() {
    var popup = document.getElementById('popup');
    popup.style.display = 'block';
    document.body.style.overflow = 'hidden';
    document.querySelector('.blur-background').style.display = 'block';
}

function closePopup() {
    var popup = document.getElementById('popup');
    popup.style.display = 'none';
    document.body.style.overflow = '';
    document.querySelector('.blur-background').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function () {
    const createButton = document.querySelector('.create-button');
    const inviteButtons = document.querySelectorAll('.invite-button');
    const popup = document.getElementById('popup');
    const blurBackground = document.querySelector('.blur-background');
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.querySelector('.search-container button');
    const userItems = document.querySelectorAll('.user-item');

    // Fonction pour ouvrir la popup
    function openPopup() {
        popup.style.display = 'block';
        document.body.style.overflow = 'hidden';
        blurBackground.style.display = 'block';
    }

    // Fonction pour fermer la popup
    function closePopup() {
        popup.style.display = 'none';
        document.body.style.overflow = '';
        blurBackground.style.display = 'none';
    }

    // Ecouteur d'événements pour le bouton "Create"
    createButton.addEventListener('click', function (event) {
        event.preventDefault();
        openPopup();
    });

    function searchUsers() {
        var searchText = document.getElementById('searchInput').value.toLowerCase();
        var users = document.querySelectorAll('.user-item');
        var searchResultDiv = document.getElementById('searchResult');
        searchResultDiv.innerHTML = ''; // Effacer les résultats précédents
        searchResultDiv.style.display = 'none'; // Masquer le div en attendant

        for (let user of users) {
            var name = user.querySelector('.user-name').textContent.toLowerCase();
            if (name.includes(searchText)) {
                var userClone = user.cloneNode(true); // Cloner l'élément trouvé
                searchResultDiv.appendChild(userClone); // Ajouter le clone au div de résultat
                searchResultDiv.style.display = ''; // Afficher le div de résultat
                break; // Sortir après avoir trouvé le premier utilisateur correspondant
            }
        }
    }

    // Modifier l'écouteur d'événements pour utiliser la fonction searchUsers lors de la saisie
    document.getElementById('searchInput').addEventListener('input', searchUsers);


    document.querySelector('.search-container button').addEventListener('click', searchUsers);

    function handleInviteButtonClick(event) {
        const userItem = event.target.closest('.user-item');
        const clonedUserItem = userItem.cloneNode(true);
        const userName = userItem.querySelector('.user-name').textContent; // Get the username
        const isInvited = event.target.textContent === 'Invite';

        // Update the button text and color
        event.target.textContent = isInvited ? '✖' : 'Invite';
        event.target.style.backgroundColor = isInvited ? 'red' : '#4CAF50';

        const targetContainerId = isInvited ? 'invitedUsers' : 'user-list';
        const targetContainer = document.getElementById(targetContainerId);

        if (isInvited && targetContainerId === 'invitedUsers') {
            // If inviting the user, search for and remove the original from the user list
            const originalUserItems = document.querySelectorAll('#user-list .user-item');
            originalUserItems.forEach(function (item) {
                const itemUserName = item.querySelector('.user-name').textContent;
                if (itemUserName === userName) {
                    item.remove(); // Remove the original item from the user list
                }
            });
        }

        targetContainer.appendChild(userItem); // Add the invited user to the target container
    }

    // Attach the event listener directly to each invite-button
    document.querySelectorAll('.invite-button').forEach(button => {
        button.addEventListener('click', handleInviteButtonClick);
    });

    // Gestion du clic sur le fond flou pour fermer la popup
    blurBackground.addEventListener('click', function () {
        closePopup();
    });
});