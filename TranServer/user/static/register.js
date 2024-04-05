
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
			throw new Error('Signup failed' + response.text);
		}
	})
	.catch(error => {
		console.error('Error:', error);
		document.getElementById('error-message').textContent = 'Signup failed. Please try again.'; // Ici, mettez le message d'erreur souhaité
		document.getElementById('error-message').style.display = 'block'; // Rend le message visible
	});	
});

