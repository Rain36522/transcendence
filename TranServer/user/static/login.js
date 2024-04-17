
document.getElementById('login-form').addEventListener('submit', function (event) {
	event.preventDefault();

	// Serialize form data
	const formData = new FormData(this);

	// Send a POST request to the login API
	fetch('/api/login/', {
		method: 'POST',
		body: formData,
	})
		.then(response => {
			if (response.ok) {
				// Redirect upon successful login
				window.history.pushState(null, null, '/dashboard/');
				fetchPage('/dashboard/')
			} else {
				// Display error message if login fails
				response.json().then(data => {
					alert(data.error);  // Assuming the error message is provided in the 'error' field of the JSON response
				});
			}
		})
		.catch(error => {
			console.error('Error:', error);
		});
});
	