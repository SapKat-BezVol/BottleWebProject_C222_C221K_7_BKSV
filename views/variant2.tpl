% rebase('layout.tpl', title='Вариант 2', year=year)
<h1>Вариант 2</h1>
<p>Выберите способ создания таблицы и нажмите «Отобразить».</p>

<form action="/variant1" method="post" enctype="multipart/form-data" class="mb-4">
  <div class="mb-3">
    <input class="form-check-input" type="radio" name="mode" id="modeGenerate" value="generate" checked>
    <label class="form-check-label me-3" for="modeGenerate">Сгенерировать</label>

    <input class="form-check-input" type="radio" name="mode" id="modeUpload" value="upload">
    <label class="form-check-label" for="modeUpload">Загрузить файл</label>
  </div>

  <div class="generate-fields row g-3">
    <div class="col-auto">
      <label for="rows" class="form-label">Строки</label>
      <input type="number" class="form-control" id="rows" name="rows" min="1" max="1000" value="100">
    </div>
    <div class="col-auto">
      <label for="cols" class="form-label">Столбцы</label>
      <input type="number" class="form-control" id="cols" name="cols" min="1" max="10" value="5">
    </div>
    <div class="col-auto">
      <label for="pattern" class="form-label">Шаблон</label>
      <select id="pattern" name="pattern" class="form-select">
        <option value="linear">linear</option>
        <option value="sin">sin</option>
        <option value="random">random</option>
      </select>
    </div>
  </div>

  <div class="upload-fields" style="display:none;">
    <label for="csv_file" class="form-label">CSV/TSV/JSON файл</label>
    <input type="file" class="form-control" id="csv_file" name="csv_file">
  </div>

  <button type="submit" class="btn btn-primary">Отобразить</button>
</form>

% if error:
<div class="alert alert-danger">{{!error}}</div>
% end

% if table:
<div class="table-scroll table-responsive">
  {{!table}}
</div>
% if corr_matrix and heatmap_url:
<h2>Корреляционная матрица</h2>
<div class="table-responsive table-scroll">
  {{!corr_matrix}}
</div>

<h2>Тепловая карта</h2>
<img src="/static/{{heatmap_url}}" alt="Heatmap" class="img-fluid border rounded shadow-sm">
% end


% else:
<p><em>Таблица появится после нажатия «Отобразить».</em></p>
% end