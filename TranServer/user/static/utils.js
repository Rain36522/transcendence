document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener('click', function (event) {
        const target = event.target;
        if (target.tagName === 'A' && target.getAttribute('href') !== '#') {
            event.preventDefault();
            const url = target.getAttribute('href');
            fetchPage(url);
            history.pushState(null, null, url);
        }
    });

    async function fetchPage(url) {
        try {
            const response = await fetch(url);
            const html = await response.text();
            replaceContent(html);
        } catch (error) {
            console.error('Error fetching page:', error);
        }
    }

    function replaceContent(html) {
        document.body.innerHTML = html;
    }

    window.onpopstate = function () {
        const url = window.location.pathname;
        fetchPage(url);
    };
});


function getCookie(name) {
    const cookieValue = document.cookie.split(';')
        .find(cookie => cookie.trim().startsWith(name + '='));
    if (cookieValue) {
        return cookieValue.split('=')[1];
    } else {
        return null;
    }
}


