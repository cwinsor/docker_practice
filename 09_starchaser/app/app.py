import time
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Environment, FileSystemLoader

DBUSER = 'marco'
DBPASS = 'foobarbaz'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'testdb'


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'


db = SQLAlchemy(app)

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))

    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr


def database_initialization_sequence():
    db.create_all()
    test_rec = students(
            'John Doe',
            'Los Angeles',
            '123 Foobar Ave')

    db.session.add(test_rec)
    db.session.rollback()
    db.session.commit()


@app.route('/database', methods=['GET', 'POST'])
def database():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(
                    request.form['name'],
                    request.form['city'],
                    request.form['addr'])

            db.session.add(student)
            db.session.commit()
            flash('Record was succesfully added')
            return redirect(url_for('home'))
    return render_template('show_all.html', students=students.query.all())


@app.route("/results")
def results():

    max_score = 100
    test_name = "Python Challenge"
    students = [
        {"name": "Sandrine",  "score": 100},
        {"name": "Gergeley", "score": 87},
        {"name": "Frieda", "score": 92},
        {"name": "Fritz", "score": 40},
        {"name": "Sirius", "score": 75},
    ]

    context = {
        "title": "Resultss",
        "students": students,
        "test_name": test_name,
        "max_score": max_score,
    }
    return render_template("results.html", **context)

@app.route("/home")
def home():

    return render_template("home.html")

@app.route("/sc01_welcome")
def sc01_welcome():

    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("sc01_welcome.html", user=user, posts=posts)

@app.route("/sc02_player_logout")
def sc02_player_logout():
    context = {
        "title": "logout",    }
    return render_template("sc02_player_logout.html", **context)

@app.route("/sc03_player_signup")
def sc03_player_signup():
    context = {
        "title": "signup",    }
    return render_template("sc03_player_signup.html", **context)

@app.route("/sc04_player_login")
def sc04_player_login():
    context = {
        "title": "login",    }
    return render_template("sc04_player_login.html", **context)

@app.route("/ref01_why_game")
def ref01_why_game():
    return render_template("ref01_why_game.html")

@app.route("/ref05_this_web_application")
def ref05_this_web_application():
    return render_template("ref05_this_web_application.html")

@app.route("/ref08_plasticc_and_kaggle")
def ref08_plasticc_and_kaggle():
    return render_template("ref08_plasticc_and_kaggle.html")

@app.route("/ref04_variety_of_approaches")
def ref04_variety_of_approaches():
    return render_template("ref04_variety_of_approaches.html")

@app.route("/ref06_building_a_model")
def ref06_building_a_model():
    return render_template("ref06_building_a_model.html")

@app.route("/ref09_metrics")
def ref09_metrics():
    return render_template("ref09_metrics.html")














if __name__ == '__main__':
    dbstatus = False
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0')
