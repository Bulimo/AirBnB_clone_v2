#!/usr/bin/python3
"""
script that starts a Flask web application
listen on 0.0.0.0, port 5000
routes: /states_list:         display HTML and state info from storage
        /cities_by_states     display HTML with cities in state info
"""
from flask import Flask, render_template
from models import storage
from models.place import Place
from models.state import State
from models.city import City

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_session(self):
    """
    terminate an SQLAlchemy session
    """
    storage.close()


@app.route('/states_list')
def states_list():
    """
    Display a html page of all States in DB ordered by Name
    """
    state_objs = list(storage.all("State").values())
    return render_template('7-states_list.html', state_objs=state_objs)


@app.route('/cities_by_states')
def cities_by_states_list():
    """
    Display a html page of all cities by States in DB ordered by Name
    """
    state_objs = list(storage.all("State").values())
    return render_template('8-cities_by_states.html', state_objs=state_objs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
