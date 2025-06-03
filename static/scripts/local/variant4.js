document.getElementById("saveForm").addEventListener("submit", function (e) {
    // Копируем значения из основной формы
    document.getElementById("save_target_col").value = document.getElementById("target_col").value;
    document.getElementById("save_features").value = document.getElementById("features").value;
});