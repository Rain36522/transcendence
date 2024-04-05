
document.getElementById("signupForm").addEventListener("submit", function(event) {
	event.preventDefault();
	var formData = {
		username: document.getElementById("id_username").value,
		email: document.getElementById("id_email").value,
		password: document.getElementById("id_password1").value,
		confirmPassword: document.getElementById("id_password2").value
	};
	if (formData.password !== formData.confirmPassword) {
		alert("Passwords do not match");
		return;
	}
	fetch('/api/signup/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': getCookie('csrftoken')
		},
		body: JSON.stringify(formData)
	})
	.then(response => {
		if (response.ok) {
			window.location.href = '/dashboard';
		} else {
			throw new Error('Signup failed');
		}
	})
	.catch(error => {
		console.error('Error:', error);
		alert('Signup failed. Please try again.');
	});
});

