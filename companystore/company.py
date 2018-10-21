import sqlite3
import requests
from flask import (
    Blueprint,
    jsonify,
    request,
    current_app,
)
from companystore.db import get_db

blueprint = Blueprint('company', __name__, url_prefix='/company')


class ValidationError(Exception):
    pass


@blueprint.route('/list')
def list_companies():
    db = get_db()
    companies = db.execute(
        'SELECT name, organizationnumber, vatnumber, id'
        ' FROM company'
    ).fetchall()
    data = []
    for row in companies:
        data.append(dict(row))
    return jsonify(data)


@blueprint.route('/create', methods=['POST'])
def create_company():
    content = request.json
    name = content.get('name')
    if name is None:
        return 'you need to specify a name', 400
    organizationnumber = content.get('organizationnumber')
    vatnumber = content.get('vatnumber')
    if organizationnumber is None and vatnumber is None:
        return 'you need to specify either an organization number or a VAT number', 400

    if vatnumber is not None:
        try:
            if not validate_vat(vatnumber):
                return 'you need to specify a valid VAT number', 400
        except ValidationError:
            return 'could not validate vat number', 500

    db = get_db()
    try:
        db.execute(
            'INSERT INTO company (name, organizationnumber, vatnumber)'
            ' VALUES (?, ?, ?)',
            (name, organizationnumber, vatnumber)
        )
    except sqlite3.IntegrityError:
        return 'company already exists', 400
    db.commit()

    return f'company "{name}" created'


def validate_vat(vatcode):
    response = requests.post(
        'https://api.cloudmersive.com/validate/vat/lookup',
        headers={"Apikey": current_app.config.get('VAT_API_KEY')},
        json={"VatCode": vatcode},
    )
    if response.status_code == 200:
        return response.json().get('IsValid')
    else:
        raise ValidationError(f'Could not validate vat number: {response.text}')
