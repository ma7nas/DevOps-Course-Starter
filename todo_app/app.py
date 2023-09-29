from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.trello_items import get_items, add_item, update_as_done, delete_item
from todo_app.data.view_model import ViewModel

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    items = get_items()
    item_view_model = ViewModel(items)
    return render_template('index.html', view_model=item_view_model)

@app.route('/add', methods=['GET', 'POST'])
def add():
    title = request.form.get('title')
    add_item(title)
    return redirect(url_for('index'))

@app.route('/done', methods=['GET', 'POST'])
def done():
    done_items = request.form.getlist('action')
    for card_id in done_items:
        update_as_done(card_id)
    return redirect(url_for('index'))

@app.route('/delete', methods=(['POST']))
def delete():
    deleted_items = request.form.getlist('action')
    for card_id in deleted_items:
        delete_item(card_id)
    return redirect(url_for('index'))