document.addEventListener('DOMContentLoaded', function () {
    const plotForm = document.getElementById('plotForm');
    const plotFrame = document.getElementById('plotFrame');
    const plotSpinner = document.getElementById('plotSpinner');
    if (!plotForm || !plotFrame || !plotSpinner) return;
    plotForm.addEventListener('submit', function () {
        plotSpinner.innerHTML = '<div class="spinner-border" role="status"><span class="visually-hidden">Загрузка...</span></div>';
        plotFrame.style.display = 'none';
    });
    plotFrame.addEventListener('load', function () {
        plotSpinner.innerHTML = '';
        const body = plotFrame.contentWindow.document.body;
        plotFrame.style.height = body.scrollHeight + 'px';
        plotFrame.style.display = 'block';
    });
});
