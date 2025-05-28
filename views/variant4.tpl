% rebase('layoutvariant.tpl', title='Предсказание числа', year=year)

<h2>Предсказание целевой переменной</h2>
<p class="mb-3">Введите значения признаков для предсказания:</p>

<form action="/predict" target="predictFrame" method="post" class="mb-3">
  <div class="form-group">
    % for i in range(num_features):
      <label for="feature_{{i}}">Признак {{i+1}}:</label>
      <input type="number" step="any" class="form-control mb-2" id="feature_{{i}}" name="feature_{{i}}" required>
    % end
  </div>
  <button type="submit" class="btn btn-primary">Сделать предсказание</button>
</form>

<iframe id="predictFrame" name="predictFrame" class="table-frame w-100 border" style="min-height:200px" title="Результат предсказания"></iframe>