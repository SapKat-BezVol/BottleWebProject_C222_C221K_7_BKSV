% rebase('layoutvariant.tpl', title='Вариант 2 — Корреляции и тепловая карта', year=year)
<script src="/static/scripts/variant2.js"></script>
<h2>Построить корреляционную матрицу и тепловую карту</h2>
<p class="mb-3">
    Нажмите кнопку, чтобы построить <strong>таблицу коэффициентов корреляции</strong> и <strong>тепловую карту</strong> по уже сгенерированной таблице.
</p>
<form method="post" action="/generate_correlation" target="corrFrame" enctype="multipart/form-data">
    <!-- поля формы -->
    <button type="submit" class="btn btn-success btn-primary">Сгенерировать</button>
</form>
<div class="alert alert-info">
    <h4 class="mb-2">Что показывает матрица корреляций?</h4>
    <p class="mb-0">
        Если таблица содержит <strong>5 числовых столбцов</strong>, то и матрица, и тепловая карта будут размером <strong>5×5</strong> — они отображают взаимосвязи между признаками.
    </p>
</div>
<div class="container-fluid my-4">
    <iframe
        name="corrFrame"
        id="corrFrame"
        class="w-100 border rounded shadow-sm"
        style="min-height: 700px; height: 100%; border: 1px solid #ccc;"
        frameborder="0"
        allowfullscreen
    ></iframe>
</div>


