% rebase('layoutvariant.tpl', title='Вариант 2 — Корреляции и тепловая карта', year=year)
<script src="/static/scripts/variant2.js"></script>
<h2>Построить корреляционную матрицу и тепловую карту</h2>
<p class="mb-3">
    Нажмите кнопку, чтобы построить <strong>таблицу коэффициентов корреляции</strong> и <strong>тепловую карту</strong> по уже сгенерированной таблице.
</p>
<form action="/generate_correlation" target="corrFrame" method="post" class="mb-3">
    <button type="submit" class="btn btn-success btn-lg">
        Выполнить анализ
    </button>
</form>
<div class="alert alert-info">
    <h4 class="mb-2">Что показывает матрица корреляций?</h4>
    <p class="mb-0">
        Если таблица содержит <strong>5 числовых столбцов</strong>, то и матрица, и тепловая карта будут размером <strong>5×5</strong> — они отображают взаимосвязи между признаками.
    </p>
</div>
<iframe id="corrFrame" name="corrFrame" class="table-frame w-100 border" style="min-height:520px" title="Корреляции"></iframe>
