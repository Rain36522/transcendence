document.addEventListener("DOMContentLoaded", function() {
	// Update slider value
	function updateSliderValue(sliderId, valueId) {
		var slider = document.getElementById(sliderId);
		var output = document.getElementById(valueId);
		output.innerHTML = slider.value;
		slider.oninput = function() {
			output.innerHTML = this.value;
	}}
	updateSliderValue('ball-size', 'ball-size-value');
	updateSliderValue('raquet-size', 'raquet-size-value');
	updateSliderValue('game-speed', 'game-speed-value');
	updateSliderValue('game-acceleration', 'game-acceleration-value');
	updateSliderValue('win-point', 'win-point-value');

	// Create button
	document.querySelector('.create-link').addEventListener('click', function(event) {
		var gameSettings = {
			ballSize: document.getElementById('ball-size').value,
			raquetSize: document.getElementById('raquet-size').value,
			gameSpeed: document.getElementById('game-speed').value,
			gameAcceleration: document.getElementById('game-acceleration').value,
			winPoint: document.getElementById('win-point').value,
			gameMode: document.getElementById('game-mode').value,
		};
		console.log(JSON.stringify(gameSettings));
		
		fetch('!!! ICI IL FAUT METTRE L`ENDROIT OU ENVOYER LE JSON !!!', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(gameSettings),
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
  