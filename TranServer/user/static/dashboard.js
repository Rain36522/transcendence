document.getElementById('profile-pic').addEventListener('change', function (e) {
	if (e.target.files && e.target.files[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			document.getElementById('profile-pic').style.backgroundImage = 'url(' + e.target.result + ')';
		};
		reader.readAsDataURL(e.target.files[0]);
	}
});

window.addEventListener('load', function () {
	var profilePicInput = document.getElementById('profile-pic');
	if (profilePicInput) {
		profilePicInput.addEventListener('change', function (e) {
			if (e.target.files && e.target.files[0]) {
				var reader = new FileReader();
				reader.onload = function (e) {
					document.getElementById('profile-pic').style.backgroundImage = 'url(' + e.target.result + ')';
				};
				reader.readAsDataURL(e.target.files[0]);
			}
		});
	} else {
		console.log('Element with ID "profile-pic" not found');
	}
});

