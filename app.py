from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from xhtml2pdf import pisa
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to set a strong secret key for production

# Setup the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            name = request.form['name']
            category = request.form['category']
            quantity = int(request.form['quantity'])
            price = float(request.form['price'])
            expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d')

            new_product = Product(name=name, category=category, quantity=quantity, price=price, expiry_date=expiry_date)
            db.session.add(new_product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('view_products'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return render_template('add_product.html')
    
    return render_template('add_product.html')

@app.route('/view_products')
def view_products():
    products = Product.query.all()
    return render_template('view_products.html', products=products)

@app.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        try:
            product.name = request.form['name']
            product.category = request.form['category']
            product.quantity = int(request.form['quantity'])
            product.price = float(request.form['price'])
            product.expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d')

            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('view_products'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return render_template('update_product.html', product=product)
    
    return render_template('update_product.html', product=product)

@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'danger')
    except Exception as e:
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('view_products'))

@app.route('/report')
def report():
    low_stock = Product.query.filter(Product.quantity < 5).all()
    return render_template('report.html', low_stock=low_stock)

@app.route('/low_stock', methods=['GET'])
def low_stock():
    """Return low-stock products in JSON format."""
    products = Product.query.filter(Product.quantity < 5).all()
    result = [
        {
            "name": product.name,
            "category": product.category,
            "quantity": product.quantity,
            "price": product.price,
            "expiry_date": product.expiry_date.strftime('%Y-%m-%d'),
        }
        for product in products
    ]
    return jsonify(result)

@app.route('/low_stock_pdf', methods=['GET'])
def low_stock_pdf():
    """Generate a PDF report of low-stock products."""
    products = Product.query.filter(Product.quantity < 5).all()
    rendered_html = render_template('report_pdf.html', low_stock=products)

    # Create a BytesIO stream to store the PDF
    pdf = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(rendered_html.encode('utf-8')), dest=pdf)

    if pisa_status.err:
        return "Error generating PDF", 500
    pdf.seek(0)
    return make_response(pdf.read(), {
        'Content-Disposition': 'attachment; filename=low_stock_report.pdf',
        'Content-Type': 'application/pdf',
    })

if __name__ == '__main__':
    app.run(debug=True)
