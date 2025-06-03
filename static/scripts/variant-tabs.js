document.addEventListener('DOMContentLoaded', function () {
    const tabButtons = document.querySelectorAll('#variantTabs button[data-bs-toggle="tab"]');
    tabButtons.forEach((btn) => {
        btn.addEventListener('click', function (event) {
            event.preventDefault();
            const tab = new bootstrap.Tab(btn);
            tab.show();
        });
    });
});
