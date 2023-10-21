#!/usr/bin/python3
"""
script that starts a Flask web application
    listen on 0.0.0.0, port 5000
    routes: /:     display "Hello HBNB!"
            /hbnb: display "HBNB"
            /c/<text>: display “C ” followed by the value of
                the text variable
            /python/<text>: display “Python ”, followed by
                the value of the text variable
            /number/<n>: display “n is a number” only if n is an integer
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


@app.route("/c/<text>")
def c(text):
    """ Initialize content in the c/ page """
    my_text = text.replace('_', ' ')
    return "C {}".format(my_text)


@app.route('/python')
@app.route('/python/<text>')
def python(text='is cool'):
    """ Initialize content in the python/ page """
    my_text = text.replace('_', ' ')
    return "Python {}".format(my_text)


@app.route('/number/<int:n>')
def int_number(n):
    """ Initialize content in the number/ page """
    return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
