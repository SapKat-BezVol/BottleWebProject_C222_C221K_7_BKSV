document.addEventListener('DOMContentLoaded', function () {
    const plotForm = document.getElementById('plotForm');
    const plotFrame = document.getElementById('plotFrame');
    const plotSpinner = document.getElementById('plotSpinner');
    if (!plotForm || !plotFrame || !plotSpinner) return;

    plotForm.addEventListener('submit', function (event) {
        event.preventDefault();
        plotSpinner.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Загрузка...</span></div>';
        plotFrame.style.display = 'none';

        const formData = new FormData(plotForm);
        fetch('/generate_plot', { method: 'POST', body: formData })
            .then((response) => response.text())
            .then((html) => {
                plotFrame.srcdoc = html;
            })
            .catch(() => {
                plotFrame.srcdoc = '<div class="alert alert-danger">Ошибка при построении графика</div>';
            });
    });

    plotFrame.addEventListener('load', function () {
        plotSpinner.innerHTML = '';
        try {
            const body = plotFrame.contentDocument.body;
            plotFrame.style.height = body.scrollHeight + 'px';
        } catch (_) {
            /* ignore cross-origin errors */
        }
        plotFrame.style.display = 'block';
    });
});
