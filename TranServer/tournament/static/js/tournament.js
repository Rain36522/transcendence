document.addEventListener("DOMContentLoaded", function() {
    // Fonction pour mettre à jour les options du sélecteur player-amount
    function updatePlayerAmountOptions() {
        var gameModeSelect = document.getElementById('game-mode');
        var playerAmountSelect = document.getElementById('player-amount');
        
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
    document.getElementById('game-mode').addEventListener('change', updatePlayerAmountOptions);
    
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
    updateSliderValue('ball-width', 'ball-width-value');
    updateSliderValue('plank-size', 'plank-size-value');
    updateSliderValue('speed', 'speed-value');
    updateSliderValue('acceleration', 'acceleration-value');
    updateSliderValue('win-point', 'win-point-value'); // Ajouté pour gérer le slider Win Point

    // Gestion de l'envoi des données au clic sur le bouton "CREATE"
    document.querySelector('.create-button').addEventListener('click', function() {
        var tournamentSettings = {
            ballWidth: document.getElementById('ball-width').value,
            plankSize: document.getElementById('plank-size').value,
            speed: document.getElementById('speed').value,
            acceleration: document.getElementById('acceleration').value,
            playerAmount: document.getElementById('player-amount').value,
            winPoint: document.getElementById('win-point').value,
            gameMode: document.getElementById('game-mode').value,
        };
        console.log(JSON.stringify(tournamentSettings));

        // Exemple d'envoi des données, remplacez l'URL par la vôtre
        fetch('!!! ICI IL FAUT METTRE L`ENDROIT OU ENVOYER LE JSON !!!', {
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
