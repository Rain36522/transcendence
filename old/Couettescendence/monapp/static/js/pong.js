import { Settings } from './Settings.js';
import { Player } from './Player.js';

let gameSettings;
let players;
let playerID = 1;// Can be 1, 2, 3 or 4
let canvas, CanvasContext, scoreBoard;
let isImage, fieldImage, backgroundImage, ballImage;
let nbPaddles = 2;

function setGameSize() {
	if (window.innerHeight < window.innerWidth)
		gameSettings.gameWidth = window.innerHeight * 0.8;
	else
		gameSettings.gameWidth = window.innerWidth * 0.8;
	gameSettings.gameHeight = gameSettings.gameWidth;
	if (gameSettings.nbPlayers !== 4)
		gameSettings.gameHeight /= 2;
}

/*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾*\
||===========================[game drawing]=========================||
\*__________________________________________________________________*/
function drawGame() {
	// Adjust canvas size
	canvas.width = gameSettings.gameWidth;
	canvas.height = gameSettings.gameHeight;

	// If playerID is 'j2', rotate the canvas for the player's perspective
	players[playerID - 1].applyRotation(CanvasContext);

	// Draw field
	if (isImage)
		CanvasContext.drawImage(fieldImage, 0, 0, gameSettings.gameWidth, gameSettings.gameHeight);
	else {
		CanvasContext.fillStyle = gameSettings.fieldColor;
		CanvasContext.fillRect(0, 0, gameSettings.gameWidth, gameSettings.gameHeight);
	}
	// Add field border
	CanvasContext.strokeStyle = gameSettings.borderColor;
	CanvasContext.lineWidth = gameSettings.gameWidth / 75;
	CanvasContext.strokeRect(0, 0, gameSettings.gameWidth, gameSettings.gameHeight);

	//draw paddles
	for (let i = 0; i < nbPaddles; i++)
		players[i].draw(CanvasContext);

	// Draw ball
	CanvasContext.fillStyle = gameSettings.ballColor;
	CanvasContext.beginPath();
	CanvasContext.arc(gameSettings.gameWidth * (gameSettings.ballPosition.x + 0.5),  gameSettings.gameHeight * (gameSettings.ballPosition.y + 0.5), gameSettings.ballSize * gameSettings.gameHeight / 2, 0, Math.PI * 2);
	if (isImage) {
		CanvasContext.closePath();
		CanvasContext.clip(); // Clips a circular area to draw the ball image in
		CanvasContext.drawImage(ballImage, gameSettings.gameWidth * (gameSettings.ballPosition.x + 0.5) - gameSettings.ballSize / 2,  gameSettings.gameHeight * (gameSettings.ballPosition.y + 0.5) - gameSettings.ballSize / 2, gameSettings.ballSize, gameSettings.ballSize);
	} else
		CanvasContext.fill();

	// Restore the original state if the canvas was rotated for player 2
	if (isImage || playerID === '2' || playerID === '3' || playerID === '4')
		CanvasContext.restore();

	// Calculs ajustés pour chaque position
	const positions = [ [1, 2, 3], [0, 3, 2], [3, 1, 0], [2, 0, 1]];
	// Sélectionner les positions relatives basées sur playerID
	const [pRight, pTop, pBottom] = positions[playerID - 1];

	// Affichage pour 2 joueurs : joueur actuel et à droite uniquement
	if (nbPaddles === 2)
		scoreBoard.innerHTML = `${gameSettings.playersNames[playerID - 1]}: ${players[playerID - 1].Points} - ${gameSettings.playersNames[pRight]}: ${players[pRight].Points}`;
	else { // Affichage pour 4 joueurs avec toutes positions
		scoreBoard.innerHTML = `${gameSettings.playersNames[pTop]}: ${players[pTop].Points}<br>`;
		scoreBoard.innerHTML += `${gameSettings.playersNames[playerID - 1]}: ${players[playerID - 1].Points} - ${gameSettings.playersNames[pRight]}: ${players[pRight].Points}<br>`;
		scoreBoard.innerHTML += `${gameSettings.playersNames[pBottom]}: ${players[pBottom].Points}`;
	}
	// Make sure to hide waiting screen and end game screen
	document.getElementById('waitingScreen').style.display = 'none';
	document.getElementById('endGameScreen').style.display = 'none';

	if (gameSettings.status == "waiting")
		document.getElementById('waitingScreen').style.display = 'block';
	if (gameSettings.status == "end")
	{
		var winner = 'le Prince de LU';
		for (let i = 0; i < nbPaddles; i++)
			if (players[i].Points == gameSettings.winPoints)
				winner = gameSettings.playersNames[i];
		document.getElementById('winnerText').textContent = 'Winner: ' + winner;
		var score = '';
		for (let i = 0; i < nbPaddles; i++)
			score += gameSettings.playersNames[i] + ': ' + players[i].Points + " <br> ";
  		document.getElementById('scoreText').innerHTML = score;
		document.getElementById('endGameScreen').style.display = 'block';	
	}
}



