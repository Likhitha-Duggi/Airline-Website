import sqlite3
from flask import Flask, request
from flask import render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        pass
    return render_template('search.html')

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/tnc")
def tnc():
    return render_template("tnc.html")

@app.route("/tq")
def tq():
    return render_template("tq.html")

@app.route('/addflight', methods=['GET', 'POST'])
def addflight():
    if request.method == 'POST':
        pass
    return render_template('addflight.html')

@app.route('/thankyou', methods=['GET', 'POST'])
def thankyou():
        return render_template('thankyou.html')



#Creating database to store registration data
#Creating signup table
@app.route("/db")
def test_db():
    conn = sqlite3.connect('database.db')   
    print('Opened database successfully', flush=True)
    conn.execute('DROP TABLE IF EXISTS signup')
    conn.commit()
    conn.execute('CREATE TABLE signup (firstname TEXT,email TEXT,dob DATE,gender TEXT,contactNumber Number,password PASSWORD)')
    print('Table created successfully', flush=True)
    conn.close()
    return "Table created successfully"

#Inserting data in the signup table
@app.route('/addrec', methods = ['POST','GET'])
def addrec():
    if request.method == 'POST':
        try:
            firstname = request.form['firstName']
            email = request.form['email']
            dob = request.form['dob']
            gender = request.form['gender']
            contactNumber = request.form['contactNumber']
            password = request.form['password']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor() 
                cur.execute("INSERT INTO signup (firstname,email,dob,gender,contactNumber,password) VALUES (?,?,?,?,?,?)", (firstname,email,dob,gender,contactNumber,password))
                con.commit()
                msg="Registration successful. You can proceed by logging in."

        except:
                con.rollback()
                msg = "error in insert operation"
        finally:
                con.close()
                return render_template("signup.html", msg=msg)
        
#Displaying registration data present in signup table       
@app.route('/list')
def list():
    con=sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from signup")

    rows = cur.fetchall();
    return render_template("list.html",rows=rows)

#LOGIN VALIDATION
#To check for correct username and password
@app.route('/login1', methods=['POST'])
def login1():
    username = request.form['username']
    password = request.form['psw']

    with sqlite3.connect("database.db") as con:
        cur = con.cursor()

            #checking if username and password match to the email and password in signup table

        cur.execute("SELECT * FROM signup WHERE email = ? AND password = ?", (username, password))
        row = cur.fetchone()
        if row is not None:
            return render_template("search.html")
        else:
            error = "Incorrect username or password"
            return render_template("signup.html",error=error,username=username)   


# Set up the database
# @app.route('/createflight')
# def createflight():
#   conn = sqlite3.connect('database.db')
#   c = conn.cursor()
#   conn.execute('DROP TABLE IF EXISTS flights')
#   conn.commit()
#   c.execute('''CREATE TABLE IF NOT EXISTS flights
#              (
#               departure TEXT,
#               arrival TEXT,
#               fcode TEXT,
#               time TEXT,
#               duration TEXT,
#               price REAL)''')

#   conn.commit()

#TO STORE FLIGHT DATA
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Retrieve the data from the form
        departure = request.form.get['departure','']
        arrival = request.form.get['arrival','']
        fcode = request.form.get['fcode','']
        time = request.form.get['time','']
        duration = request.form.get['duration','']
        price = request.form.get['price','']

        print("Retrieved data isssss:")
        print("Departure:", departure)
        print("Arrival:", arrival)
        print("Fcode:", fcode)
        print("Time:", time)
        print("Duration:", duration)
        print("Price:", price)
        return render_template('thankyou.html')
    
    else:
        # Retrieve the data from the URL parameters
        departure = request.args.get('departure')
        arrival = request.args.get('arrival')
        fcode = request.args.get('fcode')
        time = request.args.get('time')
        duration = request.args.get('duration')
        price = request.args.get('price')
        print("Retrieved data mmm:")
        print("Departure:", departure)
        print("Arrival:", arrival)
        print("Fcode:", fcode)
        print("Time:", time)
        print("Duration:", duration)
        print("Price:", price)
        # Insert the data into the database
        conn = sqlite3.connect('database.db') 
        c = conn.cursor()
        c.execute("INSERT INTO flights (departure, arrival, fcode, time, duration, price) VALUES (?, ?, ?, ?, ?, ?)", (departure, arrival, fcode, time, duration, price))
        conn.commit()
        conn.close()

        return render_template('checkout.html')
    

#Creating a table to store payment card information
@app.route("/dbase")
def testing_db():
    conn = sqlite3.connect('database.db')   
    print('Opened database successfully', flush=True)
    conn.execute('DROP TABLE IF EXISTS payments')
    conn.commit()
    conn.execute('CREATE TABLE payments (cardNumber NUMBER,mail TEXT,expiryDate DATE,cvv NUMBER,nameOnCard TEXT)')
    print('Table created successfully', flush=True)
    
    conn.close()

    return "Table created successfully"

#inserting user payment info input into table
@app.route('/addcheck', methods = ['POST','GET'])
def addcheck():
    if request.method == 'POST':
        try:
            cardNumber = request.form['card-number']
            mail = request.form['mail']
            expiryDate = request.form['expiry-date']
            cvv = request.form['cvv']
            nameOnCard = request.form['name-on-card']
        
            with sqlite3.connect("database.db") as con:
                cur = con.cursor() 
                cur.execute("INSERT INTO payments (cardNumber,mail,expiryDate,cvv,nameOnCard) VALUES (?,?,?,?,?)", (cardNumber,mail,expiryDate,cvv,nameOnCard))

                con.commit()
                msg="Record successfully added"

        except:
                con.rollback()
                msg = "error in insert operation"
        finally:
                con.close()
                return render_template("thankyou.html",msg=msg)

#fetch rows in payment table        
@app.route('/check')
def check():
    con=sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from payments")

    rows = cur.fetchall();
    return render_template("check.html",rows=rows)







