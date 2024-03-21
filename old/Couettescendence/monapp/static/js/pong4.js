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
    const ctx = canvas.getContext('2d');
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
    let paddleWidth = gameHeight * 0.025;
    let paddleHeight = gameHeight * 0.2;
    let paddleOffset = gameWidth * 0.01;

    // Initialize start positions and score
    let scorePlayer1 = 0;
    let scorePlayer2 = 0;
    let paddlePositionPlayer1 = 0;
    let paddlePositionPlayer2 = 0;
    let paddlePositionPlayer3 = 0.3;
    let paddlePositionPlayer4 = -0.3;
    let ballPosition = { x: 0, y: 0 };

    // Player information
    let playerID = '1'; // Can be '1', '2', '3' or '4'
    let player1Name = 'Ping';
    let player2Name = 'Pong';

    // Set pictures for field and ball if needed
    let isPicture = true;
    let backgroundImage = new Image();
    let ballImage = new Image();
    if (isPicture) {
        backgroundImage.src = 'https://cdn.discordapp.com/attachments/530838799626928139/1218504331242770472/JPEG_20180803_123030.jpg'; // Background image path
        ballImage.src = 'path/to/your/ball.png'; // Ball image path
    }


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
            console.log("drawing game");
            const data = JSON.parse(event.data);
        
            // ball update
            ballPosition.x = data.ballx;
            ballPosition.y = data.bally;
            // update paddles
            paddlePositionPlayer1 = data.p1;
            paddlePositionPlayer2 = data.p2;
            // update score
            scorePlayer1 = data.score1;
            scorePlayer2 = data.score2;
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

    let lastSendTime = 0;
    //interval in ms
    const sendInterval = 20;

    function throttledSendKeyStatus() {
        const now = Date.now();
        if (now - lastSendTime >= sendInterval) {
            sendKeyStatus();
            lastSendTime = now;
        }
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
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            console.log("WebSocket is not connected.");
            return;
        }
        // check state
        if (keysPressed["w"]) ws.send(playerID + "u");
        if (keysPressed["s"]) ws.send(playerID + "d");
        if (keysPressed["ArrowUp"]) ws.send(2 + "u");
        if (keysPressed["ArrowDown"]) ws.send(2 + "d");
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
            ctx.save(); // Save the current state
            ctx.translate(gameWidth / 2, gameHeight / 2); // Move to the center of the canvas
            ctx.rotate(Math.PI); // Rotate 180 degrees
            ctx.translate(-gameWidth / 2, -gameHeight / 2); // Move back to the original position
        } else if (playerID === '3') {
            ctx.save(); // Save the current state
            ctx.translate(gameWidth / 2, gameHeight / 2); // Move to the center of the canvas
            ctx.rotate(Math.PI / 2); // Rotate 90 degrees
            ctx.translate(-gameHeight / 2, -gameWidth / 2); // Move back to the original position
        } else if (playerID === '4') {
            ctx.save(); // Save the current state
            ctx.translate(gameWidth / 2, gameHeight / 2); // Move to the center of the canvas
            ctx.rotate(-Math.PI / 2); // Rotate -90 degrees
            ctx.translate(-gameHeight / 2, -gameWidth / 2); // Move back to the original position
        }

        // Draw field either with color or image
        if (isPicture && backgroundImage.complete)
            ctx.drawImage(backgroundImage, 0, 0, gameWidth, gameHeight);
        else {
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, gameWidth, gameHeight);
        }
        // Add field border
        ctx.strokeStyle = '#FFF';
        ctx.lineWidth = 5;
        ctx.strokeRect(0, 0, gameWidth, gameHeight);

        // Convert paddles position and draw paddles
        const paddleYPlayer1 = (gameHeight * (paddlePositionPlayer1 * -1 + 0.5)) - (paddleHeight / 2);
        const paddleYPlayer2 = (gameHeight * (paddlePositionPlayer2 * -1 + 0.5)) - (paddleHeight / 2);
        const paddleXPlayer3 = (gameWidth * (paddlePositionPlayer3 * -1 + 0.5)) - (paddleHeight / 2);
        const paddleXPlayer4 = (gameWidth * (paddlePositionPlayer4 * -1 + 0.5)) - (paddleHeight / 2);

        ctx.fillStyle = '#FFF';
        ctx.fillRect(paddleOffset, paddleYPlayer1, paddleWidth, paddleHeight); // Player1
        ctx.fillRect(gameWidth - paddleWidth - paddleOffset, paddleYPlayer2, paddleWidth, paddleHeight); // Player2
        ctx.fillRect(paddleXPlayer3, paddleOffset, paddleHeight, paddleWidth); // Player3
        ctx.fillRect(paddleXPlayer4, gameHeight - paddleWidth - paddleOffset, paddleHeight, paddleWidth); // Player4

        // Draw ball either with color or image
        if (isPicture && ballImage.complete)
            ctx.drawImage(ballImage, gameWidth * (ballPosition.x + 0.5) - ballDiameter / 2, gameHeight * (ballPosition.y + 0.5) - ballDiameter / 2, ballDiameter, ballDiameter);
        else {
            ctx.beginPath();
            ctx.arc(gameWidth * (ballPosition.x + 0.5), gameHeight * (ballPosition.y + 0.5), ballDiameter / 2, 0, Math.PI * 2);
            ctx.fill();
        }

        // Restore the original state if the canvas was rotated for player 2
        if (playerID === '2')
            ctx.restore();

        // Update and display the scoreboard based on playerID
        scoreBoard.innerHTML = `${player1Name}: ${scorePlayer1} - ${player2Name}: ${scorePlayer2}`;
        if (playerID === '2') {
            // Swap the score display for player 2 to maintain left-right orientation
            scoreBoard.innerHTML = `${player2Name}: ${scorePlayer2} - ${player1Name}: ${scorePlayer1}`;
        }
    }

    drawGame();

    //resize handling
    window.addEventListener('resize', () => {
        gameWidth = window.innerWidth * 0.8; // Adjust size for chat or other UI elements
        gameHeight = gameWidth / 2;
        ballDiameter = gameHeight * 0.03; // Update sizes based on new dimensions
        paddleOffset = gameWidth * 0.02;
        drawGame(); // Redraw game with new dimensions
    });
});
