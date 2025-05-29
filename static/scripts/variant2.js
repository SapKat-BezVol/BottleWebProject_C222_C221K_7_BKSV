document.addEventListener("DOMContentLoaded", function () {
    const rowsInput = document.getElementById("rows");
    const colsInput = document.getElementById("cols");

    if (rowsInput && colsInput) {
        function syncValues(e) {
            colsInput.value = e.target.value;
        }

        rowsInput.addEventListener("input", syncValues);
        colsInput.addEventListener("input", function (e) {
            rowsInput.value = e.target.value;
        });
    }
});

