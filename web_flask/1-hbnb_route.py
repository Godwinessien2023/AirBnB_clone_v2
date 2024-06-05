#!/usr/bin/python3
""" importing Flask module
"""
from flask import Flask

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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
