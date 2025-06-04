document.addEventListener('DOMContentLoaded', function () {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultDiv = document.getElementById('distributionsResult');
    if (!analyzeBtn || !resultDiv) return;
    analyzeBtn.addEventListener('click', function () {
        resultDiv.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Загрузка...</span></div></div>';
        fetch('/generate_distributions', {method: 'POST'})
            .then(response => response.text())
            .then(html => {
                resultDiv.innerHTML = html;
            })
            .catch(() => {
                resultDiv.innerHTML = '<div class="alert alert-danger">Ошибка при анализе данных</div>';
            });
    });
});
