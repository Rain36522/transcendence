const resetButton = document.querySelector('.reset-button');
resetButton.addEventListener('click', function () {
	const newPassword = document.getElementById('new-password').value;
	const confirmPassword = document.getElementById('confirm-new-password').value;
	const errorMessage = document.getElementById('error-message');
	const userInfo = document.getElementById('userInfo');
	const resetMessageLink = document.getElementById('reset-message-link');

	const username = userInfo.dataset.username;
	const token = userInfo.dataset.token;

	errorMessage.style.display = 'none';
	errorMessage.innerHTML = '';

	if (!newPassword || !confirmPassword) {
		errorMessage.textContent = 'Please complete all fields.';
		errorMessage.style.display = 'block';
	} else if (newPassword !== confirmPassword) {
		errorMessage.textContent = 'Two different passwords.';
		errorMessage.style.display = 'block';
	} else {
		// Envoyer la requête POST
		fetch('/reset_password/change/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify({
				username: username,
				token: token,
				new_password: newPassword
			})
		})
			.then(response => {
				if (response.ok) {
					return response.json();
				}
				throw new Error('Something went wrong on api server!');
			})
			.then(response => {
				console.log('Success:', response);
				resetButton.disabled = true;
				resetButton.style.backgroundColor = '#ccc';
				errorMessage.style.display = 'none';
				resetMessageLink.textContent = 'Password has been reset, please login!';
				resetMessageLink.style.display = 'block';
			})
			.catch(error => {
				console.error('Error:', error);
				errorMessage.textContent = 'Failed to reset password.';
				errorMessage.style.display = 'block';
			});
	}
});

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
