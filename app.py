from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api/instance/shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

with app.app_context():
    db.create_all()


@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_list = [{
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "image": product.image,
        "description": product.description
    } for product in products]
    return jsonify(products_list)

@app.route('/admin')
def admin():
    products = Product.query.all()
    return render_template('admin.html', products=products)

@app.route('/admin/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']
        description = request.form['description']
        new_product = Product(name=name, price=price, image=image, description=description)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('add_product.html')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.image = request.form['image']
        product.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('edit_product.html', product=product)

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
