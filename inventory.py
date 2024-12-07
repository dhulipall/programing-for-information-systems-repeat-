from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Product

inventory = Blueprint('inventory', __name__)

@inventory.route('/inventory')
def inventory_list():
    """Inventory page displaying all products."""
    products = Product.query.all()
    return render_template('inventory.html', products=products)

@inventory.route('/add', methods=['GET', 'POST'])
def add_product():
    """Page to add a new product."""
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        expiry_date = request.form['expiry_date']

        new_product = Product(name=name, category=category, quantity=quantity, price=price, expiry_date=expiry_date)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('inventory.inventory_list'))
    return render_template('add_product.html')

@inventory.route('/update/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    """Page to update a product's details."""
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.quantity = int(request.form['quantity'])
        product.price = float(request.form['price'])
        product.expiry_date = request.form['expiry_date']

        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('inventory.inventory_list'))
    return render_template('update_product.html', product=product)

@inventory.route('/delete/<int:id>')
def delete_product(id):
    """Route to delete a product."""
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for('inventory.inventory_list'))
