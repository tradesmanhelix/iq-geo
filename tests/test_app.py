import pytest
from flaskr.db import get_db


def test_borrowers_index(client):
    response = client.get('/borrowers')
    assert b"John Smith" in response.data
    assert b"Mart Mart LLC" in response.data

def test_invoices_index(client):
    response = client.get('/borrowers/1/invoices')
    assert b"JS-1000" in response.data
    assert b"JS-1001" in response.data

def test_blank_invoices_index(client):
    response = client.get('/borrowers/4/invoices')
    assert b"[]" in response.data
