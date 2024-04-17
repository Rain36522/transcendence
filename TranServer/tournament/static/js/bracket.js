// import { Match } from './match.js';

class Match {
	constructor(level, pos, ...players) {
		this.level = level;
		this.pos = pos;
		this.players = players;
		this.scores = new Array(players.length).fill(0);
		this.isRunning = false; // "live", "finished", "to be played"
		this.gameLink = "";
	}

	updateScores(...scores) {
		this.scores = scores;
	}

	setFinished() {
		this.isRunning = false;
	}

	setLive(gameLink) {
		this.isRunning = true;
		this.gameLink = gameLink;
	}

	updateFromData(data) {
		// Réinitialiser les joueurs et les scores basés sur les données reçues
		this.players = [];
		this.scores = [];
	
		for (let i = 0; i <= 3; i++) {
			const playerKey = `player${i}Id`;
			if (data[playerKey] !== undefined) {
				this.players.push(data[playerKey]);
				const scoreKey = `score${i}`;
				this.scores.push(data[scoreKey] !== undefined ? data[scoreKey] : 0);
			}
			else if (i == 0){
				this.players.push("waiting for players");
				this.scores.push(0);
			}
		}
	
		this.isRunning = data.isRunning;
		this.gameLink = data.gameId;
	}
	
	

	generateHTML() {
		let matchElement;

		if (this.isRunning)
			this.status = "playing";
		else if (this.scores.some(score => score !== 0))
			this.status = "finished";
		else
			this.status = "waiting";
	
		// Crée un élément <a> ou <div> comme conteneur principal selon le statut du match
		if (this.isRunning == true && this.gameLink) {
			matchElement = document.createElement('a');
			matchElement.href = `/game/${this.gameLink}/`;
			matchElement.classList.add('match-link');
		} else {
			matchElement = document.createElement('div');
		}
	
		const statusClass = this.status.replace(/\s+/g, '-').toLowerCase();
		matchElement.classList.add('match', statusClass);
		matchElement.setAttribute('data-id', this.pos);
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
				if (index === winnerIndex)
					playerElement.classList.add('winner');
				else
					playerElement.classList.add('loser');
			}
			
			// Ajouter la classe 'match-top' au premier élément et 'match-bottom' au dernier élément
			if (index === 0 && index === this.players.length - 1)
				playerElement.classList.add('match-unique');
			else if (index === 0)
				playerElement.classList.add('match-top');
			else if (index === this.players.length - 1)
				playerElement.classList.add('match-bottom');
	
			playerElement.innerHTML = `
				<span class="name">${player}</span>
				<span class="score">${this.scores[index]}</span>
			`;
			matchElement.appendChild(playerElement);
		});

	
		return matchElement;
	}		
}


var myUser = document.getElementById("myUser").getAttribute('data-tournamentSize');
myUser = JSON.parse(myUser);
console.log("my user is: " + myUser);
var isFull = false;
const tournamentSizeString = document.getElementById("tour_size").getAttribute('data-tournamentSize');
const tournamentSize = JSON.parse(tournamentSizeString);
const matchesMap = {}; // Store all matches by unique key (level-pos)



const dataTemplate ={
	pos: 1, // position dans le round (premier match du round x, deuxieme match du round x, etc)
	level: 0, // round du tournoi (..., huitieme, quart, demi, finale)
	player1Id: "J7", // nom du joueur
	player2Id: "J8",
	player3Id: "J9",
	player4Id: "J10",
	score1: 6, // score du joueur
	score2: 9,
	score3: 6,
	score4: 9,
	isRunning: true, // si la partie est en cours
	gameId: "" // pour faire le path avec https://sitename/game/gameId/
};
//pour playerxID et scorex, il suffit d'en mettre 4 si il y en a 4, 2 si il y en a 2, la div s'adapte


// tournament initialization
function initializeTournament(tournamentSize) {
	const bracketContainer = document.getElementById('tournamentBracket');
	bracketContainer.innerHTML = '';

	console.log(tournamentSize);
	tournamentSize.forEach((size, index) => {
		const column = document.createElement('div');
		column.classList.add('column');
		column.setAttribute('data-level', index);

		for (let matchIndex = 0; matchIndex < size; matchIndex++) {
			const match = new Match(index, matchIndex + 1, "Waiting for players...");
			matchesMap[`${index}-${matchIndex + 1}`] = match;
			column.appendChild(match.generateHTML());
		}
		bracketContainer.appendChild(column);
	});
}


function updateTournament(updatedMatches) {
	if (data["tournamentFull"] == true) {
		isFull = true;
	}
	if (isFull == true) {
		document.getElementById('join-button').style.display = 'none';
	}

	for (const key in updatedMatches) {
		const matchData = updatedMatches[key];  // Utilise matchData ici
		const matchKey = `${matchData.level}-${matchData.pos}`;
		const existingMatch = matchesMap[matchKey];
		if (existingMatch) {
			existingMatch.updateFromData(matchData);
			// Replace the existing match HTML with the updated one
			const matchElement = document.querySelector(`.match[data-id="${matchData.pos}"][data-level="${matchData.level}"]`);
			if (matchElement) {
				matchElement.replaceWith(existingMatch.generateHTML());
			}

			if (matchData.isRunning == true) {
				for (let i = 0; i <= 3; i++) {
					const playerIdKey = `player${i}Id`;
					console.log(playerIdKey);
					console.log("matchData[playerIdKey]:", matchData[playerIdKey]);
					console.log("myUser:", myUser);
					if (matchData[playerIdKey] && matchData[playerIdKey] === myUser) {
						
						console.log('Redirecting to:', `/game/${matchData.gameId}/`);
						window.history.pushState(null, null, '/game/${matchData.gameId}/');
						fetchPage('/game/${matchData.gameId}/')
						break;
					}
				}
			}
		}
	}
	console.log('Tournament updated', updatedMatches);
}


document.getElementById('join-button').addEventListener('click', function() {
	const baseUrl = window.location.href; // Récupère l'URL de la page actuelle
	const joinUrl = `${baseUrl}join/`; // Construit l'URL cible pour la requête GET
	console.log('Joining tournament:', joinUrl);
	// Effectue la requête GET avec fetch
	fetch(joinUrl, { method: 'GET' });
});


// WebSocket setup
function setupWebSocket() {
	const pathElements = window.location.pathname.split('/');
	const socket = new WebSocket('wss://' + window.location.host + '/ws/tournament/' + pathElements[2] + '/');

	socket.onopen = function(event) {
		console.log('WebSocket connection established');
	};
	socket.onmessage = function(event) {
		const dataPouet = JSON.parse(event.data);
		updateTournament(dataPouet);
	};
	socket.onerror = function(event) {
		console.error('WebSocket error:', event);
	};
	socket.onclose = function(event) {
		console.log('WebSocket connection closed');
	};
}


initializeTournament(tournamentSize); // Initialize the tournament bracket
setupWebSocket(); // Setup the WebSocket connection
