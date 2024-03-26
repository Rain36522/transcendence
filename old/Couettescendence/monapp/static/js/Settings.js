export class Settings
{
	constructor(rawSettings){
		const data = JSON.parse(rawSettings);
		this.nbPlayers = data.nbPlayers || 2;
		this.isSolo = data.isSolo || true;
		this.gameWidth = data.gameWidth || 1200;
		this.gameHeight = this.gameWidth;
		if (this.nbPlayers != 4)
			this.gameHeight /= 2;
		this.ballSize = data.ballSize || this.gameHeight * 0.03;
	}
}