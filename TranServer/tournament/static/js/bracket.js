import { Match } from './match.js';

const myUser = document.body.getAttribute('data-myUser');
const tournamentSize = document.body.getAttribute('data-tournamentSize');
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
	console.log(updatedMatches);
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
				for (let i = 1; i <= 4; i++) {
					const playerIdKey = `player${i}Id`;
					if (matchData[playerIdKey] && matchData[playerIdKey] === myUser) {
						console.log('Redirecting to:', `/game/${matchData.gameId}/`);
                        window.location.href = `${window.location.origin}/game/${matchData.gameId}/`;
						break;
					}
				}
			}
		}
	}
	console.log('Tournament updated', updatedMatches);
}




// WebSocket setup
function setupWebSocket() {
	const pathElements = window.location.pathname.split('/');
	console.log(pathElements[2]);
	const socket = new WebSocket('wss://' + window.location.host + '/ws/tournament/' + pathElements[2] + '/');

	socket.onopen = function(event) {
		console.log('WebSocket connection established');
	};
	socket.onmessage = function(event) {
		console.log("caca raw data: " + event.data);
		const dataPouet = JSON.parse(event.data);
		console.log("parsed data is: "+ dataPouet)
		updateTournament(dataPouet);
	};
	socket.onerror = function(event) {
		console.error('WebSocket error:', event);
	};
	socket.onclose = function(event) {
		console.log('WebSocket connection closed');
	};
}


document.addEventListener('DOMContentLoaded', () => {
	initializeTournament(tournamentSize); // Initialize the tournament bracket
	setupWebSocket(); // Setup the WebSocket connection
});
