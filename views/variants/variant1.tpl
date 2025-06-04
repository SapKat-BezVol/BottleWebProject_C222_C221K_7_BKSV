% rebase('variants/layout_variants.tpl', title='Вариант 1 - Распределение данных', year=year)

<script src="/static/scripts/local/variant1.js"></script>
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
            <button id="analyzeBtn" class="btn btn-success">Анализировать распределения</button>
        </div>
    </div>
    <div id="distributionsResult"></div>
</div>