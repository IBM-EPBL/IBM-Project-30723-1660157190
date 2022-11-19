from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        qty = request.form['qty']
        new_product = Product(name=name, price=price, qty=qty)

        try:
            db.session.add(new_product)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem adding that Product. Perhaps try again?'

    else:
        # Fetching all products
        products = Product.query.order_by(Product.name).all()
        print(products)
        return render_template('index.html', products=products)

# @app.route('/modal', methods=['POST', 'GET'])
# def modal():
        
#         return render_template('modal.html', products=products)

@app.route('/delete/<int:id>')
def delete(id):
    product = Product.query.get_or_404(id)

    try:
        db.session.delete(product)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that Product!'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.qty = request.form['qty']

        try:
            # db.session.add(new_product)
            print('Im here!')
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that Product. Perhaps try again?'

    else:
        products = Product.query.order_by(Product.name).all()
        return render_template('modal.html', products=products, product=product)

if __name__ == "__main__":
    app.run(debug=True)