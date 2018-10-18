DROP TABLE IF EXISTS company;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS purchase;
DROP TABLE IF EXISTS purchase_product;

CREATE TABLE company (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  organizationnumber TEXT UNIQUE,
  vatnumber TEXT UNIQUE,
  CHECK (organizationnumber IS NOT NULL or vatnumber IS NOT NULL)
);

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  company_id INTEGER NOT NULL,
  FOREIGN KEY (company_id) REFERENCES company (id),
  UNIQUE (name, company_id)
);

CREATE TABLE purchase (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_id INTEGER NOT NULL,
  FOREIGN KEY (company_id) REFERENCES company (id)
);

CREATE TABLE purchase_product (
  purchase_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  amount INTEGER NOT NULL,
  PRIMARY KEY (purchase_id, product_id),
  FOREIGN KEY (purchase_id) REFERENCES purchase (id),
  FOREIGN KEY (product_id) REFERENCES product (id)
);
