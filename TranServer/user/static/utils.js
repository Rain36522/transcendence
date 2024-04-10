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
            loadScriptsFromHTML(html);

        } catch (error) {
            console.error('Error fetching page:', error);
        }
    }

    async function loadScriptsFromHTML(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const scriptTags = doc.querySelectorAll('script');

        const scriptUrls = Array.from(scriptTags)
            .map(scriptTag => scriptTag.getAttribute('src'))
            .filter(src => src);

        await Promise.all(scriptUrls.map(loadScript));
    }

    function loadScript(url) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = url;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
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


