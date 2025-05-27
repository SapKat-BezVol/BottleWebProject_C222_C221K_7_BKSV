% rebase('layoutvariant.tpl', title='Вариант 3 — Таблицы и диаграммы', year=year)

<h2>Выберите диаграмму</h2>
<p class="mb-3">Нажмите кнопку, чтобы построить нужный график по уже сгенерированной таблице.</p>

<form action="/generate_plot" target="plotFrame" method="post" class="mb-3">
  <div class="btn-group" role="group" aria-label="plot buttons">
    <button type="submit" name="plot_type" value="hist" class="btn btn-secondary">Гистограммы</button>
    <button type="submit" name="plot_type" value="box" class="btn btn-secondary">Box-plots</button>
    <button type="submit" name="plot_type" value="scatter" class="btn btn-secondary">Scatter Matrix</button>
  </div>
</form>
<iframe id="plotFrame"
        name="plotFrame"
        class="table-frame w-100 border"
        style="min-height:380px"
        title="Диаграммы"></iframe>

<hr>
