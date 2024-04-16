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
