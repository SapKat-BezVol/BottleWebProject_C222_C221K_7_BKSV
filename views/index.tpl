% rebase('layout.tpl', title='Главная', year=year)

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
            <h2>Вариант 1: Анализ распределений и статистик</h2>
            <p class="lead">Комплексный анализ распределений данных с проверкой на нормальность и выявлением аномалий</p>
            
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
            
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Описание решения</h3>
                </div>
                <div class="panel-body">
                    <div class="row">
                        <div class="col-md-6">
                            <h4>Основные этапы анализа:</h4>
                            <ol>
                                <li><strong>Визуализация распределений</strong>
                                    <ul>
                                        <li>Гистограммы с кривыми плотности</li>
                                        <li>Ящики с усами (boxplot)</li>
                                        <li>Сравнение с нормальным распределением</li>
                                    </ul>
                                </li>
                                <li><strong>Проверка на нормальность</strong>
                                    <ul>
                                        <li>Тест Шапиро-Уилка</li>
                                        <li>Анализ асимметрии и эксцесса</li>
                                        <li>Q-Q графики</li>
                                    </ul>
                                </li>
                            </ol>
                        </div>
                        <div class="col-md-6">
                            <div class="well">
                                <h4>Пример гистограммы с пояснениями</h4>
                                <div class="row">
                                    <div class="col-md-6">
                                        <img src="/static/images/primeri/gistogramma.png" class="img-responsive" alt="Гистограмма">
                                    </div>
                                    <div class="col-md-6">
                                        <ul class="list-unstyled">
                                            <li><strong>Форма:</strong> Симметричность</li>
                                            <li><strong>Мода:</strong> Пик распределения</li>
                                            <li><strong>Хвосты:</strong> Плавное затухание</li>
                                            <li><strong>Выбросы:</strong> Отсутствуют</li>
                                            <li><strong>Нормальность:</strong> p-value > 0.05</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <h4>Математическое обоснование:</h4>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <h5>1. Основные статистические характеристики:</h5>
                            <p><strong>Среднее значение:</strong></p>
                            <p>\[ \bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i \]</p>
                            <p class="small">где \( \bar{x} \) - среднее, \( n \) - количество наблюдений, \( x_i \) - отдельные значения</p>
                            
                            <p><strong>Дисперсия:</strong></p>
                            <p>\[ s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2 \]</p>
                            <p class="small">где \( s^2 \) - дисперсия, мера разброса данных</p>
                        </div>
                        <div class="col-md-6">
                            <h5>2. Коэффициенты формы:</h5>
                            <p><strong>Асимметрия:</strong></p>
                            <p>\[ \gamma_1 = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^3}{s^3} \]</p>
                            <p class="small">\( \gamma_1 > 0 \) - правосторонняя асимметрия, \( \gamma_1 < 0 \) - левосторонняя</p>
                            
                            <p><strong>Эксцесс:</strong></p>
                            <p>\[ \gamma_2 = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^4}{s^4} - 3 \]</p>
                            <p class="small">\( \gamma_2 > 0 \) - островершинное, \( \gamma_2 < 0 \) - плосковершинное</p>
                        </div>
                    </div>

                    <div class="row mt-3">
                        <div class="col-md-6">
                            <h5>3. Тест Шапиро-Уилка:</h5>
                            <p>\[ W = \frac{(\sum_{i=1}^{n}a_i x_{(i)})^2}{\sum_{i=1}^{n}(x_i - \bar{x})^2} \]</p>
                            <p class="small">где \( W \) - статистика теста (0-1), \( a_i \) - константы, \( x_{(i)} \) - упорядоченные значения</p>
                        </div>
                        <div class="col-md-6">
                            <h5>4. Метод IQR для выбросов:</h5>
                            <p>\[ \text{IQR} = Q_3 - Q_1 \]</p>
                            <p>\[ \text{Выбросы} = \begin{cases} 
                            x < Q_1 - 1.5 \times IQR \\
                            x > Q_3 + 1.5 \times IQR 
                            \end{cases} \]</p>
                            <p class="small">где \( Q_1 \) - 25-й перцентиль, \( Q_3 \) - 75-й перцентиль</p>
                        </div>
                    </div>

                    <h4 class="mt-4">Критерии нормальности:</h4>
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead>
                                <tr class="active">
                                    <th>Параметр</th>
                                    <th>Нормальное</th>
                                    <th>Ненормальное</th>
                                    <th>Интерпретация</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Асимметрия (\( \gamma_1 \))</td>
                                    <td>\( |\gamma_1| \leq 0.5 \)</td>
                                    <td>\( |\gamma_1| > 0.5 \)</td>
                                    <td>Симметричность распределения</td>
                                </tr>
                                <tr>
                                    <td>Эксцесс (\( \gamma_2 \))</td>
                                    <td>\( |\gamma_2| \leq 0.5 \)</td>
                                    <td>\( |\gamma_2| > 0.5 \)</td>
                                    <td>"Острота" пика распределения</td>
                                </tr>
                                <tr>
                                    <td>Тест Шапиро-Уилка (p-value)</td>
                                    <td>> 0.05</td>
                                    <td>≤ 0.05</td>
                                    <td>Статистическая значимость отклонения от нормальности</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="alert alert-info mt-4">
                        <h4>Рекомендации по анализу:</h4>
                        <div class="row">
                            <div class="col-md-6">
                                <strong>Для нормальных данных:</strong>
                                <ul>
                                    <li>t-тесты и ANOVA</li>
                                    <li>Линейная регрессия</li>
                                    <li>Доверительные интервалы</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <strong>Для ненормальных данных:</strong>
                                <ul>
                                    <li>U-тест Манна-Уитни</li>
                                    <li>Преобразование Бокса-Кокса</li>
                                    <li>Робастные методы</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="text-left mt-4">
                <a class="btn btn-primary btn-lg" href="/variant1">Начать анализ &raquo;</a>
            </div>
        </div>
    </div>
