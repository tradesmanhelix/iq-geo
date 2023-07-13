from flask import Blueprint

from flask import abort, jsonify, make_response, request

from flaskr.db import get_db
from flaskr.utilities import query_to_json_response

invoice = Blueprint('invoice', __name__, url_prefix='/api/v1/invoices')

@invoice.put('/<int:invoice_id>')
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
