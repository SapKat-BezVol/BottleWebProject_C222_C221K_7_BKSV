document.addEventListener('DOMContentLoaded', function () {
    const iframe = document.getElementById('tableFrame');
    if (!iframe) return;

    function resizeFrame() {
        try {
            const doc = iframe.contentDocument || iframe.contentWindow.document;
            iframe.style.height = doc.body.scrollHeight + 'px';
        } catch (_) {
            /* ignore cross-origin errors */
        }
    }

    iframe.addEventListener('load', function () {
        iframe.style.display = 'block';
        resizeFrame();
    });

    window.addEventListener('resize', function () {
        if (iframe.style.display !== 'none') {
            resizeFrame();
        }
    });
});
