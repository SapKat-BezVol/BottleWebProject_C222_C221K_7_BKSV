% rebase('layoutvariant.tpl', title='Вариант 2 — Корреляции и тепловая карта', year=year)

<h2>Построить корреляционную тепловую карту</h2>
<p class="mb-3">Нажмите кнопку, чтобы построить тепловую карту корреляций по уже сгенерированной таблице.</p>

<form action="/generate_correlation" target="corrFrame" method="post" class="mb-3">
  <button type="submit" class="btn btn-primary">Построить тепловую карту</button>
</form>

<iframe id="corrFrame" name="corrFrame" class="table-frame w-100 border" style="min-height:380px" title="Корреляции"></iframe>
