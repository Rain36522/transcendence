export class Settings
{
	constructor(rawSettings){
		const data = JSON.parse(rawSettings);

		this.nbPlayers = data.nbPlayers || 2;
		this.playersNames = [];
		for (let i = 1; i <= this.nbPlayers; i++)
			this.playersNames.push(data[`player${i}Name`] || `Player${i}`);
		this.isSolo = data.isSolo || true;

		this.gameWidth = data.gameWidth || 1200;
		this.gameHeight = this.gameWidth;
		if (this.nbPlayers != 4)
			this.gameHeight /= 2;

		this.paddleColor = data.paddleColor || "white";
		this.paddleWidth = (data.paddleWidth || 0.02) * this.gameHeight;
		this.paddleLength = (data.paddleLength || 0.2) * this.gameHeight;
		this.paddleOffset = (data.paddleOffset || 0.02) * this.gameHeight;
	
		this.ballSize = (data.ballSize || this.gameHeight) * 0.03;
	}
}