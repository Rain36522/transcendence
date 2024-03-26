import {Settings} from './Settings.js';

export class Player
{
	constructor(PlayerID, PlayerName, gameSettings){
		this.PlayerID = PlayerID || "1"; // 1, 2, 3 our 4
		this.PlayerName = PlayerName || "bob"; // eg "BarnabéEnculeurDeMouches"
		this.Points = 0; // Points scored by the player
		this.Position = 0; // from -0.5 to 0.5, represents pos on the paddle slider
		this.keysPressed = {}; // stores keys status (pressed/released) for up and down
		this.gameSettings = gameSettings; // game settings	
	}


	// stores keys status (pressed/released)
	updateKeysPressed(event, value){
		if (this.gameSettings.isSolo && this.PlayerID == 1){ //if solo, player 1 uses "w" and "s" keys and player 2 uses arrow keys
			if (event.key == "w")
				this.keysPressed["up"] = value;
			else if (event.key == "s")
				this.keysPressed["down"] = value;
		}
		else{
			if (event.key == "ArrowUp")
				this.keysPressed["up"] = value;
			else if (event.key == "ArrowDown")
				this.keysPressed["down"] = value;
		}
	}


	// send key status to server
	sendKeyStatus(ws){
		if (this.keysPressed["up"])
			ws.send(this.PlayerID + "u");
		else if (this.keysPressed["down"])
			ws.send(this.PlayerID + "d");
	}


	// rotate if needed to put player on the left side of the screen
	applyRotation(canvasContext){
		if (this.PlayerID === 1)
			return;
		canvasContext.save(); // Save the current state
        canvasContext.translate(this.gameSettings.gameWidth / 2, this.gameSettings.gameHeight / 2); // Move to the center of the canvas
		if (this.playerID === 2)
            canvasContext.rotate(Math.PI); // Rotate 180 degrees
        else if (this.playerID === 3)
            canvasContext.rotate(-Math.PI / 2); // Rotate 90 degrees
        else if (this.playerID === 4)
            canvasContext.rotate(Math.PI / 2); // Rotate -90 degrees
		canvasContext.translate(-this.gameSettings.gameWidth / 2, -this.gameSettings.gameHeight / 2); // Move back to the original position
	}


	// draw the player's paddle with updated data
	updateAndDraw(newPosition, newPoints, canvasContext){
		this.Position = newPosition;
		this.Points = newPoints;
		this.draw(canvasContext);
	}


	// draw the player's paddle
	draw(canvasContext){
		const realPaddlePos = (this.gameSettings.gameHeight * (this.Position * -1 + 0.5)) - (this.gameSettings.paddleLength / 2); // real position of the paddle
		canvasContext.fillStyle = this.gameSettings.paddleColor; // paddle color

		if (this.PlayerID == 1)
			canvasContext.fillRect(paddleOffset, paddleYPlayer1, paddleWidth, paddleHeight);
		else if (this.PlayerID == 2)
			canvasContext.fillRect(gameWidth - paddleWidth - paddleOffset, paddleYPlayer2, paddleWidth, paddleHeight);
		else if (this.PlayerID == 3)
			canvasContext.fillRect(paddleXPlayer3, paddleOffset, paddleHeight, paddleWidth);
		else if (this.PlayerID == 4)
			canvasContext.fillRect(paddleXPlayer4, gameHeight - paddleWidth - paddleOffset, paddleHeight, paddleWidth);
	}

}