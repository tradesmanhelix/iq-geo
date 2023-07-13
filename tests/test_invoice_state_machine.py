import pytest

from flaskr.invoice_state_machine import InvoiceMachine
from statemachine.exceptions import TransitionNotAllowed

def test_valid_transition():
    sm = InvoiceMachine()
    sm.approve()

    assert sm.current_state_value == 'approved'

def test_multiple_transitions():
    sm = InvoiceMachine()
    sm.approve()
    sm.purchase()

    assert sm.current_state_value == 'purchased'

def test_invalid_transition():
    sm = InvoiceMachine()

    with pytest.raises(TransitionNotAllowed):
        sm.send('closed')
