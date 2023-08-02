from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.session_items import get_items, add_item, get_item, save_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=get_items())

@app.route('/', methods=(['POST']))
def update():
    done_items = request.form.getlist('done')
    print(done_items)
    if len(done_items) == 0:
        title = request.form.get('title')
        add_item(title)
        return redirect(url_for('index'))
    else:
        print(done_items)
        for item in done_items[0:-1]:
            updated_item = get_item(item)
            updated_item.update({"status": "Done"})
            save_item(updated_item)
            print(updated_item)
        return redirect(url_for('index'))
    
