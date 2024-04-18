document.title = "Forgot Password";

const sendButton = document.querySelector('button[type="submit"]');
sendButton.onclick = function (event) {
	event.preventDefault();
	const email = document.getElementById('email').value;
	if (email) {
		sendRequest(email);
	} else {
		document.getElementById('error-message').textContent = 'Please enter your email address.';
	}
};

function sendRequest(email) {
	fetch('URL_DE_L_API', { // Remplacez 'URL_DE_L_API' par l'URL réelle de l'API
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ email: email })
	})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				document.getElementById('error-message').textContent = '';
				alert('Success: ' + data.message);
			} else {
				throw new Error(data.message);
			}
		})
		.catch(error => {
			console.error('Error:', error);
			document.getElementById('error-message').textContent = 'Failed: ' + error.message;
		});
}