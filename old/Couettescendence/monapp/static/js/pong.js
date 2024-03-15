//elements placements
document.addEventListener('DOMContentLoaded', function()
{
	const ball = document.getElementById('ball');
	const paddles = document.querySelectorAll('.paddle');
	const playerID = document.getElementById('player');
	//prepare ball
	ball.style.width = ball.getAttribute('data-size') + 'vmin';
	ball.style.height = ball.getAttribute('data-size') + 'vmin';
	ball.style.transform = 'translate(-50%, -50%)';
	//prepare paddles
	paddles.forEach(paddle => {
		paddle.style.height = paddle.getAttribute('data-size') + 'vmin';
		paddle.style.transform = 'translate(-50%, -50%)';
	});

	placeElement(ball, 50, 50);
	placeElement(document.getElementById('paddle1'), -48, 0);
	placeElement(document.getElementById('paddle2'), 48, -50);
	//place elements on the board and rotate it if needed
	rotateGame(playerID.getAttribute('data-player'));
});

//places a single element on board
function placeElement(element, posX, posY)
{
	const gameWidth = document.getElementById('pong-game').clientWidth;
	const gameHeight = document.getElementById('pong-game').clientHeight;
	const xPercent = (posX + 50) * (gameWidth / 100);
	const yPercent = (-1 * posY + 50) * (gameHeight / 100);

	element.style.left = `${xPercent}px`;
	element.style.top = `${yPercent}px`;
}

//rotates the board with elems to place current player on the left
function rotateGame(playerID)
{
	const game = document.getElementById('pong-game');
	let toRotate = 0;

	switch(playerID)
	{
		case 'j2':
			toRotate = 180;
			break;
		case 'j3':
			toRotate = 270;
			break;
		case 'j4':
			toRotate = 90;
			break;
	}
	game.style.transform = `rotate(${toRotate}deg)`;
}


document.addEventListener('keydown', (event) => {
    if (event.key === "ArrowUp")
        sendMessage("u");
    else if (event.key === "ArrowDown")
        sendMessage("d");
});

function sendMessage(action) {
    const gameID = document.getElementById('gameID').value;
    const userID = document.getElementById('userID').value;
    const playerID = document.getElementById('playerID').value;

    if (gameID && userID) {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            connectWebSocket(gameID, userID, action, playerID);
        } else {
			console.log(`ws://192.168.2.216:8001/wsGame/1/username`)
            console.log("sending message: \"" + playerID + action + "\" to " + `ws://192.168.2.216:8001/wsGame/1/username`);
            ws.send(playerID + action);
        }
    } else {
        console.log("infos vides");
    }
}

function connectWebSocket(gameID, userID, action, playerID) {
    const url = `ws://192.168.2.216:8001/wsGame/1/username`;
    ws = new WebSocket(url);

    ws.onopen = () => {
        console.log("Connexion établie.");
		console.log("sending message: \"" + playerID + action + "\" to " +url);
        ws.send(playerID + action);
    };

    ws.onmessage = (event) => {
        console.log("Message reçu : " + event.data);
    };

    ws.onclose = () => {
        console.log("Connexion fermée.");
    };

    ws.onerror = (error) => {
        console.log("Erreur: ", error);
    };
}