// document
//   .querySelector(".edit-profile-btn")
//   .addEventListener("click", function () {
//     const fileInput = document.createElement("input");
//     fileInput.type = "file";
//     fileInput.accept = "image/*"; // Accepter seulement les images
//     fileInput.onchange = function (e) {
//       const file = e.target.files[0];
//       const reader = new FileReader();
//       reader.onload = function (e) {
//         const newProfilePic = e.target.result;
//         document.querySelector(".profile-pic").src = newProfilePic;
//       };
//       reader.readAsDataURL(file);
//     };
//     fileInput.click();
//   });

/* ------------- NEW PARAMETERS ------------ */

document.querySelectorAll('input[type="color"]').forEach((input) => {
  input.addEventListener("input", function () {
    console.log(this.id + " changed to " + this.value);
    // Ajoutez ici le code pour appliquer les couleurs à au backend
  });
});

function openColorPicker(colorId) {
  let button = document.getElementById(colorId); // Récupère le bouton qui a été cliqué

  let colorInput = document.createElement("input");
  colorInput.type = "color";
  colorInput.style.position = "absolute"; // Position absolue pour le placer correctement
  colorInput.style.visibility = "hidden"; // Rendre l'input invisible
  colorInput.style.height = "0"; // Enlève l'encombrement visuel sans affecter la fonctionnalité

  // Place l'input près du bouton
  document.body.appendChild(colorInput); // Ajoute l'input au corps pour éviter des problèmes de clipping
  let rect = button.getBoundingClientRect(); // Récupère les coordonnées du bouton
  colorInput.style.left = `${rect.left}px`;
  colorInput.style.top = `${rect.top}px`;

  // Gère la sélection de la couleur
  colorInput.onchange = (e) => {
    document.getElementById(colorId).style.backgroundColor = e.target.value; // Applique la couleur
    console.log(colorId + " changed to " + e.target.value); // Affiche la valeur choisie
    document.body.removeChild(colorInput); // Supprime l'input après la sélection pour nettoyer le DOM
  };

  colorInput.click(); // Déclenche le sélecteur de couleur
}

document.querySelectorAll(".button-8").forEach((button) => {
  const pickr = Pickr.create({
    el: button,
    theme: "classic", // Thème visuel du sélecteur
    swatches: [
      // Exemples de couleurs prédéfinies
      "rgba(244, 67, 54, 1)",
      "rgba(233, 30, 99, 0.95)",
      "rgba(156, 39, 176, 0.9)",
      "rgba(103, 58, 183, 0.85)",
    ],
    components: {
      preview: true,
      opacity: true,
      hue: true,
      interaction: {
        hex: true,
        rgba: true,
        hsla: true,
        hsva: true,
        cmyk: true,
        input: true,
        clear: true,
        save: true,
      },
    },
  });

  pickr.on("save", (color, instance) => {
    const colorValue = color.toRGBA().toString();
    button.style.backgroundColor = colorValue;
    console.log(button.getAttribute("id") + " changed to " + colorValue);
    pickr.hide();
  });
});

// document
//   .getElementById("updatePasswordBtn")
//   .addEventListener("click", function () {
//     var currentPassword = document.getElementById("currentPassword").value;
//     var newPassword = document.getElementById("newPassword").value;
//     var passwordError = document.getElementById("passwordError");

//     // Supposons que 'passwordCorrecte' est le mot de passe actuel (cette partie devrait être vérifiée côté serveur)
//     if (currentPassword === "passwordCorrecte") {
//       passwordError.style.display = "none";
//       alert("Password updated successfully!"); // Vous pouvez également mettre à jour ce message ou effectuer d'autres actions
//       // Envoyez le nouveau mot de passe au serveur pour mise à jour
//     } else {
//       passwordError.style.display = "block";
//       passwordError.textContent = "Incorrect current password"; // Afficher le message d'erreur
//     }
//   });

document.getElementById('passwordChangeForm').addEventListener('submit', function (event) {
  event.preventDefault();

  var formData = new FormData(this);

  fetch('/api/change_password/', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        document.getElementById('message').innerHTML = '<p style="color: red;">' + data.error + '</p>';
      } else {
        document.getElementById('message').innerHTML = '<p style="color: green;">' + data.message + '</p>';
        // Clear form fields
        document.getElementById('oldPassword').value = '';
        document.getElementById('newPassword').value = '';
      }
    })
    .catch(error => {
      console.error('Error:', error);
      document.getElementById('message').innerHTML = '<p style="color: red;">An unexpected error occurred. Please try again later.</p>';
    });
});

document
  .getElementById("uploadForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission
    var formData = new FormData();
    var fileInput = document.getElementById("profilePicture");
    var file = fileInput.files[0];
    formData.append("profile_picture", file);

    fetch("/api/upload_profile/", {
      method: "POST",
      body: formData,
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    })
      .then((response) => response.json())
      .then((data) => {
        refresh_image();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

function refresh_image() {
  fetch("/api/profile_pic/")
    .then((response) => response.blob())
    .then((blob) => {
      // Convert the blob to a base64 encoded string
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
    })
    .then((data) => {
      console.log(data);
      document.getElementById("profile-pic").src = data;
    });
}
refresh_image();
