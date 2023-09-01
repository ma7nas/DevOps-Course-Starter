from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.trello_items import get_cards, add_card, update_as_done, delete_card

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_cards()
    return render_template('index.html', cards=items)

@app.route('/add', methods=['GET', 'POST'])
def add():
    title = request.form.get('title')
    add_card(title)
    return redirect(url_for('index'))

@app.route('/done', methods=['GET', 'POST'])
def done():
    done_card_ids = request.form.getlist('action')
    for card_id in done_card_ids:
        update_as_done(card_id)
    return redirect(url_for('index'))

@app.route('/delete', methods=(['POST']))
def delete():
    delete_card_ids = request.form.getlist('action')
    for card_id in delete_card_ids:
        delete_card(card_id)
    return redirect(url_for('index'))
