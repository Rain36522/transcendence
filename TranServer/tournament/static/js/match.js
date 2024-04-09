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

	updateFromData(data) {
		// Réinitialiser les joueurs et les scores basés sur les données reçues
		this.players = [];
		this.scores = [];
	
		for (let i = 1; i <= 4; i++) {
			const playerKey = `player${i}Id`;
			if (data[playerKey] !== undefined) {
				this.players.push(data[playerKey]);
				const scoreKey = `score${i}`;
				this.scores.push(data[scoreKey] !== undefined ? data[scoreKey] : 0);
			}
		}
	
		this.status = data.status;
		this.gameLink = data.gameLink;
	}
	
	

	generateHTML() {
		let matchElement;
	
		// Crée un élément <a> ou <div> comme conteneur principal selon le statut du match
		if (this.status === "playing" && this.gameLink) {
			matchElement = document.createElement('a');
    		matchElement.href = `/game/${this.gameLink}/`;
    		matchElement.classList.add('match-link');
		} else {
			matchElement = document.createElement('div');
		}
	
		const statusClass = this.status.replace(/\s+/g, '-').toLowerCase();
		matchElement.classList.add('match', statusClass);
		matchElement.setAttribute('data-id', this.id);
		matchElement.setAttribute('data-level', this.level);
	
		// Déterminer l'index du gagnant et traiter tous les autres comme perdants si le match est terminé
		let winnerIndex = -1;
		if (this.status === "finished") {
			const winnerScore = Math.max(...this.scores);
			winnerIndex = this.scores.indexOf(winnerScore);
		}
	
		this.players.forEach((player, index) => {
			const playerElement = document.createElement('div');
			playerElement.classList.add('team');
			// Appliquer la classe 'winner' au gagnant, 'loser' aux autres si le match est terminé
			if (this.status === "finished") {
				if (index === winnerIndex) {
					playerElement.classList.add('winner');
				} else {
					playerElement.classList.add('loser');
				}
			}
	
			playerElement.innerHTML = `
				<span class="name">${player}</span>
				<span class="score">${this.scores[index]}</span>
			`;
			matchElement.appendChild(playerElement);
		});
		if (this.level >= 0) { // Supposons que seuls les matchs après le premier niveau ont des lignes de connexion
			const linesContainer = document.createElement('div');
			linesContainer.className = 'match-lines';
		
			// Créez la ligne horizontale
			const lineHorizontal = document.createElement('div');
			lineHorizontal.className = 'line one';
			linesContainer.appendChild(lineHorizontal);
		
			// Créez la ligne verticale reliant les deux matchs
			const lineVertical = document.createElement('div');
			lineVertical.className = 'line two';
			linesContainer.appendChild(lineVertical);
		
			matchElement.appendChild(linesContainer);
		}
	
		return matchElement;
	}		
}
