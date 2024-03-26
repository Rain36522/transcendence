document.addEventListener('DOMContentLoaded', () => {

    /*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾*\
    ||======================[first initialisation]======================||
    \*__________________________________________________________________*/
    const canvasContainer = document.createElement('div');
    document.body.appendChild(canvasContainer); // Container for canvas and scoreboard
    canvasContainer.style.display = 'flex';
    canvasContainer.style.flexDirection = 'column';
    canvasContainer.style.alignItems = 'center';
    const canvas = document.getElementById('pongCanvas');
    canvasContainer.appendChild(canvas); // Add the canvas to the container
    const CanvasContext = canvas.getContext('2d');
    const scoreBoard = document.createElement('div'); // Creating a separate scoreboard
    canvasContainer.insertBefore(scoreBoard, canvas); // Insert scoreboard above canvas in the container


    /*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾*\
    ||====================[variables initialisation]====================||
    \*__________________________________________________________________*/
    // Styling the scoreboard
    scoreBoard.style.textAlign = 'center';
    scoreBoard.style.fontSize = '20px';
    scoreBoard.style.color = 'white';
    scoreBoard.style.marginBottom = '10px';

    // Set field size
    let gameWidth = 1200;
    let gameHeight = gameWidth;

    // Set ball and paddles size
    let ballDiameter = gameHeight * 0.03;

    let paddleWidth = gameHeight * 0.02;
    let paddleHeight = gameHeight * 0.2;
    let paddleOffset = gameWidth * 0.01;

    //pictures for ball, background and field
    let isImage = false; // This switch controls if images are used
    const fieldImage = new Image();
    const backgroundImage = new Image();
    const ballImage = new Image();

    fieldImage.src = 'https://i.ibb.co/2KnGYRK/4playerspong.png'; // Adjust path
    backgroundImage.src = 'https://i1.sndcdn.com/avatars-000894638827-qr5jsd-t240x240.jpg'; // Adjust path
    ballImage.src = 'https://i1.sndcdn.com/avatars-000894638827-qr5jsd-t240x240.jpg'; // Adjust path

    // Initialize start positions and score
    let scorePlayer1 = 0;
    let scorePlayer2 = 0;
    let scorePlayer3 = 0;
    let scorePlayer4 = 0;
    let paddlePositionPlayer1 = 0.5;
    let paddlePositionPlayer2 = -0.5;
    let paddlePositionPlayer3 = 0;
    let paddlePositionPlayer4 = -0.3;
    let ballPosition = { x: 0, y: 0 };

    // Player information
    let playerID = '4'; // Can be 'j1', 'j2', 'j3' or 'j4'
    let player1Name = 'Shrek 1';
    let player2Name = 'Fionna 2';
    let player3Name = 'Donkey 3';
    let player4Name = 'Dragon 4';

    // WebSocket setup
    let ws;

    /*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾*\
    ||====================[websocket communication]=====================||
    \*__________________________________________________________________*/
    function connectWebSocket() {
        const url = `ws://127.0.0.1:8001/wsGame/1/username`; // Adjust URL as needed
        ws = new WebSocket(url);

        ws.onopen = () =>
            {console.log("WebSocket connection established.");};
        ws.onmessage = (event) => {
            // parsing
            console.log(event.data);
            const data = JSON.parse(event.data);
        
            // ball update
            ballPosition.x = data.ballx;
            ballPosition.y = data.bally;
            // update paddles
            paddlePositionPlayer1 = data.p1;
            paddlePositionPlayer2 = data.p2;
            paddlePositionPlayer3 = data.p3;
            paddlePositionPlayer4 = data.p4;
            // update score
            scorePlayer1 = data.score1;
            scorePlayer2 = data.score2;
            scorePlayer3 = data.score3;
            scorePlayer4 = data.score4;
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
    // stores keys tatus (pressed/released)
    const keysPressed = {};
    //interval in ms
    const sendInterval = 2;
    let lastSendTime = 0;

    function throttledSendKeyStatus() {
        const now = Date.now();
        if (now - lastSendTime >= sendInterval)
            {sendKeyStatus(); lastSendTime = now;}
    }

    document.addEventListener('keydown', (event) => {
        keysPressed[event.key] = true;
        throttledSendKeyStatus();
    });

    document.addEventListener('keyup', (event) => {
        keysPressed[event.key] = false;
        throttledSendKeyStatus();
    });

    function sendKeyStatus() {
        if (!ws || ws.readyState !== WebSocket.OPEN)
            {console.log("WebSocket is not connected."); return;}
        // check state
        if (keysPressed["ArrowUp"]) ws.send(playerID + "u");
        if (keysPressed["ArrowDown"]) ws.send(playerID + "d");
        console.log("sending");
    }


    /*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾*\
    ||===========================[game drawing]=========================||
    \*__________________________________________________________________*/
    function drawGame() {
        // Adjust canvas size
        canvas.width = gameWidth;
        canvas.height = gameHeight;

        // If playerID is 'j2', rotate the canvas for the player's perspective
        if (playerID === '2') {
            CanvasContext.save(); // Save the current state
            CanvasContext.translate(gameWidth / 2, gameHeight / 2); // Move to the center of the canvas
            CanvasContext.rotate(Math.PI); // Rotate 180 degrees
            CanvasContext.translate(-gameWidth / 2, -gameHeight / 2); // Move back to the original position
        } else if (playerID === '3') {
            CanvasContext.save();
            CanvasContext.translate(gameWidth / 2, gameHeight / 2);
            CanvasContext.rotate(-Math.PI / 2);
            CanvasContext.translate(-gameHeight / 2, -gameWidth / 2);
        } else if (playerID === '4') {
            CanvasContext.save();
            CanvasContext.translate(gameWidth / 2, gameHeight / 2);
            CanvasContext.rotate(Math.PI / 2);
            CanvasContext.translate(-gameHeight / 2, -gameWidth / 2);
        }

        // Draw field
        if (isImage) {
            CanvasContext.drawImage(fieldImage, 0, 0, gameWidth, gameHeight);
        } else {
            CanvasContext.fillStyle = '#000';
            CanvasContext.fillRect(0, 0, gameWidth, gameHeight);
        }
        // Add field border
        CanvasContext.strokeStyle = '#FFF';
        CanvasContext.lineWidth = 5;
        CanvasContext.strokeRect(0, 0, gameWidth, gameHeight);

        // Convert paddles position and draw paddles
        const paddleYPlayer1 = (gameHeight * (paddlePositionPlayer1 * -1 + 0.5)) - (paddleHeight / 2);
        const paddleYPlayer2 = (gameHeight * (paddlePositionPlayer2 * -1 + 0.5)) - (paddleHeight / 2);
        const paddleXPlayer3 = (gameWidth * (paddlePositionPlayer3 * -1 + 0.5)) - (paddleHeight / 2);
        const paddleXPlayer4 = (gameWidth * (paddlePositionPlayer4 * -1 + 0.5)) - (paddleHeight / 2);
        CanvasContext.fillStyle = '#FFF';
        CanvasContext.fillRect(paddleOffset, paddleYPlayer1, paddleWidth, paddleHeight); // Player1
        CanvasContext.fillRect(gameWidth - paddleWidth - paddleOffset, paddleYPlayer2, paddleWidth, paddleHeight); // Player2
        CanvasContext.fillRect(paddleXPlayer3, paddleOffset, paddleHeight, paddleWidth); // Player3
        CanvasContext.fillRect(paddleXPlayer4, gameHeight - paddleWidth - paddleOffset, paddleHeight, paddleWidth); // Player4

        // Draw ball
        if (isImage) {
            CanvasContext.beginPath();
            CanvasContext.arc(gameWidth * (ballPosition.x + 0.5), gameHeight * (ballPosition.y + 0.5), ballDiameter / 2, 0, Math.PI * 2);
            CanvasContext.closePath();
            CanvasContext.clip(); // Clips a circular area to draw the ball image in
            CanvasContext.drawImage(ballImage, gameWidth * (ballPosition.x + 0.5) - ballDiameter / 2, gameHeight * (ballPosition.y + 0.5) - ballDiameter / 2, ballDiameter, ballDiameter);
            CanvasContext.restore(); // Restores the context to draw the next frame cleanly
        } else {
            CanvasContext.beginPath();
            CanvasContext.arc(gameWidth * (ballPosition.x + 0.5), gameHeight * (ballPosition.y + 0.5), ballDiameter / 2, 0, Math.PI * 2);
            CanvasContext.fill();
        }

        // Restore the original state if the canvas was rotated for player 2
        if (playerID === '2' || playerID === '3' || playerID === '4')
            CanvasContext.restore();

        // Update and display the scoreboard based on playerID
        if (playerID === '1') {
            scoreBoard.innerHTML = `${player3Name}: ${scorePlayer3}<br>${player1Name}: ${scorePlayer1} - ${player2Name}: ${scorePlayer2}<br>${player4Name}: ${scorePlayer4}`;
        } else if (playerID === '2') {
            scoreBoard.innerHTML = `${player4Name}: ${scorePlayer4}<br>${player2Name}: ${scorePlayer2} - ${player1Name}: ${scorePlayer1}<br>${player3Name}: ${scorePlayer3}`;
        } else if (playerID === '3') {
            scoreBoard.innerHTML = `${player1Name}: ${scorePlayer1}<br>${player3Name}: ${scorePlayer3} - ${player4Name}: ${scorePlayer4}<br>${player2Name}: ${scorePlayer2}`;
        } else if (playerID === '4') {
            scoreBoard.innerHTML = `${player2Name}: ${scorePlayer2}<br>${player4Name}: ${scorePlayer4} - ${player3Name}: ${scorePlayer3}<br>${player1Name}: ${scorePlayer1}`;
        }
    }

    drawGame();

    //resize handl
});

window.addEventListener('resize', () => {
    gameWidth = window.innerWidth * 0.8; // Adjust size for chat or other UI elements
    gameHeight = gameWidth / 2;
    ballDiameter = gameHeight * 0.03; // Update sizes based on new dimensions
    paddleOffset = gameWidth * 0.02;
    drawGame(); // Redraw game with new dimensions
});
