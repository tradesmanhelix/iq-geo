from statemachine import StateMachine, State

class InvoiceMachine(StateMachine):
    # States
    created = State(initial=True)
    approved = State()
    purchased = State()
    closed = State(final=True)
    rejected = State(final=True)

    # Transitions
    reject = created.to(rejected)

    approve = created.to(approved)
    purchase = approved.to(purchased)
    close = purchased.to(closed)

    STATE_ACTION_MAPPING = {
        "approved": "approve",
        "rejected": "reject",
        "purchased": "purchase",
        "closed": "close"
    }
