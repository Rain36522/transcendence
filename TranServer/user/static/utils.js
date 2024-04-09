function getCookie(name) {
    const cookieValue = document.cookie.split(';')
	.find(cookie => cookie.trim().startsWith(name + '='));
    if (cookieValue) {
        return cookieValue.split('=')[1];
    } else {
        return null;
    }
}