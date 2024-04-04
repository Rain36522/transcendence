export class Match {
	constructor(level, id, ...players) {
		this.level = level;
		this.id = id;
		this.players = players;
		this.scores = new Array(players.length).fill(0);
		this.status = "to be played"; // "live", "finished", "to be played"
		this.gameLink = "";
	}

	updateScores(...scores) {
		this.scores = scores;
	}

	setFinished() {
		this.status = "finished";
	}

	setLive(gameLink) {
		this.status = "live";
		this.gameLink = gameLink;
	}

	generateHTML() {
		const matchElement = document.createElement('div');
		// Remplacez les espaces dans this.status par des tirets pour garantir une classe valide.
		const statusClass = this.status.replace(/\s+/g, '-').toLowerCase();
		matchElement.classList.add('match', statusClass);
		matchElement.setAttribute('data-id', this.id);
		matchElement.setAttribute('data-level', this.level);
	
		this.players.forEach((player, index) => {
			const playerElement = document.createElement('div');
			playerElement.classList.add('team');
			playerElement.innerHTML = `
				<span class="name">${player}</span>
				<span class="score">${this.scores[index]}</span>
			`;
			matchElement.appendChild(playerElement);
		});
	
		if (this.status === "live") {
			const liveLink = document.createElement('a');
			liveLink.href = this.gameLink;
			liveLink.textContent = "Regarder le match";
			liveLink.classList.add('live-link');
			matchElement.appendChild(liveLink);
		} else if (this.status === "finished") {
			const winnerScore = Math.max(...this.scores);
			matchElement.querySelectorAll('.score').forEach(scoreElement => {
				if (parseInt(scoreElement.textContent) === winnerScore) {
					scoreElement.classList.add('highlight');
				}
			});
		}
	
		return matchElement;
	}	
}
