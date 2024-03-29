export class Player
{
	constructor(PlayerID, PlayerName, gameParams){
		this.PlayerID = PlayerID || "1"; // 1, 2, 3 our 4
		this.PlayerName = PlayerName || "bob"; // eg "BarnabéEnculeurDeMouches"
		this.Points = 0; // Points scored by the player
		this.Position = 0; // from -0.5 to 0.5, represents pos on the paddle slider
		this.keysPressed = {}; // stores keys status (pressed/released) for up and down
		this.gameParams = gameParams; // game settings	
	}

	// store current keys status (pressed/released)
	updateKeysPressed(event, value){
		;
		if (this.gameParams.isSolo && this.gameParams.nbPlayers == 1){ //if 1v1 singlescreen, player 1 uses "w" and "s" keys and player 2 uses arrow keys
			if (event.key == "w")
				this.keysPressed["up"] = value;
			else if (event.key == "s")
				this.keysPressed["down"] = value;
		}else{
			if (event.key == "ArrowUp")
				this.keysPressed["up"] = value;
			else if (event.key == "ArrowDown")
				this.keysPressed["down"] = value;
	}}

	// send key status to server
	sendKeyStatus(ws){
		if (!ws || ws.readyState !== WebSocket.OPEN)
			return;
		if (this.keysPressed["up"] && !this.keysPressed["down"])
			ws.send(this.PlayerID + "u");
		else if (this.keysPressed["down"] && !this.keysPressed["up"])
			console.log(`sending ${this.PlayerID}d`);
	}

	// rotate if needed to put player on the left side of the screen
	applyRotation(canvasContext){
		if (this.PlayerID == 1)
			return;
		canvasContext.save(); // Save the current state
		canvasContext.translate(this.gameParams.gameWidth / 2, this.gameParams.gameHeight / 2); // Move to the center of the canvas
		if (this.PlayerID == 2)
			canvasContext.rotate(Math.PI); // Rotate 180 degrees
		else if (this.PlayerID == 3)
			canvasContext.rotate(-Math.PI / 2); // Rotate 90 degrees
		else if (this.PlayerID == 4)
			canvasContext.rotate(Math.PI / 2); // Rotate -90 degrees
		canvasContext.translate(-this.gameParams.gameWidth / 2, -this.gameParams.gameHeight / 2); // Move back to the original position
	}

	// draw the player's paddle with updated data
	updateStatus(newPosition, newPoints){
		this.Position = newPosition;
		this.Points = newPoints;
	}

	// draw the player's paddle
	draw(canvasContext){
		// Calculate the real position of the paddle
		const realPaddlePos = (this.gameParams.gameHeight * (this.Position * -1 + 0.5)) - (this.gameParams.paddleLength / 2);
		canvasContext.fillStyle = this.gameParams.paddleColor;

		let x, y, width, height;

		if (this.PlayerID < 3) {
			width = this.gameParams.paddleWidth * this.gameParams.gameHeight;
			height = this.gameParams.paddleLength * this.gameParams.gameHeight;
		} else {
			width = this.gameParams.paddleLength * this.gameParams.gameHeight;
			height = this.gameParams.paddleWidth * this.gameParams.gameHeight;
		}

		// Calculate the position and size based on PlayerID
		if (this.PlayerID === 1) {
			x = this.gameParams.paddleOffset * this.gameParams.gameHeight;
			y = realPaddlePos - this.gameParams.paddleLength * this.gameParams.gameHeight / 2;
		} else if (this.PlayerID === 2) {
			x = this.gameParams.gameWidth - this.gameParams.paddleWidth * this.gameParams.gameHeight - this.gameParams.paddleOffset * this.gameParams.gameHeight;
			y = realPaddlePos - this.gameParams.paddleLength * this.gameParams.gameHeight / 2;
		} else if (this.PlayerID === 3) {
			x = realPaddlePos - this.gameParams.paddleLength * this.gameParams.gameHeight / 2;
			y = this.gameParams.paddleOffset * this.gameParams.gameHeight;
		} else if (this.PlayerID === 4) {
			x = realPaddlePos - this.gameParams.paddleLength * this.gameParams.gameHeight / 2;
			y = this.gameParams.gameHeight - this.gameParams.paddleWidth * this.gameParams.gameHeight - this.gameParams.paddleOffset * this.gameParams.gameHeight;
		}
	
		// Draw the paddle with the calculated dimensions
		canvasContext.fillRect(x, y, width, height);
	}

}