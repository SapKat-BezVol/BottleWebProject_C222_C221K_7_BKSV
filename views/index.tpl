% rebase('layout.tpl', title='Главная', year=year)
<!-- Главная страница с четырьмя вкладками для вариантов анализа -->
<div class="jumbotron">
   <h1>Элементы машинного обучения и анализа данных</h1>
</div>
<!-- Навигационные вкладки -->
<ul class="nav nav-tabs" id="variantTabs" role="tablist">
   <li role="presentation" class="active">
      <a href="#variant1" aria-controls="variant1" role="tab" data-toggle="tab">Вариант 1 <small>Статистика</small></a>
   </li>
   <li role="presentation">
      <a href="#variant2" aria-controls="variant2" role="tab" data-toggle="tab">Вариант 2 <small>Корреляции</small></a>
   </li>
   <li role="presentation">
      <a href="#variant3" aria-controls="variant3" role="tab" data-toggle="tab">Вариант 3 <small>Графики</small></a>
   </li>
   <li role="presentation">
      <a href="#variant4" aria-controls="variant4" role="tab" data-toggle="tab">Вариант 4 <small>Прогноз</small></a>
   </li>
</ul>
<!-- Содержимое вкладок -->
<div class="tab-content" style="margin-left: 20px; margin-right: 20px">
   <!-- Вариант 1 -->
   <div role="tabpanel" class="tab-pane fade in active" id="variant1">
   <div class="row">
      <div class="col-md-12">
         <h2>Вариант 1: Анализ распределений и статистик</h2>
         <p class="lead">Комплексный анализ распределений данных с проверкой на нормальность и выявлением аномалий</p>
         <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script> 
         <div class="panel" style="border: none; box-shadow: none;">
            <div class="panel-heading" style="border: none; background: none; padding-left: 0;">
               <h3 class="panel-title">Описание решения</h3>
            </div>
            <div class="panel-body" style="padding-left: 0; padding-right: 0;">
               <div class="row">
                  <div class="col-md-6">
                     <h4>Основные этапы анализа:</h4>
                     <ol>
                        <li>
                           <strong>Визуализация распределений</strong>
                           <ul>
                              <li>Гистограммы с кривыми плотности</li>
                              <li>Ящики с усами (boxplot)</li>
                              <li>Сравнение с нормальным распределением</li>
                           </ul>
                        </li>
                        <li>
                           <strong>Проверка на нормальность</strong>
                           <ul>
                              <li>Тест Шапиро-Уилка</li>
                              <li>Анализ асимметрии и эксцесса</li>
                              <li>Q-Q графики</li>
                           </ul>
                        </li>
                     </ol>
                  </div>
                  <div class="col-md-6">
                     <div style="background: none; border: none; box-shadow: none;">
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
                     <p class="small">
                         где \( \bar{x} \) — среднее значение выборки,<br>
                         \( n \) — количество наблюдений,<br>
                         \( x_i \) — отдельное значение из выборки.
                     </p>

                     <p><strong>Дисперсия:</strong></p>
                     <p>\[ s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2 \]</p>
                     <p class="small">
                         где \( s^2 \) — несмещённая оценка дисперсии,<br>
                         \( x_i \) — значения выборки,<br>
                         \( \bar{x} \) — среднее значение.
                     </p>
                  </div>
                  <div class="col-md-6">
                     <h5>2. Коэффициенты формы:</h5>
                     <p><strong>Асимметрия:</strong></p>
                     <p>\[ \gamma_1 = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^3}{s^3} \]</p>
                     <p>
                        где \( \gamma_1 \) — коэффициент асимметрии,<br>
                        \( x_i \) — значения выборки,<br>
                        \( \bar{x} \) — среднее значение,<br>
                        \( s \) — стандартное отклонение.
                     </p>
                     <p><strong>Эксцесс:</strong></p>
                     <p>\[ \gamma_2 = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^4}{s^4} - 3 \]</p>
                     <p class="small">
                         где \( \gamma_2 \)  — коэффициент эксцесса,<br>
                         \( x_i \) — значения выборки,<br>
                         \( \bar{x} \) — среднее,<br>
                         \( s \) — стандартное отклонение.
                     </p>
                  </div>
               </div>
               <div class="row mt-3">
                  <div class="col-md-6">
                     <h5>3. Тест Шапиро-Уилка:</h5>
                     <p>\[ W = \frac{(\sum_{i=1}^{n}a_i x_{(i)})^2}{\sum_{i=1}^{n}(x_i - \bar{x})^2} \]</p>
                     <p class="small">
                         где $ W $ — статистика теста (значение от 0 до 1),<br>
                         \( a_i \) — весовые коэффициенты,<br>
                         \( x_{(i)} \) — упорядоченные данные (по возрастанию),<br>
                         \( \bar{x} \) — среднее значение выборки.
                     </p>
                  </div>
                  <div class="col-md-6">
                     <h5>4. Метод IQR для выбросов:</h5>
                     <p>\[ \text{IQR} = Q_3 - Q_1 \]</p>
                     <p>\[ \text{Выбросы} = \begin{cases} 
                        x < Q_1 - 1.5 \times \text{IQR} \\
                        x > Q_3 + 1.5 \times \text{IQR} 
                        \end{cases} \]
                     </p>
                     <p class="small">
                         где $ \text{IQR} $ — межквартильный размах,<br>
                         \( Q_1 \) — первый квартиль (25%),<br>
                         \( Q_3 \) — третий квартиль (75%),<br>
                         \( x \) — значение из выборки.
                     </p>
                  </div>
               </div>
               <h4 class="mt-4">Критерии нормальности:</h4>
               <div class="table-responsive">
                  <table class="table" style="border: none;">
                     <thead>
                        <tr style="background-color: #f8f9fa;">
                           <th style="border: none;">Параметр</th>
                           <th style="border: none;">Нормальное</th>
                           <th style="border: none;">Ненормальное</th>
                           <th style="border: none;">Интерпретация</th>
                        </tr>
                     </thead>
                     <tbody>
                        <tr>
                           <td style="border: none;">Асимметрия (\( \gamma_1 \))</td>
                           <td style="border: none;">\( |\gamma_1| \leq 0.5 \)</td>
                           <td style="border: none;">\( |\gamma_1| > 0.5 \)</td>
                           <td style="border: none;">Симметричность распределения</td>
                        </tr>
                        <tr>
                           <td style="border: none;">Эксцесс (\( \gamma_2 \))</td>
                           <td style="border: none;">\( |\gamma_2| \leq 0.5 \)</td>
                           <td style="border: none;">\( |\gamma_2| > 0.5 \)</td>
                           <td style="border: none;">"Острота" пика распределения</td>
                        </tr>
                        <tr>
                           <td style="border: none;">Тест Шапиро-Уилка (p-value)</td>
                           <td style="border: none;">> 0.05</td>
                           <td style="border: none;">≤ 0.05</td>
                           <td style="border: none;">Статистическая значимость отклонения от нормальности</td>
                        </tr>
                     </tbody>
                  </table>
               </div>
               <div class="alert alert-info mt-4" style="border: none;">
                  <h4>Общие рекомендации по анализу данных:</h4>
                  <div class="row">
                     <div class="col-md-6">
                        <strong>1. Подготовка данных:</strong>
                        <ul>
                           <li>Всегда начинайте с визуального анализа распределений</li>
                           <li>Проверяйте данные на наличие пропущенных значений</li>
                           <li>Исследуйте выбросы - могут ли они быть ошибками измерений?</li>
                           <li>Рассмотрите возможность логарифмического преобразования для правосторонних асимметричных данных</li>
                        </ul>
                        <strong>2. Для нормальных распределений (p-value > 0.05):</strong>
                        <ul>
                           <li><u>Параметрические тесты:</u> t-тест, ANOVA</li>
                           <li><u>Методы:</u> Линейная регрессия, доверительные интервалы</li>
                           <li><u>Преимущество:</u> Большая мощность тестов при меньшем объеме выборки</li>
                        </ul>
                     </div>
                     <div class="col-md-6">
                        <strong>3. Для ненормальных распределений (p-value ≤ 0.05):</strong>
                        <ul>
                           <li><u>Непараметрические тесты:</u> U-тест Манна-Уитни, критерий Краскела-Уоллиса</li>
                           <li><u>Методы:</u> Робастная регрессия, ранговые преобразования</li>
                           <li><u>Альтернативы:</u> Преобразование Бокса-Кокса, обрезанные средние</li>
                        </ul>
                        <strong>4. Интерпретация результатов:</strong>
                        <ul>
                           <li>Всегда учитывайте размер эффекта, а не только p-value</li>
                           <li>Для небольших выборок (n < 30) используйте непараметрические методы</li>
                           <li>При неоднозначных результатах теста на нормальность дублируйте анализ обоими методами</li>
                        </ul>
                     </div>
                  </div>
                  <div class="mt-3 p-3 rounded" style="background-color: #f8f9fa;">
                     <strong>Важно!</strong> Нормальность распределения проверяйте только для остатков в регрессионных моделях. 
                     Для больших выборок (n > 500) тесты на нормальность могут давать значимые результаты даже при небольших отклонениях от нормальности.
                  </div>
               </div>
            </div>
         </div>
         <div class="text-left mt-4">
            <a class="custom-btn" href="/variant1">Начать анализ &raquo;</a>
         </div>
      </div>
   </div>
