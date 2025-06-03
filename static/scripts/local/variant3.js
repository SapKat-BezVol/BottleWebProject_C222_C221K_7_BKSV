// services/static/scripts/local/variant3.js
// ------------------------------------------------------------
// Работаем без jQuery — чистый ES-2022.
// Файл подключайте с атрибутом defer:
// <script defer src="/static/scripts/local/variant3.js"></script>
document.addEventListener('DOMContentLoaded', () => {
    /** @type {HTMLFormElement}  */ const form = document.getElementById('plotForm');
    /** @type {HTMLIFrameElement}*/ const frame = document.getElementById('plotFrame');
    /** @type {HTMLElement}      */ const spinner = document.getElementById('plotSpinner');

    /**
     * Подгоняет высоту iframe под фактическую высоту документа,
     * учитывая margin-collapsing и возможные динамические изменения.
     */
    function adjustFrameHeight() {
        const doc = frame.contentDocument;
        if (!doc) { return; }

        // Берём максимум из body и html — самый надёжный способ
        const newHeight = Math.max(
            doc.documentElement.scrollHeight,
            doc.body.scrollHeight,
        );

        // Защита от «дёргания» кадра: увеличиваем всегда, уменьшаем только
        // если разница > 100 px (чтобы не реагировать на мелкие колебания)
        const curr = parseInt(frame.style.height || '0', 10);
        if (newHeight > curr || curr - newHeight > 100) {
            frame.style.height = `${newHeight}px`;
        }
    }

    /**
     * Показывает спиннер и прячет старый график до прихода нового HTML.
     */
    form.addEventListener('submit', () => {
        spinner.innerHTML =
            `<div class="spinner-border" role="status">
                 <span class="visually-hidden">Загрузка...</span>
             </div>`;
        frame.style.display = 'none';     // прежний график скрываем
    });

    /**
     * Срабатывает, когда /generate_plot полностью отдал HTML.
     * Здесь убираем спиннер, показываем iframe и подгоняем высоту.
     * Дополнительно подписываемся на resize (внешнее окно)
     * и ResizeObserver (внутренняя разметка), чтобы высота оставалась актуальной.
     */
    frame.addEventListener('load', () => {
        spinner.innerHTML = '';

        // Первичное измерение — после одного кадра, когда браузер дорисует изображения
        requestAnimationFrame(() => {
            adjustFrameHeight();
            frame.style.display = 'block';
        });

        // 1. Изменение размеров окна браузера
        window.addEventListener('resize', adjustFrameHeight, { passive: true });

        // 2. Динамические изменения внутри отчёта
        const ro = new ResizeObserver(adjustFrameHeight);
        ro.observe(frame.contentDocument.documentElement);
    });
});
