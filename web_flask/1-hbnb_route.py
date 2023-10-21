#!/usr/bin/python3
"""
script that starts a Flask web application
    listen on 0.0.0.0, port 5000
    routes: /:     display "Hello HBNB!"
            /hbnb: display "HBNB"
"""
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def hello():
    """ Initialize content in the root page """
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """ Initialize content in the hbnb page """
    return "HBNB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
