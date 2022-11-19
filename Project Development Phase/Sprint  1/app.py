from flask import Flask, render_template, url_for, request, redirect
import ibm_db

app = Flask(__name__)

dsn_hostname = 'b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud'
dsn_uid = 'ylv02200'
dsn_pwd = 'i9f3rgG6ItqgfHNX'

dsn_driver = '{IBM DB2 ODBC DRIVER}'
dsn_database = 'BLUDB'
dsn_port = '32716'
dsn_protocol = 'TCPIP'

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL=<41:"
    "UID={5};"
    "PWD={6};"
).format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)

print(dsn)
conn = ''

try:
    conn = ibm_db.connect("DATABASE=bludb;QUERYTIMEOUT=1;CONNECTTIMEOUT=10;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=./DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=ylv02200;PWD=i9f3rgG6ItqgfHNX", "", "")
    print('Connected to DB', dsn_database)
except:
    print('Unable to connect')

class Product:
    def __init__(self, id: int, name: str, price: float, qty: int):
        self.id = id
        self.name = name
        self.price = price
        self.qty = qty
        

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        qty = request.form['qty']

        try:
            insert_query = "INSERT INTO PRODUCTS(Name, Price, QTY) VALUES('"+name+"', "+price+", "+qty+")"
            print(insert_query)
            insert_table = ibm_db.exec_immediate(conn, insert_query)

            return redirect('/')
        except:
            return 'There was a problem adding that Product. Perhaps try again?'

    else:
        products = []
        stmt = ibm_db.exec_immediate(conn, 'SELECT * FROM PRODUCTS')
        print(stmt)
        while ibm_db.fetch_row(stmt) != False:
            products.append(Product(id=ibm_db.result(stmt, 0), name=ibm_db.result(stmt, 1), price=ibm_db.result(stmt, 2), qty=ibm_db.result(stmt, 3)))
        return render_template('index.html', products=products)



@app.route('/delete/<int:id>')
def delete(id):
   

    product = {}

    try:

        delete_query = "DELETE FROM PRODUCTS WHERE ID = " + str(id)
        stmt = ibm_db.exec_immediate(conn, delete_query)

        return redirect('/')
    except:
        return 'There was a problem deleting that Product!'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    product = {}

    select_query = "SELECT * FROM PRODUCTS WHERE ID = " + str(id)
    stmt = ibm_db.exec_immediate(conn, select_query)
    while ibm_db.fetch_row(stmt) != False:
        product = Product(id=ibm_db.result(stmt, 0), name=ibm_db.result(stmt, 1), price=ibm_db.result(stmt, 2), qty=ibm_db.result(stmt, 3))


    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']
        qty = request.form['qty']

        try:
            print('Im here!')

            update_query = "UPDATE PRODUCTS SET Name = '"+name+"', Price = "+price+", QTY = "+qty+" WHERE ID = "+ str(id)
            stmt = ibm_db.exec_immediate(conn, update_query)

            return redirect('/')
        except:
            return 'There was a problem updating that Product. Perhaps try again?'

    else:
        products = []
        select_query = "SELECT * FROM PRODUCTS"
        stmt = ibm_db.exec_immediate(conn, select_query)
        while ibm_db.fetch_row(stmt) != False:
            products.append(Product(id=ibm_db.result(stmt, 0), name=ibm_db.result(stmt, 1), price=ibm_db.result(stmt, 2), qty=ibm_db.result(stmt, 3)))
        return render_template('modal.html', products=products, product=product)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)