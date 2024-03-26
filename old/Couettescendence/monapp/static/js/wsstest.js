let ws;

document.addEventListener('keydown', (event) => {
    if (event.key === "ArrowUp") {
        sendMessage("u");
    } else if (event.key === "ArrowDown") {
        sendMessage("d");
    }
});

function sendMessage(action) {
    const gameID = document.getElementById('gameID').value;
    const userID = document.getElementById('userID').value;
    const playerID = document.getElementById('playerID').value;

    if (gameID && userID) {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
            connectWebSocket(gameID, userID, action, playerID);
        } else {
			console.log(`ws://127.0.0.1:8001/wsGame/1/username`)
            console.log("sending message: \"" + playerID + action + "\" to " + `ws://127.0.0.1:8001/wsGame/1/username`);
            ws.send(playerID + action);
        }
    } else {
        console.log("infos vides");
    }
}

function connectWebSocket(gameID, userID, action, playerID) {
    const url = `ws://127.0.0.1:8001/wsGame/1/username`;
    ws = new WebSocket(url);

    ws.onopen = () => {
        console.log("Connexion établie.");
		console.log("sending message: \"" + playerID + action + "\" to " + url);
        ws.send(playerID + action);
    };

    ws.onmessage = (event) => {
        console.log("Message reçu : " + event.data);
    };

    ws.onclose = () => {
        console.log("Connexion fermée.");
    };

    ws.onerror = (error) => {
        console.log("Erreur: ", error);
    };
}