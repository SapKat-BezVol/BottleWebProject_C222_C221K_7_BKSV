<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ title }} - Элементы машинного обучения и анализа данных</title>
        <link rel="stylesheet" href="/static/content/bootstrap.min.css" />
        <link rel="stylesheet" href="/static/content/site.css" />
        <link rel="icon" type="image/png" href="/static/images/favicon.png">
        <script src="/static/scripts/bootstrap.bundle.min.js"></script>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
            <div class="container">
                <a href="/" class="navbar-brand">Элементы машинного обучения и анализа данных</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarMain" aria-controls="navbarMain" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarMain">
                    <ul class="navbar-nav">
                        <li class="nav-item"><a class="nav-link" href="/about">О команде</a></li>
                    </ul>
                </div>
            </div>
        </nav>
        <div class="container body-content" style="padding-top: 10px;">
            {{!base}}
            <hr />
            <footer>
                <p>&copy; {{ year }} - SapKat&BezVol ©</p>
            </footer>
        </div>
    </body>
</html>
