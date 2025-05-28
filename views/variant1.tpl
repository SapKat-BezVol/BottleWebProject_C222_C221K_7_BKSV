% rebase('layoutvariant.tpl', title='Вариант 1 - Распределение данных', year=year)

<div class="container mt-4">
    <h2 class="mb-4">Анализ распределений данных</h2>
    
    <div class="card mb-4">
        <div class="card-header">
            <h4>Инструкция</h4>
        </div>
        <div class="card-body">
            <ol>
                <li>Сгенерируйте или загрузите таблицу на главной странице</li>
                <li>Нажмите кнопку ниже для анализа распределений</li>
            </ol>
            <button id="analyzeBtn" class="btn btn-primary">Анализировать распределения</button>
        </div>
    </div>
    
    <div id="distributionsResult"></div>
</div>

<script>
$(document).ready(function() {
    $('#analyzeBtn').click(function() {
        $('#distributionsResult').html('<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Загрузка...</span></div></div>');
        
        $.post('/variant1/generate_distributions', function(data) {
            $('#distributionsResult').html(data);
        }).fail(function() {
            $('#distributionsResult').html('<div class="alert alert-danger">Ошибка при анализе данных</div>');
        });
    });
});
</script>