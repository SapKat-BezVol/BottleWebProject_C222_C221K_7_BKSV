document.addEventListener('DOMContentLoaded', () => {
        const iframe = document.getElementById('tableFrame');

    // Ф-ция подгонки высоты iframe под реальную высоту содержимого
    function resizeFrame() {
            try {
                const doc = iframe.contentDocument || iframe.contentWindow.document;
    iframe.style.height = doc.body.scrollHeight + 'px';
            } catch (_) { /* на случай неожиданных кросс-доменных ошибок */}
        }

        // После каждой загрузки в iframe
        iframe.addEventListener('load', () => {
        iframe.style.display = 'block';   // делаем видимым
    resizeFrame();                    // адаптируем высоту
        });

        // Доп-подгонка при изменении размера окна
        window.addEventListener('resize', () => {
            if (iframe.style.display !== 'none') resizeFrame();
        });
    });