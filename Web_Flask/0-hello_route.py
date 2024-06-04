#!/usr/bin/python3
from flask import Flask


"""
Create a Flask app
"""
app = Flask(__name__)

"""
Define route for the homepage
"""
@app.route('/', strict_slashes=False)
def hello_hbnb():
    return "Hello HBNB!"

"""
Run the app
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
