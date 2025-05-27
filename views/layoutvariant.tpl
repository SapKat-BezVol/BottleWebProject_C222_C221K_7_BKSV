<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Элементы машинного обучения и анализа данных</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>
</head>

<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="/" class="navbar-brand">Элементы машинного обучения и анализа данных</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="/home">Главная</a></li>
                    <li><a href="/about">О команде</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content">
        <h1>{{ title }}</h1>
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
                <option value="gaussian">gaussian</option>
                <option value="sine">sine</option>
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
        {{!base}}
        <hr />
        <footer>
            <p>&copy; {{ year }} - SapKat&BezVol ©</p>
        </footer>
    </div>
</body>
</html>
