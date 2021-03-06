import os
from flask import Flask
from companystore import (
    company,
    db,
    product,
    purchase,
)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'companystore.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(company.blueprint)
    app.register_blueprint(product.blueprint)
    app.register_blueprint(purchase.blueprint)
    db.init_app(app)
    return app
