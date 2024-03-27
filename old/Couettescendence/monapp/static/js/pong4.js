import { Settings } from './Settings.js';
import { Player } from './Player.js';

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

    // Player information
    let playerID = 4; // Can be 1, 2, 3 or 4

    const settingsJson = JSON.stringify({
        nbPlayers: 4,
        player1Name: 'Shrek 1',
        player2Name: 'Fionna 2',
        player3Name: 'Donkey 3',
        player4Name: 'Dragon 4',
        gameWidth: 1200,
        paddleColor: "white",
        paddleWidth: 0.02,
        paddleLength: 0.2,
        paddleOffset: 0.02,
        ballSize: 0.03,
        isSolo: false
        });

    let gameSettings = new Settings(settingsJson);

    //pictures for ball, background and field
    let isImage = false; // This switch controls if images are used
    const fieldImage = new Image();
    const backgroundImage = new Image();
    const ballImage = new Image();

    fieldImage.src = 'https://i.ibb.co/2KnGYRK/4playerspong.png'; // Adjust path
    backgroundImage.src = 'https://i1.sndcdn.com/avatars-000894638827-qr5jsd-t240x240.jpg'; // Adjust path
    ballImage.src = 'https://i1.sndcdn.com/avatars-000894638827-qr5jsd-t240x240.jpg'; // Adjust path

    // Initialize start positions and score
    let ballPosition = { x: 0, y: 0 };

    let players = [gameSettings.nbPlayers];
    for (let i = 0; i < gameSettings.nbPlayers; i++)
        players[i] = new Player(i + 1, gameSettings.playersNames[i], gameSettings);


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

            for (let i = 0; i < gameSettings.nbPlayers; i++)
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
        players[playerID - 1].applyRotation(CanvasContext);

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


        //draw paddles
        for (let i = 0; i < gameSettings.nbPlayers; i++)
            players[i].draw(CanvasContext);


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

        if (playerID === 1)
            scoreBoard.innerHTML = `${gameSettings.playersNames[2]}: ${players[2].Points}<br>${gameSettings.playersNames[0]}: ${players[0].Points} - ${gameSettings.playersNames[1]}: ${players[1].Points}<br>${gameSettings.playersNames[3]}: ${players[3].Points}`;
        else if (playerID === 2)
            scoreBoard.innerHTML = `${gameSettings.playersNames[3]}: ${players[3].Points}<br>${gameSettings.playersNames[1]}: ${players[1].Points} - ${gameSettings.playersNames[0]}: ${players[0].Points}<br>${gameSettings.playersNames[2]}: ${players[2].Points}`;
        else if (playerID === 3)
            scoreBoard.innerHTML = `${gameSettings.playersNames[0]}: ${players[0].Points}<br>${gameSettings.playersNames[2]}: ${players[2].Points} - ${gameSettings.playersNames[3]}: ${players[3].Points}<br>${gameSettings.playersNames[1]}: ${players[1].Points}`;
        else if (playerID === 4)
            scoreBoard.innerHTML = `${gameSettings.playersNames[1]}: ${players[1].Points}<br>${gameSettings.playersNames[3]}: ${players[3].Points} - ${gameSettings.playersNames[2]}: ${players[2].Points}<br>${gameSettings.playersNames[0]}: ${players[0].Points}`;
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
