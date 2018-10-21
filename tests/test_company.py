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

    yield app.test_client()

    os.close(database)
    os.unlink(app.config['DATABASE'])


def test_company(client):
    # Eric wants to keep track of his companies
    # He lists the current companies and sees that none exist
    result = json.loads(client.get('/company/list').data)
    assert result == []

    # He makes a request, but isn't sure what to add, so he sends no data
    result = client.post('/company/create', json={})
    assert b'you need to specify a name' in result.data
    assert result.status_code == 400

    # He creates a company but only submits a name
    result = client.post('/company/create', json={"name": "MyCompany"})
    assert b'you need to specify either an organization number or a VAT number' in result.data
    assert result.status_code == 400

    # He adds an organization number
    result = client.post('/company/create', json={"name": "MyCompany", "organizationnumber": 1})
    assert b'company "MyCompany" created' in result.data

    # He can now see his company in the company list
    result = json.loads(client.get('/company/list').data)
    assert result == [{'name': 'MyCompany', 'organizationnumber': '1', 'vatnumber': None}]
