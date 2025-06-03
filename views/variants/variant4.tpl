% rebase('variants/layout_variants.tpl', title='Вариант 4 - Предсказание числа', year=year)

<script src="/static/scripts/local/variant4.js"></script>
<h2>Предсказание целевой переменной</h2>
<p class="mb-3">
    Выберите целевой столбец и введите значения признаков для предсказания:
</p>
<form action="/make_prediction" target="predictFrame" method="post" class="mb-3">
    <div class="form-group">
        <label for="target_col">Номер целевого столбца:</label>
        <input type="number" class="form-control" id="target_col" name="target_col" style="width: 80px;" required>
    </div>
    <div class="form-group">
        <label for="features">Значения признаков (через пробел):</label>
        <input type="text" class="form-control" id="features" name="features" placeholder="Например: 1.2 3.4 5.6" required>
    </div>
    <button type="submit" style="margin-top: 30px;" class="btn btn-success">Сделать предсказание</button>
</form>
<iframe id="predictFrame" name="predictFrame" style="width: 100%; height: 280px" title="Результат предсказания"></iframe>
<form action="/save_prediction" target="predictFrame" method="post" class="mb-3" id="saveForm">
    <input type="hidden" name="target_col" id="save_target_col">
    <input type="hidden" name="features" id="save_features">
    <button type="submit" style="margin-top: 30px;" class="btn btn-success">
        <i class="fas fa-save"></i> Сохранить результаты
    </button>
</form>
