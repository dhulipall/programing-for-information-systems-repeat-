from flask import Blueprint, render_template
from models import db, Product

reports = Blueprint('reports', __name__)

@reports.route('/reports')
def reports_list():
    """Page to display reports, such as low stock products."""
    low_stock = Product.query.filter(Product.quantity < 5).all()
    return render_template('reports.html', low_stock=low_stock)
