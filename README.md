companystore
============
A backend web application for keeping track of companies, products and orders

Installation
------------
1. Create a virtual environment
2. Install with pip `pip install .`
3. Run with flask `FLASK_APP=companystore flask run`

Testing
-------
Tests are run with pytest, install [test] for test requirements `pip install .[test]`

Usage
-----
Available endpoints:  
/company/list, GET  
List all companies

/company/create, POST  
Create a company. Parameters:  
name, vatnumber, organizationnumber

/product/list, POST  
List all products for a company. Parameters:  
company

/product/create, POST  
Create a product. Parameters:  
name, company

/purchase/list, POST  
List all purchases for a company. Parameters:  
company

/purchase/create, POST
Create a purchase. Parameters:  
company, products: [id, amount]
