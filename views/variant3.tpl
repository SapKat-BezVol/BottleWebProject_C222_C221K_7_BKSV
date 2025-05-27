% rebase('layoutvariant.tpl', title='Вариант 3 — Таблицы и диаграммы', year=year)

<h2>Построить диаграммы</h2>
<p class="mb-2">Заполните параметры (или оставьте прежние) и нажмите нужную кнопку.
Каждая кнопка отправит <code>POST</code>-запрос и обновит фрейм ниже только
диаграммами, не трогая таблицу.</p>

<form action="/generate_plots" target="plotFrame" method="post" enctype="multipart/form-data" class="mb-3" id="plotForm">
  <input class="form-check-input" type="radio" name="mode" id="pModeGenerate" value="generate" checked>
  <label class="form-check-label me-3" for="pModeGenerate">Сгенерировать</label>

  <input class="form-check-input" type="radio" name="mode" id="pModeUpload" value="upload">
  <label class="form-check-label" for="pModeUpload">Загрузить файл</label>

  <div class="generate-fields d-flex flex-wrap gap-3 mb-2 mt-2">
    <div>
      <label for="pRows" class="form-label">Строки</label>
      <input type="number" class="form-control" id="pRows" name="rows" min="1" max="1000" value="100">
    </div>
    <div>
      <label for="pCols" class="form-label">Столбцы</label>
      <input type="number" class="form-control" id="pCols" name="cols" min="1" max="10" value="5">
    </div>
    <div>
      <label for="pPattern" class="form-label">Шаблон</label>
      <select id="pPattern" name="pattern" class="form-select">
        <option value="linear">linear</option>
        <option value="sin">sin</option>
        <option value="random">random</option>
      </select>
    </div>
  </div>

  <div class="upload-fields mb-3">
    <label for="pCsvFile" class="form-label">CSV/TSV/JSON файл</label>
    <input type="file" class="form-control" id="pCsvFile" name="csv_file">
  </div>

  <div class="btn-group" role="group" aria-label="plot buttons">
    <button type="submit" name="plot_type" value="hist" class="btn btn-secondary">Гистограммы</button>
    <button type="submit" name="plot_type" value="box" class="btn btn-secondary">Box-plots</button>
    <button type="submit" name="plot_type" value="scatter" class="btn btn-secondary">Scatter Matrix</button>
  </div>
</form>

<iframe id="plotFrame" name="plotFrame" class="table-frame w-100 border" style="min-height:380px" title="Диаграммы"></iframe>
