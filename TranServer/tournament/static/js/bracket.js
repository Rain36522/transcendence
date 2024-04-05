import { Match } from './match.js';

const tournamentSize = 8; // amount of matches during first round
const matchesMap = {}; // Store all matches by unique key (level-id)

// Data for testing purposes
const simulatedData = [
    { id: 1, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, status: "to be played", gameLink: ""},
    { id: 2, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, status: "to be played", gameLink: ""},
    { id: 3, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, status: "to be played", gameLink: ""},
    { id: 4, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, status: "to be played", gameLink: ""},
    { id: 5, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, status: "to be played", gameLink: ""},
    { id: 6, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, status: "to be played", gameLink: ""},
    { id: 7, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, status: "to be played", gameLink: ""},
    { id: 8, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 0, score2: 0, score3: 0, score4: 0, status: "to be played", gameLink: ""},
    { id: 1, level: 1, player1Id: "J1", player2Id: "J3", score1: 1, score2: 2, status: "finished", gameLink: "" },
    { id: 2, level: 1, player1Id: "J5", player2Id: "J7", score1: 0, score2: 0, status: "to be played", gameLink: ""}
];

const simulatedData2 = [
    { id: 3, level: 0, player1Id: "J5", player2Id: "J6", score1: 1, score2: 2, status: "finished", gameLink: ""},
    { id: 4, level: 0, player1Id: "J7", player2Id: "J8", player3Id: "J9", player4Id: "J10", score1: 2, score2: 3, score3: 1, score4: 4, status: "finished", gameLink: "" },
    { id: 2, level: 1, player1Id: "J5", player2Id: "J9", score1: 3, score2: 2, status: "finished", gameLink: "" },
    { id: 1, level: 2, player1Id: "J3", player2Id: "J9", score1: 0, score2: 0, status: "to be played", gameLink: "" },
    { id: 2, level: 2, player1Id: "J1", player2Id: "J5", score1: 0, score2: 0, status: "to be played", gameLink: "" }
];

const simulatedData3 = [
    { id: 1, level: 2, player1Id: "J3", player2Id: "J9", score1: 1, score2: 3, status: "finished", gameLink: "" },
    { id: 2, level: 2, player1Id: "J1", player2Id: "J5", score1: 2, score2: 1, status: "finished", gameLink: "" },
    { id: 1, level: 3, player1Id: "J9", player2Id: "J1", score1: 0, score2: 0, status: "playing", gameLink: "https://localhost/dashboard/" }
];


// tournament initialization
function initializeTournament(tournamentSize) {
    const bracketContainer = document.getElementById('tournamentBracket');
    bracketContainer.innerHTML = ''; // Clear the container before adding new elements

    const totalRounds = Math.ceil(Math.log2(tournamentSize)) + 1;

    for (let round = 0; round < totalRounds; round++) {
        const column = document.createElement('div');
        column.classList.add('column');
        column.setAttribute('data-round', round);

        const matchesInRound = Math.ceil(tournamentSize / Math.pow(2, round));

        for (let matchIndex = 0; matchIndex < matchesInRound; matchIndex++) {
            // Create a new match object and store it in the matchesMap
            const match = new Match(round, matchIndex + 1, "Waiting for players...");
            matchesMap[`${round}-${matchIndex + 1}`] = match;
            // Add the match HTML to the column
            column.appendChild(match.generateHTML());
        }
        bracketContainer.appendChild(column);
    }   
}

function updateTournament(updatedMatches) {
    updatedMatches.forEach(matchData => {
        const matchKey = `${matchData.level}-${matchData.id}`;
        const existingMatch = matchesMap[matchKey];
        if (existingMatch) {
            existingMatch.updateFromData(matchData);
            
            // Replace the existing match HTML with the updated one
            const matchElement = document.querySelector(`.match[data-id="${matchData.id}"][data-level="${matchData.level}"]`);
            if (matchElement) {
                matchElement.replaceWith(existingMatch.generateHTML());
            }
        }
    });
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
