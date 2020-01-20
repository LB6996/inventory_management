import peeweedbevolve
from flask import Flask, flash, redirect, url_for, render_template, request
from models import db, Store, Warehouse


app = Flask(__name__)
app.secret_key = 'super secret key'


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/store")
def store():
    return render_template('store.html')


@app.route("/store_form", methods=["POST"])
def create_store():
    s = Store(name=request.form.get('name'))

    if s.save():
        flash("successfully saved")
        # return render_template('store.html', name=request.args['name'])
        return redirect(url_for('store'))
    else:
        return render_template('store.html', name=request.form.get('name'))

@app.route("/warehouse")
def warehouse():
    store_list = Store.select()
    return render_template('warehouse.html', store_list=store_list)

@app.route("/warehouse_form", methods=["POST"])
def create_warehouse():
    w_location = request.form.get('w_location')
    s_id = Store.get_by_id(request.form.get('s_id'))
    w = Warehouse(location=w_location, store_id=s_id)

    if w.save():
        flash("successfully saved")
        return redirect(url_for('warehouse'))
    else:
        return render_template('warehouse.html')


if __name__ == '__main__':
    app.run()