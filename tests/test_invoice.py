import json
import pytest

from flask import url_for
from flaskr.db import get_db
from flaskr import create_app


def test_put_invoice(app, client):
    with app.app_context(), app.test_request_context():
        tested_id = 1
        new_status = 'approved'
        data = { 'invoice': { 'status': new_status }}
        headers = {'Content-Type': 'application/json'}

        response = client.put(url_for('invoice.update_invoice', invoice_id=tested_id), data=json.dumps(data), headers=headers)

        updated = get_db().execute(
            'SELECT * FROM invoice WHERE id = ?', (tested_id,)
        ).fetchone()

        assert response.status_code == 200
        assert updated['state'] == new_status
