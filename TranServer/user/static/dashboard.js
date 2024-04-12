if (e.target.files && e.target.files[0]) {
	var reader = new FileReader();
	reader.onload = function (e) {
		document.getElementById('profile-pic').style.backgroundImage = 'url(' + e.target.result + ')';
	};
	reader.readAsDataURL(e.target.files[0]);
}

var profilePicInput = document.getElementById('profile-pic');
if (profilePicInput) {
	if (e.target.files && e.target.files[0]) {
		var reader = new FileReader();
		reader.onload = function (e) {
			document.getElementById('profile-pic').style.backgroundImage = 'url(' + e.target.result + ')';
		};
		reader.readAsDataURL(e.target.files[0]);
	}
} else {
	console.log('Element with ID "profile-pic" not found');
}
