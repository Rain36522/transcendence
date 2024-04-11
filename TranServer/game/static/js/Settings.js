export class Settings
{
	constructor(rawSettings){
		const data = JSON.parse(rawSettings);

		this.nbPlayers = data.nbPlayers || 2; // number of players in the game
		this.playersNames = []; // names of the players
		for (let i = 1; i <= this.nbPlayers; i++)
			this.playersNames.push(data[`player${i}Name`] || `Player${i}`);
		this.isSolo = data.isSolo; // if no other players on other screens
		this.status = data.status || "waiting"; // if the game is running
		this.winPoints = data.winPoints || 10;

		this.gameWidth = data.gameWidth || 1200; // width of the field
		this.gameHeight = this.gameWidth; // height of the field
		if (this.nbPlayers != 4)
			this.gameHeight /= 2; // field is square if 4 players, else it's a rectangle so we divide the height by 2

		this.paddleColor = data.paddleColor || "white"; // color of the paddles
		this.ballColor = data.ballColor || "white"; // color of the ball
		this.fieldColor = data.fieldColor || "#000"; // color of the field
		this.borderColor = data.borderColor || "white"; // color of the border

		this.paddleWidth = data.paddleWidth || 0.02; // width of the paddles
		this.paddleLength = data.paddleLength || 0.2; // length of the paddles
		this.paddleOffset = data.paddleOffset || 0.02; // offset of the paddles from the border
	
		this.ballSize = data.ballSize || 0.03; // size of the ball
		this.ballPosition = { x: 0, y: 0 }; // position of the ball
		this.userID = data.user;
		this.gameID = data.gameid;
	}
}