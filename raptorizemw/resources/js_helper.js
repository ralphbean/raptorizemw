function include_js(url, success) {
    var script     = document.createElement('script');
    script.src = url;

    var head = document.getElementsByTagName('head')[0],
    done = false;
    // Attach handlers for all browsers
    script.onload = script.onreadystatechange = function() {
        if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete')) {
            done = true;
            success();  // Do the callback
            script.onload = script.onreadystatechange = null;
            head.removeChild(script);
        };
    };
    head.appendChild(script);
};

function run_with_jquery(callback) {
    var jq_url = 'http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js';
    if (typeof jQuery == 'undefined') {
        include_js(jq_url, callback);
    } else {
        callback();
    }
}