</div>

    <!-- Вариант 2 -->
    <div role="tabpanel" class="tab-pane fade" id="variant2">
      <div class="row">
        <div class="col-md-12">
          <h2>Вариант 2: Корреляции и тепловая карта</h2>

                      <hr>
            <h3>Как работает корреляция и как она вычисляется</h3>

            <p>
              <strong>Корреляция</strong> — это числовой показатель, отражающий <em>насколько сильно</em> и <em>в каком направлении</em> связаны две количественные переменные.
            </p>

            <h4>Что делает корреляция:</h4>
            <ul>
              <li>Измеряет <strong>силу линейной зависимости</strong> между переменными.</li>
              <li>Показывает, увеличивается или уменьшается одна переменная при изменении другой.</li>
              <li>Имеет значение от <strong>-1 до +1</strong>.</li>
            </ul>

            <div style="background-color:#f8f9fa;border-left:4px solid #007bff;padding:1em;margin-bottom:1em;">
              <p><strong>Значения коэффициента корреляции \( r \):</strong></p>
              <ul>
                <li><strong>\( r = +1 \)</strong> — идеальная положительная связь</li>
                <li><strong>\( r = 0 \)</strong> — переменные не связаны линейно</li>
                <li><strong>\( r = -1 \)</strong> — идеальная отрицательная связь</li>
              </ul>
            </div>

            <h4>Формула корреляции Пирсона</h4>

            <p>Для двух переменных \( X \) и \( Y \) с \( n \) наблюдениями:</p>

            <p style="text-align:center;font-size:120%;">
              \[
              r = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}
              {\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \cdot \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}
              \]
            </p>

            <p>
              Где:
            </p>
            <ul>
              <li>\( x_i, y_i \) — значения переменных \( X \) и \( Y \) на \( i \)-м наблюдении</li>
              <li>\( \bar{x}, \bar{y} \) — средние значения переменных</li>
              <li>\( n \) — количество наблюдений (строк)</li>
            </ul>

            <h4>Как работает эта формула:</h4>
            <ol>
              <li>Сначала находятся средние значения: \( \bar{x}, \bar{y} \)</li>
              <li>Вычисляются отклонения от среднего: \( x_i - \bar{x}, y_i - \bar{y} \)</li>
              <li>Умножаются попарно эти отклонения и суммируются</li>
              <li>В знаменателе — произведение стандартных отклонений (корни квадратов сумм отклонений)</li>
            </ol>

            <p>
              Таким образом, корреляция — это <strong>нормализованная ковариация</strong>: насколько два признака изменяются совместно, по сравнению с их вариацией в отдельности.
            </p>


            <h4>Важное условие: одинаковое число строк</h4>
            <p>
              Все переменные в таблице должны иметь одинаковое число наблюдений (строк), иначе корреляцию посчитать нельзя.
            </p>

            <div style="background:#fff3cd;border-left:4px solid #ffc107;padding:1em;margin-bottom:1em;">
              <strong>Если в одной колонке 100 значений, а в другой — 98:</strong><br>
              Нельзя сопоставить строки по индексу. Возникает ошибка или пропущенные значения (NaN).
            </div>

            <p>
              Перед анализом нужно:
            </p>
            <ul>
              <li>Удалить строки с пропущенными значениями;</li>
              <li>Заполнить пропуски (например, средним или медианой);</li>
              <li>Или исключить неполные переменные.</li>
            </ul>

            <h4>Пример на Python</h4>

            <pre><code>import pandas as pd

            data = {
                "X": [1, 2, 3, 4, 5],
                "Y": [2, 4, 6, 8, 10],
                "Z": [5, 3, 6, 2, 7]
            }

            df = pd.DataFrame(data)
            print(df.corr())</code></pre>

            <p><strong>Результат:</strong></p>
            <pre><code>          X         Y         Z
            X  1.000000  1.000000  0.000000
            Y  1.000000  1.000000  0.000000
            Z  0.000000  0.000000  1.000000
            </code></pre>

            <p>
              Из этого видно:
              <ul>
                <li>между X и Y — идеальная положительная корреляция,</li>
                <li>Z не связана с X и Y.</li>
              </ul>
            </p>

            <p>Теперь вы можете понимать и интерпретировать результаты тепловой карты с полным осознанием статистического смысла!</p>


          <p><a class="btn btn-primary" href="/variant2">Перейти к анализу &raquo;</a></p>
        </div>
      </div>
    </div>

    <!-- Вариант 3 -->
    <div role="tabpanel" class="tab-pane fade" id="variant3">
        <div class="row">
            <div class="col-md-12">

                <h2>Вариант 3: Графики и scatter-matrix</h2>
                <p class="lead">Различные диаграммы для каждого столбца, матрица рассеяния и визуализация выявленных зависимостей</p>

                <script id="MathJax-script" async
                        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h3 class="panel-title">Описание решения</h3>
                    </div>

                    <div class="panel-body">

                        <h4>1. Гистограмма распределения</h4>

                        <h5>1.1. Назначение</h5>
                        <p>Гистограмма&nbsp;— ключевой инструмент одномерного анализа, позволяющий визуально оценить форму распределения, наличие асимметрии,
                           мультимодальности и выбросов.</p>

                        <h5>1.2. Логическая структура данных</h5>
                        <p>Требуется одноколонный числовой массив размера \(N\). Каждая гистограмма отражает <em>все</em> наблюдения выбранного
                           столбца, независимо от того, какая подвыборка отображена пользователю.</p>

                        <h5>1.3. Алгоритм построения</h5>
                        <ol>
                            <li>Определяем диапазон: \(\min(x),\;\max(x)\).</li>
                            <li>Выбираем число бинов по правилу Стерджесса:
                                \[
                                    k=\Bigl\lceil \log_{2}N+1 \Bigr\rceil
                                \]</li>
                            <li>Ширина бина:
                                \[
                                    h=\frac{\max(x)-\min(x)}{k}
                                \]</li>
                            <li>Считаем частоту значений в каждом интервале и строим вертикальные прямоугольники;
                                по оси \(Y\) можно отображать абсолютные, относительные частоты или плотность.</li>
                        </ol>

                        <h5>1.4. Особенности обработки</h5>
                        <ul>
                            <li>Пропущенные значения исключаются.</li>
                            <li>Выбросы попадают в крайние интервалы и визуально выделяются.</li>
                            <li>При необходимости ось \(X\) может быть логарифмирована.</li>
                        </ul>

                        <div class="row">
                            <div class="col-md-4">
                                <div class="thumbnail">
                                    <img src="/static/images/primeri/gistogramma.png" alt="Пример гистограммы">
                                    <div class="caption">
                                        <h5>Пример гистограммы</h5>
                                        <p>Распределение показателя с двумя модами</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <hr>

                        <h4>2. Ящичковая диаграмма (Box-plot)</h4>

                        <h5>2.1. Назначение</h5>
                        <p>Box-plot компактен и нагляден: отображает медиану, квартили, межквартильный размах и выбросы,
                           упрощая сравнение распределений между группами.</p>

                        <h5>2.2. Логическая структура данных</h5>
                        <p>Одномерная числовая выборка либо несколько выборок, если требуется
                           сравнить группы. Все доступные значения участвуют в вычислении статистик.</p>

                        <h5>2.3. Алгоритм построения</h5>
                        <ol>
                            <li>Сортировка значений: \(x_{(1)}\le\ldots\le x_{(N)}\).</li>
                            <li>Квартильные статистики:
                                \[
                                    Q_1,\;Q_2,\;Q_3;\qquad IQR = Q_3 - Q_1
                                \]</li>
                            <li>Усы по правилу Тьюки:
                                \[
                                    \text{Нижний ус}=Q_1-1.5\,IQR,\quad
                                    \text{Верхний ус}=Q_3+1.5\,IQR
                                \]</li>
                            <li>Точки за пределами усов — выбросы, отображаются отдельно.</li>
                        </ol>

                        <h5>2.4. Особенности обработки</h5>
                        <ul>
                            <li>NaN исключаются.</li>
                            <li>Масштаб оси общий для всех «ящиков» на графике.</li>
                            <li>При сильной асимметрии возможна лог-шкала.</li>
                        </ul>

                        <div class="row">
                            <div class="col-md-4">
                                <div class="thumbnail">
                                    <img src="/static/images/primeri/boxplot.png" alt="Пример box-plot">
                                    <div class="caption">
                                        <h5>Пример box-plot</h5>
                                        <p>Сравнение двух групп данных</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <hr>

                        <h4>3. Матрица диаграмм рассеяния (Scatter Matrix)</h4>

                        <h5>3.1. Назначение</h5>
                        <p>Матрица рассеяния позволяет одновременно оценить все парные зависимости между \(p\) числовыми
                           признаками таблицы и быстро выявить корреляции, кластеры и выбросы.</p>

                        <h5>3.2. Логическая структура данных</h5>
                        <p>Исходные данные — таблица \(N\times p\) числовых значений. Для каждой пары
                           \((X_i,X_j)\) строится точечный график; на диагонали обычно размещают гистограммы
                           отдельных признаков.</p>

                        <h5>3.3. Алгоритм построения</h5>
                        <ol>
                            <li>Выбор \(p\) переменных (2 ≤ \(p\) ≤ 10).</li>
                            <li>Создание сетки \(p\times p\); для \(i\neq j\) — scatter-plot всех \(N\) наблюдений,
                                для \(i=j\) — гистограмма или KDE.</li>
                            <li>При необходимости отображение коэффициента корреляции
                                \[
                                    r_{ij}=
                                    \frac{\displaystyle\sum_{k=1}^{N}(x_{ki}-\bar{x}_i)(x_{kj}-\bar{x}_j)}
                                         {\sqrt{\displaystyle\sum_{k=1}^{N}(x_{ki}-\bar{x}_i)^2
                                                \sum_{k=1}^{N}(x_{kj}-\bar{x}_j)^2}}
                                \]</li>
                        </ol>

                        <h5>3.4. Особенности обработки</h5>
                        <ul>
                            <li>При наличии пропусков пара \((x_{ki},x_{kj})\) не отображается.</li>
                            <li>При сильном различии масштабов отдельных признаков возможна стандартизация
                                или лог-шкала по выбранной оси.</li>
                        </ul>

                        <div class="row">
                            <div class="col-md-4">
                                <div class="thumbnail">
                                    <img src="/static/images/primeri/scattermatrix.png" alt="Пример scatter-matrix">
                                    <div class="caption">
                                        <h5>Пример scatter-matrix</h5>
                                        <p>Парные связи между четырьмя переменными</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <hr>

                        <h4>4. Итог</h4>
                        <p>Гистограммы раскрывают распределения отдельных признаков, box-plot
                           конденсирует ключевые статистики и выбросы, а scatter-matrix
                           демонстрирует структуру многомерных взаимосвязей. Комплексное использование
                           этих диаграмм обеспечивает глубокое понимание таблицы данных и служит основой
                           для последующего моделирования.</p>

                    </div>
                </div>

                <p><a class="btn btn-primary btn-lg" href="/variant3">Перейти к графикам &raquo;</a></p>
            </div>
        </div>
    </div> 

    <!-- Вариант 4 -->
    <div role="tabpanel" class="tab-pane fade" id="variant4">
      <div class="row">
        <div class="col-md-12">
          <h2>Вариант 4: Модель и прогнозирование</h2>
      
          <div class="alert alert-info">
            <h4>Алгоритм работы системы прогнозирования</h4>
            <p>Пошаговый процесс от ввода данных до получения прогноза:</p>
          </div>

          <h3>1. Входные данные</h3>
          <p>Система принимает:</p>
          <ul>
            <li><strong>k = номер столбца-1</strong> - индекс целевой переменной (нумерация с 0)</li>
            <li><strong>S = {s₁, s₂, ..., sₙ}</strong> - множество значений признаков для прогноза</li>
          </ul>
      
          <div class="alert alert-warning">
            <strong>Пример:</strong> Если в таблице 5 столбцов, допустимые значения k: 0, 1, 2, 3, 4
          </div>

          <h3>2. Проверка корректности</h3>
          <p>Выполняется валидация:</p>
          <div style="text-align:center; margin:20px 0;">
            \[ k \in [0, N-1] \]
          </div>
          <p>где <em>N</em> - общее количество столбцов в данных.</p>

          <h3>3. Подготовка данных</h3>
          <p>При успешной проверке:</p>
          <div style="text-align:center; margin:20px 0;">
            \[ \begin{cases}
            y = X[:,k] & \text{(целевая переменная)} \\
            X = X \setminus \{x_k\} & \text{(матрица признаков)}
            \end{cases} \]
          </div>

          <h3>4. Преобразование входных значений</h3>
          <p>Введенные признаки преобразуются:</p>
          <div style="text-align:center; margin:20px 0;">
            \[ F = \{f(s₁), f(s₂), ..., f(sₙ)\} \]
          </div>
          <p>где <em>f: s → ℝ</em> - функция преобразования строки в число.</p>

          <h3>5. Проверка размерности</h3>
          <p>Система проверяет соответствие количества признаков:</p>
          <div style="text-align:center; margin:20px 0;">
            \[ |F| = \dim(X) \]
          </div>
          <p>где <em>dim(X)</em> - количество признаков в обучающих данных.</p>

          <h3>6. Построение модели</h3>
          <p>Создается модель линейной регрессии:</p>
          <div style="text-align:center; margin:20px 0;">
            \[ M(\theta) = \theta₀ + \theta₁x₁ + ... + \thetaₙxₙ \]
          </div>

          <h3>7. Обучение модели</h3>
          <p>Нахождение оптимальных параметров:</p>
          <div style="text-align:center; margin:20px 0;">
            \[ \theta^* = \underset{\theta}{\mathrm{argmin}}\sum(yᵢ - M(xᵢ))² \]
          </div>

          <h3>8. Прогнозирование</h3>
          <p>Вычисление прогнозируемого значения:</p>
          <div style="text-align:center; margin:20px 0;">
            \[ ŷ = M(F) \]
          </div>

          <div class="alert alert-success" style="margin-top:30px;">
            <h4>Пример практического применения</h4>
            <p>Допустим, мы хотим предсказать цену дома на основе его характеристик:</p>
            <ul>
              <li>Выбираем столбец "Цена" как целевую переменную (k=3)</li>
              <li>Вводим значения признаков: площадь=120, комнаты=3, этаж=5</li>
              <li>Система вычисляет: ŷ = θ₀ + θ₁·120 + θ₂·3 + θ₃·5</li>
              <li>Возвращает прогнозируемую цену, например: 9,500,000 руб.</li>
            </ul>
          </div>

          <h3>Возможные ошибки</h3>
          <div class="alert alert-danger">
            <ul>
              <li><strong>k ∉ допустимому диапазону</strong> - некорректный номер столбца</li>
              <li><strong>|F| ≠ dim(X)</strong> - количество введенных признаков не соответствует обучающим данным</li>
              <li><strong>Некорректные значения</strong> - ввод текста вместо чисел</li>
            </ul>
          </div>

          <p><a class="btn btn-primary btn-lg" href="/variant4">Начать прогнозирование &raquo;</a></p>
        </div>
      </div>
    </div>
</div>