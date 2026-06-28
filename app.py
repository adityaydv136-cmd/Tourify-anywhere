from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'tourismproject'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# DATABASE MODELS

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    hotel = db.Column(db.String(100))


# HOME PAGE

@app.route('/')
def home():
    return render_template('index.html')


# REGISTER

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User(name=name, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:
            session['user'] = user.name
            return redirect(url_for('destinations'))

        return "Invalid Credentials"

    return render_template('login.html')


# DESTINATIONS

@app.route('/destinations')
def destinations():
    return render_template('destinations.html')


# AGRA PAGE

@app.route('/agra')
def agra():
    return render_template('agra.html')


# GOA PAGE

@app.route('/goa')
def goa():
    return render_template('goa.html')


# SHIMLA PAGE

@app.route('/shimla')
def shimla():
    return render_template('shimla.html')


# MANALI PAGE

@app.route('/manali')
def manali():
    return render_template('manali.html')


# JAIPUR PAGE

@app.route('/jaipur')
def jaipur():
    return render_template('jaipur.html')


# KERALA PAGE

@app.route('/kerala')
def kerala():
    return render_template('kerala.html')


# KASHMIR PAGE

@app.route('/kashmir')
def kashmir():
    return render_template('kashmir.html')


# DELHI PAGE

@app.route('/delhi')
def delhi():
    return render_template('delhi.html')

# BOOKING

@app.route('/booking/<destination>/<hotel>', methods=['GET', 'POST'])
def booking(destination, hotel):

    if request.method == 'POST':

        username = session.get('user')

        new_booking = Booking(
            username=username,
            destination=destination,
            hotel=hotel
        )

        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('success'))

    return render_template(
        'booking.html',
        destination=destination,
        hotel=hotel
    )


# SUCCESS PAGE

@app.route('/success')
def success():
    return render_template('success.html')


# LOGOUT

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


# MAIN

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)