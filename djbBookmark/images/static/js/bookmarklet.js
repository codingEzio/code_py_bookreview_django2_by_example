(function () {
    const jquery_ver = '3.1.1';

    // const site_url = 'http://127.0.0.1:1080/';
    const site_url = 'https://ed186bdb.ngrok.io/';
    const static_url = site_url + 'static/';

    // The min w/h for crawling
    const min_width = 100;
    const min_height = 100;

    function bookmarklet(msg) {
        // load CSS (that's it)
        const css = jQuery('<link>');  // create a <link> tag
        css.attr({
            rel: 'stylesheet',
            type: 'text/css',
            href: static_url + 'css/bookmarklet.css?=' + Math.floor(Math.random() * 9999)
        });
        jQuery('head').append(css);

        // load HTML
        const close_button_escaped = '&times;';
        const box_html = `
        <div id="bookmarklet">
            <a href="#" id="close">${close_button_escaped}</a>  
            <h1>Select an image to bookmark:</h1>
            <div class="images"></div>
        </div>
        `;
        jQuery('body').append(box_html);

        // close
        jQuery('#bookmarklet #close').click(function () {
            jQuery('#bookmarklet').remove();
        });

        // find images that larger than 600x600(example) then
        // display them (underlying mechanics: append to our `div` container)
        jQuery.each(jQuery('img[src$="jpg"]'), function (index, image) {
            if (jQuery(image).width() >= min_width &&
                jQuery(image).height() >= min_height) {
                let image_url = jQuery(image).attr('src');
                jQuery('#bookmarklet .images').append(
                    `<a href="#"><img src="${image_url}" /> </a>`
                );
            }
        });

        // concatenate the GET request for `image_create`
        jQuery('#bookmarklet .images a').click(function (e) {
            const selected_image = jQuery(this).children('img').attr('src');
            jQuery('#bookmarklet').hide();
            window.open(site_url +
                'images/create/?url=' + encodeURIComponent(selected_image) +
                '&title=' + encodeURIComponent(jQuery('title').text()),
                '_blank'
            );
        });
    }

    // Check if jQuery is loaded
    if (typeof window.jQuery != 'undefined') {
        bookmarklet();
    } else {
        const conflict = typeof window.$ != 'undefined';

        const script = document.createElement('script');
        script.src = '//cdn.bootcss.com/jquery/' + jquery_ver + '/jquery.min.js';
        document.head.appendChild(script);

        let attempts = 15;
        (function () {
            if (typeof window.jquery == 'undefined') {
                if (--attempts > 0) {
                    window.setTimeout(arguments.callee, 250);
                } else {
                    alert('An error occurred while loading jQuery');
                }
            } else {
                bookmarklet();
            }
        })();
    }
})();