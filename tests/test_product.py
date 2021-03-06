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
    client.post('/company/create', json={"name": "MyOtherCompany", "organizationnumber": 2})
    client.post('/product/create', json={"name": "GameCube", "company": 2})
    yield client

    os.close(database)
    os.unlink(app.config['DATABASE'])


def test_product(client):
    # Eric wants to create a product in his company
    # He tries to list his products, but doesn't supply a company and gets an error
    result = client.post('/product/list')
    assert b'you need to specify a company' in result.data
    assert result.status_code == 400

    # He adds a company and can see that he has no products
    result = json.loads(client.post('/product/list', json={"company": 1}).data)
    assert result == []

    # He makes a request, but forgets to submit a name
    result = client.post('/product/create', json={"company": 1})
    assert b'you need to specify a name' in result.data
    assert result.status_code == 400

    # He makes a new request but forgets the company this time
    result = client.post('/product/create', json={"name": "NUC8I7HVK2"})
    assert b'you need to specify a company' in result.data
    assert result.status_code == 400

    # He makes a new request and remembers to set the name
    result = client.post('/product/create', json={"company": 1, "name": "NUC8I7HVK2"})
    assert b'product "NUC8I7HVK2" created' in result.data

    # He can see it in the list
    result = json.loads(client.post('/product/list', json={"company": 1}).data)
    assert result == [{'name': 'NUC8I7HVK2', 'id': 2}]
