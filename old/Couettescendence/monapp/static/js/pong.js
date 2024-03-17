document.addEventListener('DOMContentLoaded', () => {
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

    // Styling the scoreboard
    scoreBoard.style.textAlign = 'center';
    scoreBoard.style.fontSize = '20px';
    scoreBoard.style.color = 'white';
    scoreBoard.style.marginBottom = '10px';

    // Set field size
    let gameWidth = 1200;
    let gameHeight = gameWidth / 2;

    // Set ball and paddles size
    let ballDiameter = gameHeight * 0.03;
    let paddleWidth = gameWidth * 0.01;
    let paddleHeight = gameHeight * 0.2;
    let paddleOffset = gameWidth * 0.02;

    // Initialize start positions and score
    let scorePlayer1 = 0;
    let scorePlayer2 = 0;
    let paddlePositionPlayer1 = 0;
    let paddlePositionPlayer2 = 0;
    let ballPosition = { x: 0, y: 0 };

    // Player information
    let playerID = '1'; // Can be 'j1' or 'j2'
    let player1Name = 'Ping';
    let player2Name = 'Pong';

    // Set pictures for field and ball if needed
    let isPicture = false;
    let backgroundImage = new Image();
    let ballImage = new Image();
    if (isPicture) {
        backgroundImage.src = 'https://cdn.discordapp.com/attachments/530838799626928139/1218504331242770472/JPEG_20180803_123030.jpg'; // Background image path
        ballImage.src = 'path/to/your/ball.png'; // Ball image path
    }

    // WebSocket setup
    let ws;

    function connectWebSocket() {
        const url = `ws://127.0.0.1:8001/wsGame/1/username`; // Adjust URL as needed
        ws = new WebSocket(url);

        ws.onopen = () =>
            {console.log("WebSocket connection established.");};
        ws.onmessage = (event) => {
            // parsing
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

    document.addEventListener('keydown', (event) => {
        if (!ws || ws.readyState !== WebSocket.OPEN)
            {console.log("WebSocket is not connected."); return;}

        if (event.key === "z")
            ws.send(playerID + "u");
        else if (event.key === "s")
            ws.send(playerID + "d");
        else if (event.key === "ArrowUp")
            ws.send("u");
        else if (event.key === "ArrowDown")
            ws.send("d");
    });

    function drawGame() {
        // Adjust canvas size
        canvas.width = gameWidth;
        canvas.height = gameHeight;

        // If playerID is 'j2', rotate the canvas for the player's perspective
        if (playerID === 'j2') {
            ctx.save(); // Save the current state
            ctx.translate(gameWidth / 2, gameHeight / 2); // Move to the center of the canvas
            ctx.rotate(Math.PI); // Rotate 180 degrees
            ctx.translate(-gameWidth / 2, -gameHeight / 2); // Move back to the original position
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
        const paddleYPlayer1 = (gameHeight * (paddlePositionPlayer1 + 0.5)) - (paddleHeight / 2);
        const paddleYPlayer2 = (gameHeight * (paddlePositionPlayer2 + 0.5)) - (paddleHeight / 2);
        ctx.fillStyle = '#FFF';
        ctx.fillRect(paddleOffset, paddleYPlayer1, paddleWidth, paddleHeight); // Player1
        ctx.fillRect(gameWidth - paddleWidth - paddleOffset, paddleYPlayer2, paddleWidth, paddleHeight); // Player2

        // Draw ball either with color or image
        if (isPicture && ballImage.complete)
            ctx.drawImage(ballImage, gameWidth * (ballPosition.x + 0.5) - ballDiameter / 2, gameHeight * (ballPosition.y + 0.5) - ballDiameter / 2, ballDiameter, ballDiameter);
        else {
            ctx.beginPath();
            ctx.arc(gameWidth * (ballPosition.x + 0.5), gameHeight * (ballPosition.y + 0.5), ballDiameter / 2, 0, Math.PI * 2);
            ctx.fill();
        }

        // Restore the original state if the canvas was rotated for player 2
        if (playerID === 'j2')
            ctx.restore();

        // Update and display the scoreboard based on playerID
        scoreBoard.innerHTML = `${player1Name}: ${scorePlayer1} - ${player2Name}: ${scorePlayer2}`;
        if (playerID === 'j2') {
            // Swap the score display for player 2 to maintain left-right orientation
            scoreBoard.innerHTML = `${player2Name}: ${scorePlayer2} - ${player1Name}: ${scorePlayer1}`;
        }
    }

    window.addEventListener('resize', () => {
        gameWidth = window.innerWidth * 0.8; // Adjust size for chat or other UI elements
        gameHeight = gameWidth / 2;
        ballDiameter = gameHeight * 0.03; // Update sizes based on new dimensions
        paddleOffset = gameWidth * 0.02;
        updateGameState(); // Redraw game with new dimensions
    });
});
