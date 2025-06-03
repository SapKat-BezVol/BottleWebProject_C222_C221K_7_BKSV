$(function () {
    $('#plotForm').on('submit', function () {
        // показываем спиннер, а сам iframe по-прежнему скрыт
        $('#plotSpinner').html(
            '<div class="spinner-border" role="status">' +
            '<span class="visually-hidden">Загрузка...</span>' +
            '</div>'
        );
    });

    $('#plotFrame').on('load', function () {
        $('#plotSpinner').empty();                     // убираем спиннер
        const body = this.contentWindow.document.body; // вычисляем высоту
        this.style.height = body.scrollHeight + 'px';  // авто-рост фрейма
        $(this).show();                                // делаем видимым
    });
});