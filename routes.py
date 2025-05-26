from bottle import route, view
from datetime import datetime

@route('/')
@route('/home')
@view('index')
def home():
    """Рендер домашней страницы."""
    return dict(
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Рендер страницы с информацией о команде."""
    return dict(
        message='Your application description page.',
        year=datetime.now().year
    )

@route('/variant1')
@view('variant1')
def about():
    """Рендер страницы для первого варианта."""
    return dict(
        year=datetime.now().year
    )

@route('/variant2')
@view('variant2')
def about():
    """Рендер страницы для второго варианта."""
    return dict(
        year=datetime.now().year
    )

@route('/variant3')
@view('variant3')
def about():
    """Рендер страницы для третьего варианта."""
    return dict(
        year=datetime.now().year
    )

@route('/variant4')
@view('variant4')
def about():
    """Рендер страницы для четвёртого варианта."""
    return dict(
        year=datetime.now().year
    )