document.addEventListener('DOMContentLoaded', () => {
	/*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾*\
	||=====================[Context initialisation]=====================||
	\*__________________________________________________________________*/
	const canvasContainer = document.createElement('div');
	document.body.appendChild(canvasContainer); // Container for canvas and scoreboard
	canvasContainer.style.display = 'flex'; canvasContainer.style.flexDirection = 'column'; canvasContainer.style.alignItems = 'center';
	canvas = document.getElementById('pongCanvas');
	canvasContainer.appendChild(canvas); // Add the canvas to the container
	CanvasContext = canvas.getContext('2d');
	scoreBoard = document.createElement('div'); // Creating a separate scoreboard
	canvasContainer.insertBefore(scoreBoard, canvas); // Insert scoreboard above canvas in the container

	// Styling the scoreboard
	scoreBoard.style.textAlign = 'center'; scoreBoard.style.fontSize = '20px'; scoreBoard.style.color = 'white'; scoreBoard.style.marginBottom = '10px';

	/*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾*\
	||====================[variables initialisation]====================||
	\*__________________________________________________________________*/

	
	// Initialize game settings and players
	if (window.contexteJson)
		gameSettings = new Settings(window.contexteJson);
	if (gameSettings.nbPlayers > 2)
		nbPaddles = 4;
	players = [nbPaddles];
	for (let i = 0; i < nbPaddles; i++)
		players[i] = new Player(i + 1, gameSettings.playersNames[i], gameSettings);
	setGameSize()

	// pictures for ball and field
	isImage = false;
	if (isImage){
		fieldImage = new Image();
		ballImage = new Image();
		fieldImage.src = 'https://i.ibb.co/2KnGYRK/4playerspong.png'; // Adjust path
		ballImage.src = 'https://i1.sndcdn.com/avatars-000894638827-qr5jsd-t240x240.jpg'; // Adjust path
	}

	// WebSocket setup
	let ws;

	/*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾*\
	||====================[websocket communication]=====================||
	\*__________________________________________________________________*/
	function connectWebSocket() {
		const url = `ws://127.0.0.1:8001/wsGame/3sdfsdfsdf/username`; // Adjust URL as needed
		ws = new WebSocket(url);

		ws.onopen = () =>
			{console.log("WebSocket connection established.");};
		ws.onmessage = (event) => {
			// parsing
			console.log(event.data);
			const data = JSON.parse(event.data);
			// ball update
			gameSettings.ballPosition = { x: data.ballx, y: -1 * data.bally };
			// update players
			for (let i = 0; i < nbPaddles; i++)
				players[i].updateStatus(data[`p${i + 1}`], data[`score${i + 1}`]);
			drawGame();
		};
		ws.onclose = () =>
			{console.log("WebSocket connection closed.");};
		ws.onerror = (error) =>
			{console.log("WebSocket error: ", error);};
	}
	// Establish WebSocket connection
	connectWebSocket();

	/*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾*\
	||=========================[input managment]========================||
	\*__________________________________________________________________*/
	// Event listeners for key presses
	document.addEventListener('keydown', (event) => {
		if (gameSettings.status !== "playing")
			return;
		players[playerID - 1].updateKeysPressed(event, true, ws);
		if (gameSettings.isSolo == true && gameSettings.nbPlayers == 2 && event.key == "ArrowUp" || event.key == "ArrowDown")
			players[1].updateKeysPressed(event, true, ws);
	});
	// Event listeners for key releases
	document.addEventListener('keyup', (event) => {
		players[playerID - 1].updateKeysPressed(event, false, ws); // Update keysPressed for the player
		if (gameSettings.isSolo && gameSettings.nbPlayers == 2)
			players[1].updateKeysPressed(event, false, ws); // Update keysPressed for the other player if in 1v1 singlescreen
	});

	drawGame();
});
// Adjust canvas size on window resize
window.addEventListener('resize', () => {
	setGameSize()
	drawGame();
});
