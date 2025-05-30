% rebase('layout.tpl', title='О команде', year=year)

<h2>О команде</h2>

<p><strong>Команда 7</strong>: Безруких, Катаван, Сапрыкин, Володин</p>

<p>Разработка проекта в рамках Учебной практикики по МДК 01.03 <em>Элементы машинного обучения</em> и <em>анализа данных.</em>.</p>

<h3>Исходные данные</h3>
<p>Для анализа используется таблица от 1 до 10 столбцов числовых данных (до 1000 строк). Данные можно:
<ul>
  <li>сгенерировать псевдослучайно (с контролируемой закономерностью);</li>
  <li>загрузить из CSV‑файла.</li>
</ul>
Пользователь выбирает, какую часть таблицы вывести на экран — <code>n</code> первых, <code>n</code> последних или случайные записи — тогда как анализ выполняется по всему набору.</p>

<h3>Варианты анализа</h3>
<ol>
  <li><strong>Распределения и аномалии</strong><br>
      Построим распределения каждого столбца, проверим данные на нормальность, вычислим статистические характеристики (среднее, медиана, стандартное отклонение и т. д.) и определим аномальные значения.</li>
  <li><strong>Корреляционный анализ</strong><br>
      Создадим матрицу корреляций и тепловую карту (<em>heatmap</em>) для поиска линейных зависимостей между столбцами.</li>
  <li><strong>Визуальный анализ</strong><br>
      Построим диаграммы (гистограммы, коробчатые диаграммы, матрицу рассеяния) для каждого столбца и матрицу рассеяния (<em>scatter matrix</em>) для всего набора данных.</li>
  <li><strong>Моделирование и прогноз</strong><br>
      Выберем один столбец как целевую переменную, остальные — как признаки, обучим модель (например, линейную регрессию, дерево решений или MLP) и получим прогноз для новых данных, введённых пользователем.</li>
</ol>

<h3>Личный вклад участников</h3>
<div class="team-members" style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
  <div style="flex: 0 1 220px; background: #f9f9f9; border-radius: 12px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;">
    <img src="/static/images/team/bezrukih.png" alt="Безруких Алексей Петрович" 
         style="width:100px; height:100px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
    <div>
      <strong>Безруких Алексей Петрович</strong><br>
      разработка генератора данных, реализация проверки нормальности распределения и расчёта статистических характеристик.
    </div>
  </div>
  <div style="flex: 0 1 220px; background: #f9f9f9; border-radius: 12px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;">
    <img src="/static/images/team/katavan.png" alt="Катаван Максим Андреевич" 
         style="width:100px; height:100px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
    <div>
      <strong>Катаван Максим Андреевич</strong><br>
      исследование корреляций, построение тепловых карт и аналитические выводы.
    </div>
  </div>
  <div style="flex: 0 1 220px; background: #f9f9f9; border-radius: 12px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;">
    <img src="/static/images/team/saprykin.png" alt="Сапрыкин Семён Максимович" 
         style="width:100px; height:100px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
    <div>
      <strong>Сапрыкин Семён Максимович</strong><br>
      визуализация данных (гистограммы, box‑plot, scatter matrix).
    </div>
  </div>
  <div style="flex: 0 1 220px; background: #f9f9f9; border-radius: 12px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center;">
    <img src="/static/images/team/volodin.png" alt="Володин Андрей Алексеевич" 
         style="width:100px; height:100px; object-fit:cover; border-radius:8px; margin-bottom:10px;">
    <div>
      <strong>Володин Андрей Алексеевич</strong><br>
      интеграция моделей машинного обучения.
    </div>
  </div>
</div>

