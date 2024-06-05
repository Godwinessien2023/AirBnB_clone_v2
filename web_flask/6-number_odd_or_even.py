#!/usr/bin/python3
""" importing Flask module
"""
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ Defining the function hello
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def display_hbnb():
    """ Display HBNB """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def display_C(text):
    """ display “C ” followed by the value of the text variable
    """
    text = text.replace("_", " ")
    return "C {}".format(escape(text))


@app.route("/python/", defaults={"text": "is_cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def display(text):
    """ display “Python ”, followed by the value of the text
        The default value of text is “is cool”
    """
    text = text.replace("_", " ")
    return "Python {}".format(escape(text))


@app.route("/number/<int:n>", strict_slashes=False)
def display_n(n):
    """ display “n is a number” only if n is an integer
    """
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def template(n):
    """ display a HTML page only if n is an integer:
    H1 tag: “Number: n” inside the tag BODY
    """
    return render_template("5-number.html", number=n)


@app.route("/number_odd_or_even/<int:n>",  strict_slashes=False)
def odd_or_even(n):
    """ display a HTML page only if n is an integer:
    H1 tag: “Number: n is even|odd” inside the tag BODY
    """
    if isinstance(n, int):
        n_type = "even" if n % 2 == 0 else "odd"
        return render_template("6-number_odd_or_even.html", n=n, n_type=n_type)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