</div>
   <!-- Вариант 2 -->
   <div role="tabpanel" class="tab-pane fade" id="variant2">
      <div class="row">
         <div class="col-md-12">
            <h2>Вариант 2: Корреляции и тепловая карта</h2>
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
            <p>
                <a class="custom-btn" href="/variant2">Перейти к анализу &raquo;</a>
            </p>
         </div>
      </div>
   </div>
   <div role="tabpanel" class="tab-pane fade in" id="variant3" style="line-height:1.7;">
      <div class="row">
         <div class="col-md-12">
            <h2>Вариант 3: Графики и scatter-matrix</h2>
            <p class="lead">Визуализация распределений и зависимостей: гистограммы, ящичковые диаграммы и scatter-matrix</p>
            <!-- Описание предметной области -->
            <section class="row mb-3 d-flex flex-wrap">
               <div class="col-md-12">
                  <h3>Описание предметной области</h3>
                  <p class="mb-0">
                     Раздел посвящён визуализации табличных данных, содержащих <strong>1–10 числовых признаков</strong> и до <strong>1000 наблюдений</strong>. Используются три базовых графика разведочного анализа:
                  </p>
                  <ul class="mb-1">
                     <li><strong>Гистограмма</strong> — отображает распределение одного признака, помогает выявить форму, асимметрию, мультимодальность и выбросы.</li>
                     <li><strong>Box-plot</strong> — показывает медиану, квартили, межквартильный размах и выбросы; удобен для сравнения групп.</li>
                     <li><strong>Scatter-matrix</strong> — обзор всех парных корреляций между признаками, обнаружение кластеров.</li>
                  </ul>
                  <p class="mt-1">
                     Каждый график строится <em>по всей выборке</em>, вне зависимости от того, сколько строк видно на экране; это обеспечивает корректную статистическую интерпретацию.
                  </p>
               </div>
            </section>
            <!-- Теория и примеры -->
            <section class="row mb-3 d-flex flex-wrap">
               <div class="col-md-6">
                  <h3>Теория и примеры</h3>
                  <h4>Основные этапы визуализации</h4>
                  <ul class="mb-1">
                     <li><strong>Гистограмма</strong>: выбор числа бинов <span class="text-muted">(Стерджесс)</span>, подсчёт частот, маркировка выбросов.</li>
                     <li><strong>Box-plot</strong>: расчёт квартилей, усов Тьюки (<span class="text-muted">1.5 IQR</span>), выделение выбросов.</li>
                     <li><strong>Scatter-matrix</strong>: p×p-сетка парных scatter-plot; диагональ — гистограммы/KDE.</li>
                  </ul>
                  <ul class="list-unstyled">
                     <li><strong>Размер выборки:</strong> \( N \leq 1000 \)</li>
                     <li><strong>Пропуски:</strong> игнорируются</li>
                     <li><strong>Масштаб:</strong> log-шкала при сильной асимметрии</li>
                  </ul>
               </div>
               <div class="col-md-6 text-center">
                  <h4 class="hidden-md hidden-lg">&nbsp;</h4>
                  <div class="row d-flex flex-wrap">
                     <div class="col-xs-4">
                        <img src="/static/images/primeri/gistogramma.png" class="img-thumbnail" style="max-width:100%;" alt="Гистограмма">
                        <p class="small mt-1">Гистограмма</p>
                     </div>
                     <div class="col-xs-4">
                        <img src="/static/images/primeri/boxplot.png" class="img-thumbnail" style="max-width:100%;" alt="Box-plot">
                        <p class="small mt-1">Box-plot</p>
                     </div>
                     <div class="col-xs-4">
                        <img src="/static/images/primeri/scattermatrix.png" class="img-thumbnail" style="max-width:100%;" alt="Scatter-matrix">
                        <p class="small mt-1">Scatter-matrix</p>
                     </div>
                  </div>
               </div>
            </section>
            <!-- Гистограмма -->
            <section class="row mb-3">
               <div class="col-md-12">
                  <h3>1. Гистограмма</h3>
                  <h4>Назначение</h4>
                  <p>Оценивает форму распределения: асимметрию, мультимодальность, выбросы; даёт быструю оценку центра и разброса.</p>
                  <h4>Структура данных</h4>
                  <p>Одноколонный массив \( N \) чисел. Гистограмма строится по <strong>всем</strong> наблюдениям.</p>
                  <h4>Алгоритм</h4>
                  <ul class="mb-1">
                     <li>
                        Диапазон: \( \min(x), \max(x) \).
                     </li>
                     <li>
                        Число бинов (Стерджесс):
                        <br>
                        \[
                        k = \lceil \log_{2} N + 1 \rceil
                        \]
                        <div class="math-defs">
                           <strong>Обозначения:</strong><br>
                           \( k \) — число бинов (столбцов);<br>
                           \( N \) — размер выборки.
                        </div>
                     </li>
                     <li>
                        Ширина бина:
                        <br>
                        \[
                        h = \frac{\max(x)-\min(x)}{k}
                        \]
                        <div class="math-defs">
                           <strong>Обозначения:</strong><br>
                           \( h \) — ширина одного бина;<br>
                           \( \max(x) \), \( \min(x) \) — максимальное и минимальное значения;<br>
                           \( k \) — число бинов.
                        </div>
                     </li>
                     <li>Частоты → столбики; при необходимости нормировать до плотности.</li>
                  </ul>
                  <h4>Особенности</h4>
                  <ul>
                     <li>NaN исключаются.</li>
                     <li>Выбросы попадают в крайние интервалы.</li>
                     <li>При длинных хвостах — log-шкала.</li>
                  </ul>
                  <p class="mt-1">
                     <em>Оптимальная ширина KDE (Silverman):</em>
                     <br>
                     \[
                     h_\mathrm{opt} = 0.9 \min\left(s, \frac{\mathrm{IQR}}{1.34}\right) N^{-1/5}
                     \]
                  <div class="math-defs">
                     <strong>Обозначения:</strong><br>
                     \( h_\mathrm{opt} \) — оптимальная ширина окна ядра;<br>
                     \( s \) — стандартное отклонение;<br>
                     \( \mathrm{IQR} \) — межквартильный размах (\( Q_3 - Q_1 \));<br>
                     \( N \) — число наблюдений.
                  </div>
                  </p>
               </div>
            </section>
            <!-- Box-plot -->
            <section class="row mb-3">
               <div class="col-md-12">
                  <h3>2. Box-plot</h3>
                  <h4>Назначение</h4>
                  <p>Компактно показывает медиану, IQR и выбросы; удобен для сравнения групп.</p>
                  <h4>Структура данных</h4>
                  <p>Одна или несколько выборок чисел; каждая выборка — отдельный ящик.</p>
                  <h4>Алгоритм</h4>
                  <ul class="mb-1">
                     <li>Сортировка выборки.</li>
                     <li>
                        Квартильные статистики:
                        <br>
                        \( Q_1, Q_2, Q_3,\, \mathrm{IQR} = Q_3 - Q_1 \)
                        <div class="math-defs">
                           <strong>Обозначения:</strong><br>
                           \( Q_1 \) — первый квартиль (25%);<br>
                           \( Q_2 \) — медиана (50%);<br>
                           \( Q_3 \) — третий квартиль (75%);<br>
                           \( \mathrm{IQR} \) — межквартильный размах.
                        </div>
                     </li>
                     <li>
                        Усы Тьюки:
                        <br>
                        \[
                        L = Q_1 - 1.5\,\mathrm{IQR}, \quad U = Q_3 + 1.5\,\mathrm{IQR}
                        \]
                        <div class="math-defs">
                           <strong>Обозначения:</strong><br>
                           \( L \) — нижняя граница "усов";<br>
                           \( U \) — верхняя граница "усов";<br>
                           \( Q_1 \), \( Q_3 \) — квартильные значения;<br>
                           \( \mathrm{IQR} \) — межквартильный размах.
                        </div>
                     </li>
                     <li>Точки за пределами \( L, U \) — выбросы.</li>
                  </ul>
                  <h4>Особенности</h4>
                  <ul>
                     <li>Пропуски игнорируются.</li>
                     <li>Лог-шкала при сильной асимметрии.</li>
                     <li>При «длинных усах» можно использовать 3 IQR.</li>
                  </ul>
               </div>
            </section>
            <!-- Scatter-matrix -->
            <section class="row mb-3">
               <div class="col-md-12">
                  <h3>3. Scatter-matrix</h3>
                  <h4>Назначение</h4>
                  <p>Показывает все парные зависимости между \( p \) признаками (\( 2 \leq p \leq 10 \)); помогает выявлять корреляции, кластеры и выбросы.</p>
                  <h4>Структура данных</h4>
                  <p>Таблица \( N \times p \). Ячейка (i, j) содержит точки \( (X_j, X_i) \); диагональ — гистограммы или KDE.</p>
                  <h4>Алгоритм</h4>
                  <ul class="mb-1">
                     <li>Выбор переменных.</li>
                     <li>Создание сетки \( p \times p \).</li>
                     <li>\( i \neq j \): scatter-plot; \( i = j \): гистограмма/KDE.</li>
                     <li>
                        При необходимости коэффициент корреляции:
                        <br>
                        \[
                        r_{ij} = \frac{\sum_k (x_{ki} - \overline{x}_i)(x_{kj} - \overline{x}_j)}
                        {\sqrt{\sum_k (x_{ki} - \overline{x}_i)^2 \sum_k (x_{kj} - \overline{x}_j)^2}}
                        \]
                        <div class="math-defs">
                           <strong>Обозначения:</strong><br>
                           \( r_{ij} \) — коэффициент корреляции между переменными \( i \) и \( j \);<br>
                           \( x_{ki} \) — значение \( i \)-й переменной в наблюдении \( k \);<br>
                           \( \overline{x}_i \) — среднее значение переменной \( i \);<br>
                           \( k \) — индекс наблюдения.
                        </div>
                     </li>
                  </ul>
                  <h4>Особенности</h4>
                  <ul>
                     <li>Записи с NaN в паре \( (X_i, X_j) \) исключаются из этой диаграммы.</li>
                     <li>Лог-шкала для широких диапазонов.</li>
                     <li>Число диаграмм растёт как \( p^2 \); оптимально \( p \leq 10 \).</li>
                  </ul>
                  <p class="mt-1">
                     <em>t-статистика корреляции:</em>
                     <br>
                     \[
                     t = r_{ij} \sqrt{\frac{N-2}{1-r_{ij}^2}},\quad t \sim t_{N-2}
                     \]
                  <div class="math-defs">
                     <strong>Обозначения:</strong><br>
                     \( t \) — t-статистика для проверки значимости корреляции;<br>
                     \( r_{ij} \) — коэффициент корреляции;<br>
                     \( N \) — размер выборки.
                  </div>
                  </p>
               </div>
            </section>
            <!-- Сводка рекомендаций -->
            <section class="row mb-3">
               <div class="col-md-12">
                  <h3>4. Сводка рекомендаций</h3>
                  <div class="table-responsive">
                     <table class="table table-bordered mb-1">
                        <thead>
                           <tr class="active">
                              <th>Диаграмма</th>
                              <th>Наилучшее применение</th>
                              <th>Ключевые выводы</th>
                           </tr>
                        </thead>
                        <tbody>
                           <tr>
                              <td>Гистограмма</td>
                              <td>Оценка распределения</td>
                              <td>Асимметрия, моды, выбросы</td>
                           </tr>
                           <tr>
                              <td>Box-plot</td>
                              <td>Сравнение групп</td>
                              <td>Медиана, IQR, выбросы</td>
                           </tr>
                           <tr>
                              <td>Scatter-matrix</td>
                              <td>Парные зависимости</td>
                              <td>Корреляции, кластеры</td>
                           </tr>
                        </tbody>
                     </table>
                  </div>
               </div>
            </section>
            <!-- Практические советы -->
            <section class="row mb-3">
               <div class="col-md-6">
                  <div class="alert alert-info mb-0">
                     <h4 class="mt-0">Практические советы</h4>
                     <strong>Большие выборки (\( N > 500 \)):</strong>
                     <ul class="mb-1">
                        <li>Прозрачность точек (α-blend)</li>
                        <li>Hex-bin или 2D-KDE для плотных scatter-plot</li>
                        <li>Сократите число бинов в гистограмме</li>
                     </ul>
                  </div>
               </div>
               <div class="col-md-6">
                  <div class="alert alert-info mb-0">
                     <h4 class="hidden-md hidden-lg mt-0">&nbsp;</h4>
                     <strong>Смешанные масштабы:</strong>
                     <ul class="mb-1">
                        <li>Стандартизация перед scatter-matrix</li>
                        <li>Лог-шкала для длиннохвостых положительных распределений</li>
                     </ul>
                  </div>
               </div>
            </section>
            <div class="text-left mt-3">
               <a class="custom-btn" href="/variant3">Перейти к графикам &raquo;</a>
            </div>
         </div>
      </div>
   </div>
   <!-- Вариант 4 -->
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
               <li><strong>k</strong> - номер столбца с целевой переменной (начинается с 1 для удобства пользователя)</li>
               <li><strong>S = {s₁, s₂, ..., sₙ}</strong> - значения признаков для прогноза (вводимые пользователем)</li>
            </ul>
            <div class="alert alert-warning">
               <strong>Пример:</strong> Если таблица содержит столбцы ["Площадь", "Комнаты", "Этаж", "Цена"], то:<br>
               • k=4 выбирает "Цена" как целевую переменную<br>
               • S = [120, 3, 5] - характеристики нового дома
            </div>
            <h3>2. Проверка корректности</h3>
            <p>Выполняется валидация номера столбца:</p>
            <div style="text-align:center; margin:20px 0;">
               \[ 1 \leq k \leq N \]
            </div>
            <p>где <em>N</em> - общее количество столбцов в данных.</p>
            <h3>3. Подготовка данных</h3>
            <p>При успешной проверке данные разделяются:</p>
            <div style="text-align:center; margin:20px 0;">
               \[ \begin{cases}
               y = \text{столбец } k \text{ из таблицы} & \text{(целевая переменная)} \\
               X = \text{все столбцы КРОМЕ } k & \text{(признаки для обучения)}
               \end{cases} \]
            </div>
            <div class="alert alert-secondary">
               <strong>Пояснение:</strong><br>
               • <em>y</em> - вектор значений, которые мы хотим предсказывать<br>
               • <em>X</em> - матрица признаков, используемых для прогноза<br>
            </div>
            <h3>4. Преобразование входных значений</h3>
            <p>Введенные пользователем данные преобразуются в числовой формат:</p>
            <div style="text-align:center; margin:20px 0;">
               \[ F = [\text{float}(s₁), \text{float}(s₂), ..., \text{float}(sₙ)] \]
            </div>
            <p>где каждое значение <em>sᵢ</em> преобразуется в вещественное число.</p>
            <h3>5. Проверка размерности</h3>
            <p>Система проверяет соответствие количества признаков:</p>
            <div style="text-align:center; margin:20px 0;">
               \[ \text{len}(F) = \text{количество столбцов в } X \]
            </div>
            <p>Количество введенных значений должно точно совпадать с количеством признаков модели.</p>
            <h3>6. Построение модели</h3>
            <p>Создается модель линейной регрессии:</p>
            <div style="text-align:center; margin:20px 0;">
               \[ \hat{y} = \theta_0 + \theta_1x_1 + \theta_2x_2 + ... + \theta_nx_n \]
            </div>
            <p>где:<br>
               • <em>θ₀</em> - свободный член (bias)<br>
               • <em>θ₁...θₙ</em> - весовые коэффициенты для каждого признака<br>
               • <em>x₁...xₙ</em> - значения признаков<br>
               • <em>ŷ</em> - прогнозируемое значение
            </p>
            <h3>7. Обучение модели</h3>
            <p>Нахождение оптимальных параметров модели методом наименьших квадратов:</p>
            <div style="text-align:center; margin:20px 0; background:#f8f9fa; padding:15px; border-radius:5px;">
               \[ 
               \min_{\theta} \sum_{i=1}^{m} (y_i - (\theta_0 + \theta_1x_{i1} + \theta_2x_{i2} + ... + \theta_nx_{in}))^2 
               \]
            </div>
            <div class="alert alert-info">
               <h5>Подробное объяснение формулы:</h5>
               <p>Эта формула означает, что мы ищем такие значения параметров θ (тета), при которых <strong>сумма квадратов ошибок</strong> будет минимальной:</p>
               <table class="table table-bordered" style="margin:15px;">
                  <thead>
                     <tr>
                        <th>Элемент</th>
                        <th>Обозначение</th>
                        <th>Пояснение</th>
                        <th>Пример</th>
                     </tr>
                  </thead>
                  <tbody>
                     <tr>
                        <td>Целевое значение</td>
                        <td>y<sub>i</sub></td>
                        <td>Реальное значение из обучающих данных для i-го наблюдения</td>
                        <td>Фактическая цена дома №5: 8,400,000 руб.</td>
                     </tr>
                     <tr>
                        <td>Прогноз модели</td>
                        <td>θ<sub>0</sub> + θ<sub>1</sub>x<sub>i1</sub> + ...</td>
                        <td>Предсказание модели для i-го наблюдения</td>
                        <td>Предсказанная цена: 8,200,000 руб.</td>
                     </tr>
                     <tr>
                        <td>Ошибка</td>
                        <td>(y<sub>i</sub> - ŷ<sub>i</sub>)</td>
                        <td>Разница между реальным и предсказанным значением</td>
                        <td>Ошибка: 200,000 руб.</td>
                     </tr>
                     <tr>
                        <td>Квадрат ошибки</td>
                        <td>(y<sub>i</sub> - ŷ<sub>i</sub>)<sup>2</sup></td>
                        <td>Квадрат разницы (чтобы избежать отрицательных значений)</td>
                        <td>40,000,000,000</td>
                     </tr>
                     <tr>
                        <td>Сумма по всем данным</td>
                        <td>∑<sub>i=1</sub><sup>m</sup></td>
                        <td>Суммируем квадраты ошибок для всех m наблюдений</td>
                        <td>Общая ошибка для 100 домов</td>
                     </tr>
                  </tbody>
               </table>
               <h5 style="margin-top:20px;">Как работает процесс обучения:</h5>
               <ol>
                  <li><strong>Инициализация:</strong> Начинаем со случайных значений θ (обычно нули или малые случайные числа)</li>
                  <li><strong>Расчет ошибки:</strong> Для каждого наблюдения вычисляем разницу между предсказанием и реальным значением</li>
                  <li><strong>Корректировка параметров:</strong> Специальный алгоритм (градиентный спуск) постепенно изменяет θ, чтобы уменьшить общую ошибку</li>
                  <li><strong>Оптимизация:</strong> Процесс повторяется, пока ошибка не перестанет существенно уменьшаться</li>
               </ol>
               <div class="alert alert-warning" style="margin-top:15px;">
                  <strong>Важно:</strong> Этот метод находит оптимальные параметры θ, которые минимизируют среднюю ошибку прогноза на обучающих данных, но не гарантирует идеальную точность на новых данных.
               </div>
            </div>
            <h3>8. Прогнозирование</h3>
            <p>Вычисление прогнозируемого значения для новых данных:</p>
            <div style="text-align:center; margin:20px 0;">
               \[ \hat{y}_{\text{new}} = \theta_0 + \theta_1f_1 + \theta_2f_2 + ... + \theta_nf_n \]
            </div>
            <p>где <em>f₁...fₙ</em> - преобразованные значения признаков из ввода пользователя.</p>
            <h3>Возможные ошибки</h3>
            <div class="alert alert-danger">
               <ul>
                  <li><strong>Некорректный номер столбца</strong> - значение k вне диапазона [1, N]</li>
                  <li><strong>Несоответствие количества признаков</strong> - введено неверное число параметров</li>
                  <li><strong>Ошибки преобразования</strong> - введены нечисловые значения или пустые поля</li>
               </ul>
            </div>
            <div class="text-left mt-3">
               <a class="custom-btn" href="/variant4">Начать прогнозирование &raquo;</a>
            </div>
         </div>
      </div>
   </div>
</div>
