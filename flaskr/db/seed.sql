INSERT INTO borrower (id, name)
VALUES
    (1, 'John Smith'),
    (2, 'Jane Jones'),
    (3, 'United Roofing, Inc.'),
    (4, 'Mart Mart LLC');

INSERT INTO invoice (borrower_id, amount, due_date, invoice_number, state)
VALUES
    (1, 99.90, CURRENT_TIMESTAMP, 'JS-1000', 'created'),
    (1, 299.00, CURRENT_TIMESTAMP, 'JS-1001', 'closed'),
    (2, 80.99, CURRENT_TIMESTAMP, 'JJ-2032', 'purchased'),
    (2, 90.00, CURRENT_TIMESTAMP, 'JJ-2033', 'created'),
    (2, 120.99, CURRENT_TIMESTAMP, 'JJ-2034', 'approved'),
    (2, 33.87, CURRENT_TIMESTAMP, 'JJ-2035', 'rejected'),
    (3, 100.00, CURRENT_TIMESTAMP, 'URI-8000', 'rejected');
