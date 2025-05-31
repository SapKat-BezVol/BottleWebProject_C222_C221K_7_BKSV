<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Элементы машинного обучения и анализа данных</title>
    
    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <!-- Ваши стили и скрипты -->
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <link rel="stylesheet" href="/static/content/custom-navbar.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <link rel="icon" type="image/png" href="/static/images/favicon.png">


</head>

<body style="padding-top:40px;">
    <!-- Навигация -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <a class="navbar-brand custom-brand" href="/">Элементы машинного обучения и анализа данных</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarNav" aria-controls="navbarNav"
                    aria-expanded="false" aria-label="Переключить навигацию">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-3">
                    <li class="nav-item"><a class="nav-link" href="/home">Главная</a></li>
                    <li class="nav-item"><a class="nav-link" href="/about">О команде</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container body-content" style="padding-top:40px;">
        <h1>{{ title }}</h1>
        <p>Выберите способ создания таблицы, затем нажмите «Отобразить» — обновится только таблица ниже.</p>

        <!-- Форма генерации / загрузки -->
        <form action="/generate_table" target="tableFrame" method="post"
              enctype="multipart/form-data" class="mb-4">
            <input class="form-check-input" type="radio" name="mode"
                   id="modeGenerate" value="generate" checked>
            <label class="form-check-label me-3" for="modeGenerate">Сгенерировать</label>

            <input class="form-check-input" type="radio" name="mode"
                   id="modeUpload" value="upload">
            <label class="form-check-label" for="modeUpload">Загрузить файл</label>

            <div class="generate-fields d-flex mt-3 gap-3">
                <div>
                    <label for="rows" class="form-label">Строки</label>
                    <input type="number" class="form-control" id="rows" name="rows"
                           min="1" max="1000" value="100">
                </div>
                <div>
                    <label for="cols" class="form-label">Столбцы</label>
                    <input type="number" class="form-control" id="cols" name="cols"
                           min="1" max="10" value="5">
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

            <div class="upload-fields mt-3">
                <label for="csv_file" class="form-label">CSV/TSV/JSON файл</label>
                <input type="file" class="form-control" id="csv_file" name="csv_file">
            </div>

            <!-- Кнопка «Продолжить» отправляет форму в iframe -->
            <button type="submit" class="btn btn-primary btn-sm">Продолжить</button>
        </form>

        <!-- Форма «Показать часть данных» -->
        <div class="mb-4 border rounded p-3 bg-light">
            <h5>Показать часть данных:</h5>
            <form action="/show_sample" method="post" target="tableFrame"
                  class="d-flex flex-wrap gap-3 align-items-end">
                <div>
                    <label for="n" class="form-label">Сколько записей:</label>
                    <input type="number" name="n" id="n" value="5" min="1"
                           max="100" class="form-control">
                </div>
                <div>
                    <label for="sample_mode" class="form-label">Режим:</label>
                    <select name="mode" id="sample_mode" class="form-select">
                        <option value="head">Первые n</option>
                        <option value="tail">Последние n</option>
                        <option value="random">Случайные n</option>
                    </select>
                </div>
                <div>
                    <button type="submit" class="btn btn-primary btn-sm">Показать</button>
                </div>
            </form>
        </div>

        <!-- Фрейм для сообщений и таблицы: скрыт до первой загрузки -->
        <iframe id="tableFrame" name="tableFrame"
                class="table-frame" title="Таблица" style="display: none;"></iframe>

        {{!base}}
        <hr>
        <footer><p>&copy; {{ year }} – SapKat&BezVol ©</p></footer>
    </div>

    <!-- Скрипт: раскрывает iframe и подгоняет его высоту под контент -->
    <script>
    document.addEventListener('DOMContentLoaded', () => {
        const iframe = document.getElementById('tableFrame');

        // Ф-ция подгонки высоты iframe под реальную высоту содержимого
        function resizeFrame() {
            try {
                const doc = iframe.contentDocument || iframe.contentWindow.document;
                iframe.style.height = doc.body.scrollHeight + 'px';
            } catch (_) { /* на случай неожиданных кросс-доменных ошибок */ }
        }

        // После каждой загрузки в iframe
        iframe.addEventListener('load', () => {
            iframe.style.display = 'block';   // делаем видимым
            resizeFrame();                    // адаптируем высоту
        });

        // Доп-подгонка при изменении размера окна
        window.addEventListener('resize', () => {
            if (iframe.style.display !== 'none') resizeFrame();
        });
    });
    </script>
</body>
</html>
