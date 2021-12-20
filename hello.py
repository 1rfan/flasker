from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# create a flask instance
app = Flask(__name__)
# create a secret key (CSRF)
app.config['SECRET_KEY'] = "my super secret key dat nobody should know!"

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
