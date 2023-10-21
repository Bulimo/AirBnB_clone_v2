#!/usr/bin/python3
"""
script that starts a Flask web application
listen on 0.0.0.0, port 5000
routes: /states_list:         display HTML and state info from storage
"""
from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    """
    Display a html page of all States in DB ordered by Name
    """
    state_objs = [s for s in storage.all(State).values()]
    return render_template('7-states_list.html', state_objs=state_objs)


@app.teardown_appcontext
def teardown_session():
    """
    terminate an SQLAlchemy session
    """
    storage.close()
