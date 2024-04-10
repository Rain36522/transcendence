document.addEventListener("DOMContentLoaded", function() {
    // Fonction pour mettre à jour les options du sélecteur playerNumber
    function updatePlayerAmountOptions() {
        var gameModeSelect = document.getElementById('gamesettings');
        var playerAmountSelect = document.getElementById('playerNumber');
        
        // Effacer les options actuelles
        playerAmountSelect.innerHTML = '';

        // Ajouter les nouvelles options en fonction du mode de jeu sélectionné
        if (gameModeSelect.value === '2') {
            [4, 8, 16, 32].forEach(function(option) {
                var newOption = document.createElement('option');
                newOption.value = option;
                newOption.textContent = option;
                playerAmountSelect.appendChild(newOption);
            });
        } else if (gameModeSelect.value === '4') {
            [8, 16, 32].forEach(function(option) {
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
        slider.oninput = function() {
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
    document.querySelector('.create-button').addEventListener('click', function() {
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
            if(data.gameLink)
                window.location.href = data.gameLink;
            else
                console.error('No game link received from server');
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
