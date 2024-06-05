#!/usr/bin/python3
""" importing Flask module
"""
from flask import Flask
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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
