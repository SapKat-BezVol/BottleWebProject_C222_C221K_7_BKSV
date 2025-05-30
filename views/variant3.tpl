% rebase('layoutvariant.tpl', title='Вариант 3 — Таблицы и диаграммы', year=year)

<h2>Выберите диаграмму</h2>
<p class="mb-3">Нажмите кнопку, чтобы построить нужный график по уже сгенерированной таблице.</p>

<form id="plotForm" action="/generate_plot" target="plotFrame" method="post" class="mb-3">
  <div class="btn-group" role="group" aria-label="plot buttons">
    <button type="submit" name="plot_type" value="hist" class="btn btn-secondary">Гистограммы</button>
    <button type="submit" name="plot_type" value="box" class="btn btn-secondary">Box-plots</button>
    <button type="submit" name="plot_type" value="scatter" class="btn btn-secondary">Scatter Matrix</button>
  </div>
</form>

<div id="plotSpinner" class="text-center my-3"></div>

<iframe id="plotFrame"
        name="plotFrame"
        class="table-frame w-100 border"
        style="min-height:380px; display:none"
        title="Диаграммы"></iframe>

<script>
$(document).ready(function () {
    $('#plotForm').submit(function () {
        $('#plotSpinner').html(
            '<div class="spinner-border" role="status">' +
            '<span class="visually-hidden">Загрузка...</span>' +
            '</div>'
        );
        $('#plotFrame').hide();
    });

    $('#plotFrame').on('load', function () {
        $('#plotSpinner').empty();
        $(this).show();
    });
});
</script>
<hr>
