$(document).ready(function () {
    $('#analyzeBtn').click(function () {
        $('#distributionsResult').html('<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Загрузка...</span></div></div>');

        $.post('/variant1/generate_distributions', function (data) {
            $('#distributionsResult').html(data);
        }).fail(function () {
            $('#distributionsResult').html('<div class="alert alert-danger">Ошибка при анализе данных</div>');
        });
    });
});