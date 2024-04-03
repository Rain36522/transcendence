document.addEventListener("DOMContentLoaded", function() {
	// Update slider value
	function updateSliderValue(sliderId, valueId) {
		var slider = document.getElementById(sliderId);
		var output = document.getElementById(valueId);
		output.innerHTML = slider.value;
		slider.oninput = function() {
			output.innerHTML = this.value;
		}
	}
	updateSliderValue('ball-width', 'ball-width-value');
	updateSliderValue('plank-size', 'plank-size-value');
	updateSliderValue('speed', 'speed-value');
	updateSliderValue('acceleration', 'acceleration-value');
  
	// Create button
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
  