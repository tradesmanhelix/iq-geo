import os
import json

from flask import Flask, jsonify
from flaskr.db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def query_to_json_response(db_result):
        response = jsonify([dict(row) for row in db_result])
        response.headers['Content-Type'] = 'application/json'
        return response

    @app.get('/borrowers')
    def borrowers():
        db = get_db()
        borrowers = db.execute('SELECT * FROM borrower').fetchall()
        return query_to_json_response(borrowers)

    @app.get('/borrowers/<int:borrower_id>/invoices')
    def borrower_invoices(borrower_id):
        db = get_db()
        invoices = db.execute(
            'SELECT * FROM invoice WHERE borrower_id = ?', (borrower_id,)
        ).fetchall()
        return query_to_json_response(invoices)

    @app.put('/borrowers/<int:borrower_id>/invoice/<int:invoice_id>')
    def update_invoice(borrower_id):
        return 'Put invoice'

    from . import db
    db.init_app(app)

    return app
