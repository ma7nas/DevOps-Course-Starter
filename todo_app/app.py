from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.session_items import delete_item
from todo_app.data.trello_items import get_cards, add_card, update_as_done

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    sorted_cards = sorted(get_cards(), key=lambda x: x['status'], reverse=True)
    return render_template('index.html', cards=sorted_cards)

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
    delete_items = request.form.getlist('action')
    for item in delete_items:
        delete_item(item)
    return redirect(url_for('index'))
