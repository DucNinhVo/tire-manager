import base64
import csv
import datetime
import pytz
import requests
import urllib
import uuid

from datetime import datetime
from io import BytesIO
from matplotlib.figure import Figure
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def diagramGenerate1(time, amount):
    fig = Figure(figsize=(17, 6))
    ax = fig.subplots()
    ax.plot(time, amount)
    ax.set(xlabel='Time', ylabel='Amount',
           title='Amount of fuel loaded per stop')
    ax.grid()
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


def diagramGenerate2(time, air_temp, track_temp):
    fig = Figure(figsize=(17, 6))
    ax = fig.subplots()
    ax.plot(time, air_temp, label="Air temperatur")
    ax.plot(time, track_temp, label="Track temperatur")
    ax.legend()
    ax.set(xlabel='Time', ylabel='Temperatur',
           title='Air and track temperature')
    ax.grid()
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


def diagramGenerate3(desc, number):
    fig = Figure(figsize=(10, 6))
    ax = fig.subplots()
    ax.bar(desc, number)
    ax.set(xlabel='Tire Types', ylabel='Frequecy of use',
           title='Which types of tires are used and how often')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


def current_time():
    current_time = datetime.now()
    formated_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formated_time
