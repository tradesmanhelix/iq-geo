from flask import Blueprint

from flaskr.db import get_db
from flaskr.utilities import query_to_json_response

borrower = Blueprint('borrower', __name__, url_prefix='/api/v1/borrowers')

@borrower.get('/')
def borrowers():
    db = get_db()
    borrowers = db.execute('SELECT * FROM borrower').fetchall()
    return query_to_json_response(borrowers)

@borrower.get('/<int:borrower_id>/invoices')
def borrower_invoices(borrower_id):
    db = get_db()
    invoices = db.execute(
        'SELECT * FROM invoice WHERE borrower_id = ?', (borrower_id,)
    ).fetchall()
    return query_to_json_response(invoices)
