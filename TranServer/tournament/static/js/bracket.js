import { Match } from './match.js'; // Assurez-vous que le chemin est correct

const tournamentSize = 8; // Nombre de matchs au premier tour
const matchSize = 2; // Nombre de joueurs par match, supposé pour l'exemple

import { Match } from './match.js'; // Ajustez le chemin selon votre structure

// Initialisation du tournoi
function initializeTournament() {
    // Créez ici la structure initiale du tournoi si nécessaire
    // Cela peut impliquer de générer des colonnes vides pour chaque tour
}

// Mise à jour du tournoi avec les données reçues
function updateTournament(matches) {
    const bracketContainer = document.getElementById('tournamentBracket');
    bracketContainer.innerHTML = ''; // Réinitialiser pour la mise à jour

    matches.forEach(matchData => {
        const match = new Match(matchData.level, matchData.id, matchData.player1Id, matchData.player2Id);
        match.updateScores(matchData.score1, matchData.score2);
        match.status = matchData.status;
        match.gameLink = matchData.gameLink;
        bracketContainer.appendChild(match.generateHTML());
    });
}

// Connexion WebSocket
function setupWebSocket() {
    const socket = new WebSocket('wss://example.com/ws'); // Remplacez par votre URL de WebSocket

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
    initializeTournament(); // Initialisez le tournoi à chargement de page
    setupWebSocket(); // Établissez la connexion WebSocket
});
