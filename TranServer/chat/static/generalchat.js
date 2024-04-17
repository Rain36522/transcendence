var participants = { participants: [] };
var socket;

var blocked = [];

async function fetchBlocked() {
  try {
    const response = await fetch(`/api/blocked/`);
    if (!response.ok) {
      throw new Error("Failed to fetch blocked users");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching blocked users:", error);
    return [];
  }
}

function startChatSocket(chatId) {
  if (socket) socket.close();
  socket = new WebSocket(
    "wss://" + window.location.host + "/ws/chat/" + chatId + "/"
  );
  socket.addEventListener("open", function (event) {
    console.log("WebSocket connection established.");
  });

  socket.addEventListener("error", function (event) {
    console.error("WebSocket error:", event);
  });

  socket.addEventListener("message", function (event) {
    const message = JSON.parse(event.data);
    renderMessage(message);
  });
}

function selectChat(chatName, chatId, is_personal) {
  document.querySelector(".selected-user").textContent =
    "Chatting with: " + chatName;
  if (is_personal)
    document.querySelector(".selected-user").textContent = "Game Invitations";
  document.getElementById("messages").innerHTML = "";
  open_chat(chatId);
}

async function renderMessage(message) {
  var messageBox = document.createElement("div");
  messageBox.style.display = "flex";
  messageBox.style.alignItems = "center";

  var usernameElement = document.createElement("span");
  usernameElement.textContent = message.username + ": ";
  usernameElement.style.fontWeight = "bold";
  usernameElement.style.marginRight = "5px";
  messageBox.appendChild(usernameElement);

  if (message.message) {
    const messageElement = document.createElement("div");
    messageElement.textContent = message.message;
    for (user in blocked) {
      if (blocked[user].username == message.username)
        messageElement.textContent = "BLOCKED";
    }
    if (await fetchBlockStatus(message.username))
      messageElement.textContent = "BLOCKED";
    messageElement.classList.add("message-box");
    messageBox.appendChild(messageElement);
  }
  if (message.image) {
    const img = document.createElement("img");
    img.src = message.image;
    img.classList.add("image");
    img.classList.add("message-box");
    messageBox.appendChild(img);
  }
  document.getElementById("messages").appendChild(messageBox);
  scrollToBottom();
}

async function fetchBlockStatus(username) {
  try {
    const response = await fetch(`/api/is_blocked/` + username);
    if (!response.ok) {
      throw new Error("Failed to fetch status");
    }
    const data = await response.json();

    return data;
  } catch (error) {
    console.error("Error fetching status:", error);
    return false;
  }
}

async function fetchChats() {
  try {
    const response = await fetch(`/api/chat/`);
    if (!response.ok) {
      throw new Error("Failed to fetch chats");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching messages:", error);
    return [];
  }
}

async function fetchMessages(chatId) {
  try {
    const response = await fetch(`/api/messages/${chatId}/`);
    if (!response.ok) {
      throw new Error("Failed to fetch messages");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching messages:", error);
    return [];
  }
}

function load_chats() {
  fetchChats().then((chats) => {
    const userList = document.getElementById("userList");
    userList.innerHTML = ""; // Effacer le contenu existant
    console.log(chats);
    for (const chat of chats) {
      let usernames = chat.participants
        .map((participant) => participant.username)
        .join(", ");
      if (chat.is_personal) usernames = "Game Invitations"; // Nom spécial pour les chats personnels

      const userDiv = document.createElement("div");
      userDiv.classList.add("user");
      if (chat.is_personal) {
        userDiv.classList.add("game-invitation"); // Ajouter une classe spécifique pour les invitations de jeu
      }
      userDiv.textContent = usernames;
      userDiv.addEventListener("click", () => selectChat(usernames, chat.id, chat.is_personal));
      userList.appendChild(userDiv);
    }
  });
}

async function renderMessagesInOrder(messages) {
  for (const mess of messages) {
    await renderMessage({
      message: mess.content,
      username: mess.sender,
      image: mess.image,
    });
  }
}

function open_chat(chatId) {
  fetchMessages(chatId).then((messages) => {
    console.log(messages);
    renderMessagesInOrder(messages);
  });
  startChatSocket(chatId);
}

function scrollToBottom() {
  const messagesContainer = document.getElementById("messages");
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function sendMessage() {
  if (!socket) return;
  const messageText = document.getElementById("messageText").value.trim();
  const imageData = document.getElementById("imageData").value;

  if (messageText !== "") socket.send(JSON.stringify({ message: messageText }));
  if (imageData !== "") socket.send(JSON.stringify({ image: imageData }));
  document.getElementById("messageText").value = "";
  document.getElementById("imageData").value = "";
  document.getElementById("imagePreview").innerHTML = "";
}

fetchBlocked().then((data) => {
  blocked = data;
  load_chats();
});
