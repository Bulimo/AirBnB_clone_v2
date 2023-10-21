#!/usr/bin/python3
"""

"""
from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    """ """
    state_objs = [s for s in storage.all("State").values()]
    return render_template('7-states_list.html', state_objs=state_objs)


@app.teardown_appcontext
def teardown_session():
    """ """
    storage.close()
