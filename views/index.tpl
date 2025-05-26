% rebase('layout.tpl', title='Home Page', year=year)

<!-- Главная страница с четырьмя вкладками для вариантов анализа -->
<div class="jumbotron">
    <h1>Элементы машинного обучения и анализа данных</h1>
    <p class="lead">
        Проект учебной практики команды 7: анализ случайно сгенерированной таблицы (до 1000 строк и 10 столбцов).
    </p>
</div>

<!-- Навигационные вкладки -->
<ul class="nav nav-tabs" id="variantTabs" role="tablist">
    <li role="presentation" class="active">
        <a href="#variant1" aria-controls="variant1" role="tab" data-toggle="tab">Вариант 1 <small>Статистика</small></a>
    </li>
    <li role="presentation">
        <a href="#variant2" aria-controls="variant2" role="tab" data-toggle="tab">Вариант 2 <small>Корреляции</small></a>
    </li>
    <li role="presentation">
        <a href="#variant3" aria-controls="variant3" role="tab" data-toggle="tab">Вариант 3 <small>Графики</small></a>
    </li>
    <li role="presentation">
        <a href="#variant4" aria-controls="variant4" role="tab" data-toggle="tab">Вариант 4 <small>Прогноз</small></a>
    </li>
</ul>

<!-- Содержимое вкладок -->
<div class="tab-content" style="margin-top: 20px;">
    <!-- Вариант 1 -->
    <div role="tabpanel" class="tab-pane fade in active" id="variant1">
        <div class="row">
            <div class="col-md-12">
                <h2>Вариант 1: Распределения и статистики</h2>
                <p>Построение распределений данных для каждого столбца, проверка на нормальность, вычисление основных статистик и выявление аномалий.</p>
                <p><a class="btn btn-primary" href="/variant1">Перейти к анализу &raquo;</a></p>
            </div>
        </div>
    </div>

    <!-- Вариант 2 -->
    <div role="tabpanel" class="tab-pane fade" id="variant2">
        <div class="row">
            <div class="col-md-12">
                <h2>Вариант 2: Корреляции и тепловая карта</h2>
                <p>Построение матрицы корреляций и тепловой карты зависимостей между столбцами с выводами по обнаруженным связям.</p>
                <p><a class="btn btn-primary" href="/variant2">Перейти к анализу &raquo;</a></p>
            </div>
        </div>
    </div>

    <!-- Вариант 3 -->
    <div role="tabpanel" class="tab-pane fade" id="variant3">
        <div class="row">
            <div class="col-md-12">
                <h2>Вариант 3: Графики и scatter‑matrix</h2>
                <p>Различные диаграммы для каждого столбца, матрица рассеяния и визуализация выявленных зависимостей.</p>
                <p><a class="btn btn-primary" href="/variant3">Перейти к графикам &raquo;</a></p>
            </div>
        </div>
    </div>

    <!-- Вариант 4 -->
    <div role="tabpanel" class="tab-pane fade" id="variant4">
        <div class="row">
            <div class="col-md-12">
                <h2>Вариант 4: Модель и прогнозирование</h2>
                <p>Выбор целевой переменной, построение и обучение модели, получение прогноза для новых данных, введённых пользователем.</p>
                <p><a class="btn btn-primary" href="/variant4">Перейти к прогнозу &raquo;</a></p>
            </div>
        </div>
    </div>
</div>