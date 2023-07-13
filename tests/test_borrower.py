import pytest

from flask import url_for
from flaskr import create_app
from flaskr.db import get_db


def test_borrowers_index(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('borrower.borrowers'))
        assert b"John Smith" in response.data
        assert b"Mart Mart LLC" in response.data

def test_invoices_index(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('borrower.borrower_invoices', borrower_id=1))
        assert b"JS-1000" in response.data
        assert b"JS-1001" in response.data

def test_blank_invoices_index(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for('borrower.borrower_invoices', borrower_id=4))
        assert b"[]" in response.data
