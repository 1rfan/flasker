from flask import Flask, render_template

# create a flask instance
app = Flask(__name__)

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
