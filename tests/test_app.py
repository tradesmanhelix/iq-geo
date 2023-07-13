import json
import pytest

from flask import url_for
from flaskr.db import get_db
from flaskr import create_app


def test_borrowers_index(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('borrowers'))
        assert b"John Smith" in response.data
        assert b"Mart Mart LLC" in response.data

def test_invoices_index(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('borrower_invoices', borrower_id=1))
        assert b"JS-1000" in response.data
        assert b"JS-1001" in response.data

def test_blank_invoices_index(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('borrower_invoices', borrower_id=4))
        assert b"[]" in response.data

def test_put_invoice(app, client):
    with app.app_context(), app.test_request_context():
        tested_id = 1
        new_status = 'approved'
        data = { 'status': new_status }
        headers = {'Content-Type': 'application/json'}

        response = client.put(url_for('update_invoice', invoice_id=tested_id), data=json.dumps(data), headers=headers)

        updated = get_db().execute(
            'SELECT * FROM invoice WHERE id = ?', (tested_id,)
        ).fetchone()

        assert response.status_code == 200
        assert updated['state'] == new_status
