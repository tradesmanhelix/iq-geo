import os
import json

from flask import Flask, abort, jsonify, make_response, request

from flaskr.db import get_db

from flaskr.blueprints.borrower import borrower


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(borrower)

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

    @app.put('/api/v1/invoices/<int:invoice_id>')
    def update_invoice(invoice_id):
        db = get_db()
        error = None

        invoice = db.execute(
            'SELECT * FROM invoice WHERE id = ?', (invoice_id,)
        ).fetchone()

        if invoice is None:
            abort(make_response(jsonify(message="Invoice id {invoice_id} doesn't exist."), 404))

        data = request.get_json()
        state = data.get('invoice').get('status')

        if not state:
            abort(make_response(jsonify(message="Invoice state is required."), 400))

        db.execute(
            'UPDATE invoice SET state = ?'
            ' WHERE id = ?',
            (state, invoice_id)
        )
        db.commit()
        updated_row = dict(invoice)
        updated_row['state'] = state

        return jsonify(updated_row)

    from . import db
    db.init_app(app)

    return app
