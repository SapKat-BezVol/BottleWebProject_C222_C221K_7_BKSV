% rebase('layoutvariant.tpl', title='Вариант 2 — Корреляции и тепловая карта', year=year)

<h2>Построить корреляционную тепловую карту</h2>
<p class="mb-3">Нажмите кнопку, чтобы построить тепловую карту корреляций по уже сгенерированной таблице.</p>

<form action="/generate_correlation" target="corrFrame" method="post" class="mb-3">
  <button type="submit" class="btn btn-primary">Построить тепловую карту</button>
</form>

<!-- Пояснение о размере матрицы -->
<div class="alert alert-info">
  <h4 class="mb-2">Что показывает матрица корреляций?</h4>
  <p class="mb-0">
    Если таблица содержит <strong>5 числовых столбцов</strong>, то тепловая карта корреляций будет иметь размер <strong>5×5</strong>.
    Это потому что карта отображает взаимосвязи <em>между признаками</em> (столбцами), а не строками данных.
  </p>
</div>

<iframe id="corrFrame" name="corrFrame" class="table-frame w-100 border" style="min-height:380px" title="Корреляции"></iframe>
