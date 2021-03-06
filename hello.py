from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# create a flask instance
app = Flask(__name__)
# add database
# old database sqlite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# new mysql db 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:irfan123@localhost/users'
# create a secret key (CSRF)
app.config['SECRET_KEY'] = "my super secret key dat nobody should know!"
# initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# create model


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # create a string
    def __repr__(self):
        return '<Name %r>' % self.name


# create a user form class


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")

# update database record


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", form=form, name_to_update=name_to_update)
        except:
            flash("Error! Seems like a problem occured. Try again?")
            return render_template("update.html", form=form, name_to_update=name_to_update)
    else:
        return render_template("update.html", form=form, name_to_update=name_to_update, id=id)

# create a form class


class NamerForm(FlaskForm):
    name = StringField("What's yer name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create a route decorator


@app.route('/')
def index():
    favorite_pizza = ["pepperoni", "jinja", "cheese", "masalodeh"]
    nama = "jeppu'"
    return render_template("index.html",
                           favorite_pizza=favorite_pizza,
                           nama=nama)

# localhost:5000/user/jepp


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# pej dok jumpe


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# seber rosak


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# create name page


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template("name.html", name=name, form=form)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data,
                         favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)

    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Sucessfully!!")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:
        flash("Whoops! threre was a problem dele")
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
