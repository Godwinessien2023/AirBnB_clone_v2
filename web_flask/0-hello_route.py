#!/usr/bin/python3
from flask import Flask

"""
Create a Flask app
"""
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """
    Define route for the homepage
    """
    return "Hello HBNB!"


"""
Run the app
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
