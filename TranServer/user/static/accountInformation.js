document.querySelectorAll('input[type="color"]').forEach((input) => {
  input.addEventListener("input", function () {
    console.log(this.id + " changed to " + this.value);
  });
});

function openColorPicker(colorId) {
  let button = document.getElementById(colorId);

  let colorInput = document.createElement("input");
  colorInput.type = "color";
  colorInput.style.position = "absolute";
  colorInput.style.visibility = "hidden";
  colorInput.style.height = "0";

  document.body.appendChild(colorInput);
  let rect = button.getBoundingClientRect();
  colorInput.style.left = `${rect.left}px`;
  colorInput.style.top = `${rect.top}px`;

  colorInput.onchange = (e) => {
    document.getElementById(colorId).style.backgroundColor = e.target.value;
    console.log(colorId + " changed to " + e.target.value);
    document.body.removeChild(colorInput);
  };

  colorInput.click();
}

document.querySelectorAll(".button-8").forEach((button) => {
  const pickr = Pickr.create({
    el: button,
    theme: "classic",
    swatches: [
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
        var passwordError = document.getElementById('passwordError');
        passwordError.textContent = data.error;
        passwordError.style.display = 'block';
      } else {
        var passwordSuccess = document.getElementById('passwordSuccess');
        passwordSuccess.textContent = 'Your password has been successfully changed.';
        passwordSuccess.style.display = 'block';
      }
    })

    .catch(error => {
      console.error('Error:', error);
      var passwordError = document.getElementById('passwordError');
      passwordError.textContent = 'An unexpected error occurred. Please try again later.';
      passwordError.style.display = 'block';
    });
});

document
  .getElementById("uploadForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
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
