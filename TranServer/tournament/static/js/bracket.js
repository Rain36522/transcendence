import { Match } from './match.js';

const myUser = document.body.getAttribute('data-myUser');
const tournamentSize = document.body.getAttribute('data-tournamentSize');
const matchesMap = {}; // Store all matches by unique key (level-pos)

// Data for testing purposes
const simulatedData = [
	{ pos: 1, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, isRunning: false, gameId: "55"},
	{ pos: 2, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, isRunning: false, gameId: ""},
	{ pos: 3, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, isRunning: true, gameId: "34"},
	{ pos: 4, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, isRunning: true, gameId: "2"},
	{ pos: 5, level: 0, player1Id: "J7", player2Id: "J8", score1: 0, score2: 0, isRunning: "to be played", gameId: ""},
	{ pos: 6, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, isRunning: false, gameId: ""},
	{ pos: 7, level: 0, player1Id: "J7", player2Id: "J8",  score1: 0, score2: 0, isRunning: false, gameId: ""},
	{ pos: 8, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 5, score4: 0, isRunning: false, gameId: ""},
	{ pos: 1, level: 1, player1Id: "J1", player2Id: "J3", score1: 1, score2: 2, isRunning: "finished", gameId: "" },
	{ pos: 3, level: 1, player1Id: "J5", player2Id: "J7", score1: 0, score2: 0, isRunning: "to be played", gameId: ""}
];
const simulatedData2 = [
	{ pos: 1, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 6, score2: 9, score3: 6, score4: 9, isRunning: true, gameId: "55"},
	{ pos: 3, level: 0, player1Id: "J5", player2Id: "J6", score1: 1, score2: 2, isRunning: "finished", gameId: ""},
	{ pos: 4, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 2, score2: 3, score3: 1, score4: 4, isRunning: "finished", gameId: "" },
	{ pos: 2, level: 1, player1Id: "J5", player2Id: "J9", score1: 3, score2: 2, isRunning: "finished", gameId: "" },
	{ pos: 1, level: 2, player1Id: "J3", player2Id: "J9", score1: 0, score2: 0, isRunning: "to be played", gameId: "" },
	{ pos: 2, level: 2, player1Id: "J1", player2Id: "J5", score1: 0, score2: 0, isRunning: "to be played", gameId: "" }
];
const simulatedData3 = [
	{ pos: 1, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 6, score2: 9, score3: 6, score4: 9, isRunning: false, gameId: "55"},
	{ pos: 1, level: 2, player1Id: "J3", player2Id: "J9", score1: 1, score2: 3, isRunning: "finished", gameId: "" },
	{ pos: 2, level: 2, player1Id: "J1", player2Id: "J5", score1: 2, score2: 1, isRunning: "finished", gameId: "" },
	{ pos: 1, level: 3, player1Id: "jeanPipou", player2Id: "J1", score1: 0, score2: 0, isRunning: "playing", gameId: "18" }
];

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
	updatedMatches.forEach(matchData => {
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
                    	window.location.pathname = `/game/${matchData.gameId}/`;
						break;
	}}}}});
	console.log('Tournament updated' + updatedMatches);
}


// WebSocket setup
function setupWebSocket() {
	const socket = new WebSocket('wss://AjouterIciLeBonURLDeTournois/');

	socket.onopen = function(event) {
		console.log('WebSocket connection established');
	};
	socket.onmessage = function(event) {
		const data = JSON.parse(event.data);
		updateTournament(data.matches);
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
	// Simulate data updates
	setTimeout(() => updateTournament(simulatedData), 1000);
	setTimeout(() => updateTournament(simulatedData2), 3000);
	setTimeout(() => updateTournament(simulatedData3), 5000);
});
