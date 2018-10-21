import os
import tempfile
import pytest
import json
from companystore import create_app
from companystore.db import init_db


@pytest.fixture
def client():
    app = create_app()
    database, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.app_context():
        init_db()

    client = app.test_client()
    # Create a client for use in the tests
    client.post('/company/create', json={"name": "MyCompany", "organizationnumber": 1})
    client.post('/product/create', json={"name": "NUC8I7HVK2", "company": 1})
    client.post('/product/create', json={"name": "Dell U2415", "company": 1})
    yield client

    os.close(database)
    os.unlink(app.config['DATABASE'])


def test_purchase(client):
    # Eric wants to create a purchase order
    # He can see that he has no purchases
    result = json.loads(client.get('/purchase/list', json={"company": 1}).data)
    assert result == []

    # He makes a purchase, but forgets to submit a company
    result = client.post('/purchase/create', json={})
    assert b'you need to specify a company' in result.data
    assert result.status_code == 400

    # He makes a new request but forgets the product
    result = client.post('/purchase/create', json={"company": 1})
    assert b'you need to specify at least one product' in result.data
    assert result.status_code == 400

    # He makes a new request and remembers to set the product
    result = client.post('/purchase/create', json={"company": 1, "products": [{"id": 1}]})
    assert b'you need to specify an amount' in result.data
    assert result.status_code == 400

    # He makes a new request and sets the amount
    result = client.post('/purchase/create', json={"company": 1, "products": [{"id": 1, "amount": 1}]})
    assert b'purchase created' in result.data

    # He can see it in the list
    result = json.loads(client.get('/purchase/list', json={"company": 1}).data)
    assert result == [[{'name': 'NUC8I7HVK2', 'amount': 1}]]

    # He makes another purchase that has multiple products
    client.post(
        '/purchase/create',
        json={
            "company": 1,
            "products": [
                {
                    "id": 1,
                    "amount": 1,
                },
                {
                    "id": 2,
                    "amount": 3,
                },
            ]
        }
    )

    # He can see both purchase orders
    result = json.loads(client.get('/purchase/list', json={"company": 1}).data)
    print(result)
    assert result == [
        [{'name': 'NUC8I7HVK2', 'amount': 1}],
        [{'name': 'NUC8I7HVK2', 'amount': 1}, {'name': 'Dell U2415', 'amount': 3}]
    ]
