import sqlite3
from flask import (
    Blueprint,
    jsonify,
    request,
)
from companystore.db import get_db

blueprint = Blueprint('company', __name__, url_prefix='/company')


@blueprint.route('/list')
def list_companies():
    db = get_db()
    companies = db.execute(
        'SELECT name, organizationnumber, vatnumber'
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
