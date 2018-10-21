import sqlite3
from flask import (
    Blueprint,
    jsonify,
    request,
)
from companystore.db import get_db

blueprint = Blueprint('product', __name__, url_prefix='/product')


@blueprint.route('/list', methods=['POST'])
def list_products():
    content = request.json
    if content is None:
        return 'you need to specify a company', 400
    company_id = content.get('company', None)
    if company_id is None:
        return 'you need to specify a company', 400

    db = get_db()
    products = db.execute(
        'SELECT name, id'
        ' FROM product'
        ' WHERE company_id = ?',
        str(company_id),
    ).fetchall()
    data = []
    for row in products:
        data.append(dict(row))
    return jsonify(data)


@blueprint.route('/create', methods=['POST'])
def create_product():
    content = request.json
    name = content.get('name')
    if name is None:
        return 'you need to specify a name', 400
    company_id = content.get('company')
    if company_id is None:
        return 'you need to specify a company', 400

    db = get_db()
    try:
        db.execute(
            'INSERT INTO product (name, company_id)'
            ' VALUES (?, ?)',
            (name, company_id)
        )
    except sqlite3.IntegrityError:
        return 'product already exists', 400
    db.commit()

    return f'product "{name}" created'
