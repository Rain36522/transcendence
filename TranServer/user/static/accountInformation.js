document.querySelector('.edit-profile-btn').addEventListener('click', function () {
	const fileInput = document.createElement('input');
	fileInput.type = 'file';
	fileInput.accept = 'image/*'; // Accepter seulement les images
	fileInput.onchange = function (e) {
		const file = e.target.files[0];
		const reader = new FileReader();
		reader.onload = function (e) {
			const newProfilePic = e.target.result;
			document.querySelector('.profile-pic').src = newProfilePic;
		};
		reader.readAsDataURL(file);
	};
	fileInput.click();
});
