(function () {
    if (window.myBookmarklet !== undefined) {
        /* clicks on the bookmarklet repeatedly */
        myBookmarklet();
    } else {
        /* clicks for the 1st time */
        /*
        const site_url = 'http://127.0.0.1:8000/'; */
        const site_url = 'https://8a0ce388.ngrok.io/';
        document.body.appendChild(
            document.createElement('script')
        ).src = site_url + 'static/js/bookmarklet.js?r=' +
            Math.floor(Math.random() * 999999999999999999999999);
    }
})();