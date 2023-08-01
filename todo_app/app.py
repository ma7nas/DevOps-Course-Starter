from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.session_items import get_items, add_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_items())

@app.route('/', methods=(['POST']))
def addItem():
    title = request.form.get('title')
    add_item(title)
    return redirect(url_for('index'))
