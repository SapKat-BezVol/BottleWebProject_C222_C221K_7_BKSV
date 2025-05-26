% rebase('layout.tpl', title='Вариант 1', year=year)
<h1>Вариант 1</h1>
<p>Выберите способ создания таблицы, затем нажмите «Отобразить» — обновится только таблица ниже.</p>

<form action="/generate_table" target="tableFrame" method="post" enctype="multipart/form-data" class="mb-4">
  <input class="form-check-input" type="radio" name="mode" id="modeGenerate" value="generate" checked>
  <label class="form-check-label me-3" for="modeGenerate">Сгенерировать</label>

  <input class="form-check-input" type="radio" name="mode" id="modeUpload" value="upload">
  <label class="form-check-label" for="modeUpload">Загрузить файл</label>

  <div class="generate-fields d-flex">
    <div>
      <label for="rows" class="form-label">Строки</label>
      <input type="number" class="form-control" id="rows" name="rows" min="1" max="1000" value="100">
    </div>
    <div>
      <label for="cols" class="form-label">Столбцы</label>
      <input type="number" class="form-control" id="cols" name="cols" min="1" max="10" value="5">
    </div>
    <div>
      <label for="pattern" class="form-label">Шаблон</label>
      <select id="pattern" name="pattern" class="form-select">
        <option value="linear">linear</option>
        <option value="sin">sin</option>
        <option value="random">random</option>
      </select>
    </div>
  </div>

  <div class="upload-fields">
    <label for="csv_file" class="form-label">CSV/TSV/JSON файл</label>
    <input type="file" class="form-control" id="csv_file" name="csv_file">
  </div>

  <button type="submit" class="btn btn-primary">Отобразить</button>
</form>

<iframe id="tableFrame" name="tableFrame" class="table-frame" title="Таблица"></iframe>