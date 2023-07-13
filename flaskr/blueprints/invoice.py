from flask import Blueprint

from flask import abort, jsonify, make_response, request

from flaskr.db import get_db
from flaskr.invoice_state_machine import InvoiceMachine
from flaskr.utilities import query_to_json_response

invoice = Blueprint('invoice', __name__, url_prefix='/api/v1/invoices')

def abort_with_message(err_msg, http_code):
    abort(make_response(jsonify(message=err_msg), http_code))

@invoice.put('/<int:invoice_id>')
def update_invoice(invoice_id):
    db = get_db()
    error = None

    invoice = db.execute(
        'SELECT * FROM invoice WHERE id = ?', (invoice_id,)
    ).fetchone()

    if invoice is None:
        abort_with_message("Invoice id {invoice_id} doesn't exist.", 404)

    data = request.get_json()
    new_state = data.get('invoice').get('status')

    if not new_state:
        abort_with_message("Invoice state is required.", 400)

    sm = InvoiceMachine(start_value = invoice['state'])

    try:
        sm.send(InvoiceMachine.STATE_ACTION_MAPPING[new_state])
    except:
        abort_with_message("Invalid transition from {invoice['state']} to {new_state} for invoice status.", 400)

    db.execute(
        'UPDATE invoice SET state = ?'
        ' WHERE id = ?',
        (new_state, invoice_id)
    )
    db.commit()
    updated_row = dict(invoice)
    updated_row['state'] = new_state

    return jsonify(updated_row)
