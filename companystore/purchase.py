from flask import (
    Blueprint,
    jsonify,
    request,
)
from companystore.db import get_db

blueprint = Blueprint('purchase', __name__, url_prefix='/purchase')


@blueprint.route('/list')
def list_purchase():
    content = request.json
    if content is None:
        return 'you need to specify a company', 400
    company_id = content.get('company')
    if company_id is None:
        return 'you need to specify a company', 400

    db = get_db()
    purchases = db.execute(
        'SELECT *'
        ' FROM purchase'
        ' WHERE company_id = ?',
        str(company_id),
    ).fetchall()
    purchase_ids = []
    for row in purchases:
        purchase_ids.append(dict(row).get('id'))

    data = []
    for purchase_id in purchase_ids:
        purchase = []
        purchases = db.execute(
            'SELECT product.name, purchase_product.amount'
            ' FROM purchase_product'
            ' JOIN purchase ON purchase.id = purchase_product.purchase_id'
            ' JOIN product ON product.id = purchase_product.product_id'
            ' WHERE purchase_product.purchase_id = ?',
            str(purchase_id),
        ).fetchall()
        for row in purchases:
            purchase.append(dict(row))
        data.append(purchase)
    return jsonify(data)


@blueprint.route('/create', methods=['POST'])
def create_product():
    content = request.json
    company_id = content.get('company')
    if company_id is None:
        return 'you need to specify a company', 400
    products = content.get('products', [])
    if not products:
        return 'you need to specify at least one product', 400
    for product in products:
        if product.get('id') is None:
            return 'you need to specify the id of the product', 400
        if product.get('amount') is None:
            return 'you need to specify an amount', 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO purchase (company_id)'
        ' VALUES (?)',
        str(company_id)
    )
    db.commit()
    purchase_id = cursor.lastrowid
    cursor.close()

    for product in products:
        db.execute(
            'INSERT INTO purchase_product (purchase_id, product_id, amount)'
            ' VALUES (?, ?, ?)',
            (purchase_id, product.get('id'), product.get('amount'))
        )
    db.commit()

    return f'purchase created'
