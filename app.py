import secrets

from cs50 import SQL
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, diagramGenerate1, diagramGenerate2, diagramGenerate3, current_time

app = Flask(__name__)

# Configure time zone
app.config['TIMEZONE'] = 'Europe/Berlin'

app.secret_key = secrets.token_hex(16)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tyremanager.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    current_set = db.execute("SELECT * FROM tyre_settings ORDER BY id DESC LIMIT 1")
    lastest_order = db.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 1")

    if not current_set or not lastest_order:
        return render_template("index.html")

    order_nr = current_set[0]['order_number']
    order = db.execute("SELECT * FROM orders WHERE order_number = ?", order_nr)

    data = db.execute("SELECT description, COUNT(*) AS count FROM orders GROUP BY description")
    number_list = [item['count'] for item in data]
    desc_list = [item['description'] for item in data]
    diagram = diagramGenerate3(desc_list, number_list)
    return render_template("index.html", current_set=current_set, order=order, lastest_order=lastest_order, diagram=diagram)


# login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure role was submitted
        elif not request.form.get("roles"):
            return apology("must provide role", 400)

        # Check if username already exists
        users = db.execute(
            "SELECT username FROM users WHERE username = ?", request.form.get("username")
        )
        if len(users) != 0:
            return apology("Usermame is not available")

        # Check if password is identical with passwwor_again
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match", 400)

        db.execute("INSERT INTO users (username, hash, role) VALUES (?,?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")), request.form.get("roles"))

        new_user_id = db.execute("SELECT id FROM users WHERE username = ?",
                                 request.form.get("username"))

        # Log in the new user
        session["user_id"] = new_user_id[0]["id"]

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/contingent", methods=["GET", "POST"])
@login_required
def contingent():

    # just show contingent for today
    # today = datetime.datetime.now().date()
    # contingents = [contingent for contingent in contingents if datetime.datetime.strptime(contingent['time'], '%Y-%m-%d %H:%M:%S').date() == today]

    if request.method == "POST":

        # the add button is clicked
        if "add" in request.form:
            type = request.form.get("type")
            desc = ""
            quota = request.form.get("quota")
            time = current_time()

            # add the value of description
            if "cold" in type:
                desc = "1xx"
            elif "medium" in type:
                desc = "2xx"
            elif "hot" in type:
                desc = "3xx"
            elif "inters" in type:
                desc = "4xx"
            elif "dry" in type:
                desc = "5xx"
            elif "heavy" in type:
                desc = "6xx"

            # check if input valid
            if not type or not desc or not quota:
                return apology("Invalid input", 400)

            db.execute(
                "INSERT INTO contingents (type, description, quota, time) VALUES (?,?,?,?)", type, desc, quota, time)
            flash("Added!")

        # delete button is clicked
        # use delete when the contingent input is wrong
        elif "delete" in request.form:
            # get id contingent id from input field
            id = request.form.get('delete')

            # delete the contingent if there is no order from it
            try:
                db.execute("DELETE FROM contingents WHERE id = ?", id)
            except ValueError as e:
                return apology("Can not delete the contingent which already has orders from it", 500)
            flash("Deleted!")

            contingents = db.execute("SELECT * FROM contingents")
            return render_template("contingent.html", contingents=contingents, id=id)

    contingents = db.execute("SELECT * FROM contingents")
    return render_template("contingent.html", contingents=contingents)


@app.route("/order", methods=["GET", "POST"])
@login_required
def order():

    if request.method == "POST":

        # the add button is clicked
        if "order" in request.form:

            # get input
            desc = request.form.get("type_desc")
            order_number = 0
            rl = request.form.get("rear-left")
            rr = request.form.get("rear-right")
            fl = request.form.get("front-left")
            fr = request.form.get("front-right")
            order_time = current_time()
            status = request.form.get("status")

            # check if input valid
            if not desc or not rl or not rr or not fl or not fr or not status:
                return apology("Invalid input", 400)

            # format order_number
            counter = db.execute(
                "SELECT COUNT(*) AS counter FROM orders WHERE description = (?)", desc)

            # check if counter is empty
            if not counter:
                order_number = int(desc[0]) * 100 + 1
            else:
                order_number = int(desc[0]) * 100 + counter[0]['counter'] + 1

            # check quota before order
            quota = db.execute("SELECT quota FROM contingents WHERE description = (?)", desc)
            if quota[0]['quota'] > 0:
                try:
                    db.execute("INSERT INTO orders (description, order_number, rear_left, rear_right, front_left, front_right, order_time, status) VALUES (?,?,?,?,?,?,?,?)",
                               desc, order_number, rl, rr, fl, fr, order_time, status)
                    db.execute("UPDATE contingents SET quota = quota - 1 WHERE description = ?", desc)
                    flash("Ordered!")
                except ValueError as e:
                    return apology("This type doesn't exist in contingent", 500)
            else:
                return apology("This type has been used up", 400)

        # the delete button is clicked
        # use delete when order input is wrong
        elif "delete" in request.form:
            # get orderId from input field
            orderId = request.form.get('delete')

            # get description of that order
            order = db.execute("SELECT * FROM orders WHERE id = ?", int(orderId))
            desc = order[0]['description']

            try:
                # delete the order
                db.execute("DELETE FROM orders WHERE id = ?", orderId)
                # increase quota back
                db.execute("UPDATE contingents SET quota = quota + 1 WHERE description = ?", desc)
            except ValueError as e:
                return apology("Can not delete an finished order!", 500)
            flash('Deleted!')

        elif "time-end" in request.form:
            current_endtime = request.form.get("time-end")
            db.execute(
                "UPDATE orders SET pickup_time = ? WHERE id = ( SELECT MAX(id) FROM orders )", current_endtime)
            flash('Add pickup time!')

        elif "status" in request.form:
            status = request.form.get("status")
            if status == "Status":
                return apology("Choose new status!", 400)

            db.execute(
                "UPDATE orders SET status = ? WHERE id = ( SELECT MAX(id) FROM orders )", status)
            flash('Status updated!')

    # query the data in orders to display in the table
    orders = db.execute("SELECT * FROM orders")

    return render_template("order.html", orders=orders)


@app.route("/weather", methods=["GET", "POST"])
@login_required
def weather():

    if request.method == "POST":
        if "addWeather" in request.form:
            time = current_time()
            airTemp = request.form.get("airTemp")
            trackTemp = request.form.get("trackTemp")
            trackCond = request.form.get("trackCond")

            if not airTemp or not trackTemp or not trackCond:
                return apology("Invalid input", 400)

            db.execute("INSERT INTO weathers (time, air_temp, track_temp, track_cond) VALUES (?,?,?,?)",
                       time, airTemp, trackTemp, trackCond)
            flash("Added!")

        elif "delete" in request.form:
            weatherId = request.form.get("delete")
            db.execute("DELETE FROM weathers WHERE id = ?", weatherId)
            flash("Deleted!")

    # data to output
    data = db.execute("SELECT * FROM weathers")

    time_list = [(item['time'].split())[1][:5] for item in data]
    air_temp = [item['air_temp'] for item in data]
    track_temp = [item['track_temp'] for item in data]
    diagram = diagramGenerate2(time_list, air_temp, track_temp)
    return render_template("weather.html", data=data, diagram=diagram)


@app.route("/fuel", methods=["GET", "POST"])
@login_required
def fuel():

    if request.method == "POST":
        if "addFuel" in request.form:
            time = current_time()
            driver = request.form.get("driver")
            amount = request.form.get("amount")
            note = request.form.get("note")

            if not amount or not driver:
                return apology("Invalid input", 400)

            db.execute("INSERT INTO fuels (time, driver, amount, note) VALUES (?,?,?,?)",
                       time, driver, amount, note)
            flash("Added!")

        elif "delete" in request.form:
            fuel_id = request.form.get("delete")
            db.execute("DELETE FROM fuels WHERE id = ?", fuel_id)
            flash("Deleted!")

    # data to output
    data = db.execute("SELECT * FROM fuels")

    time_list = [(item['time'].split())[1][:5] for item in data]
    amount_list = [item['amount'] for item in data]
    diagram = diagramGenerate1(time_list, amount_list)
    return render_template("fuel.html", data=data, diagram=diagram)


@app.route("/setting", methods=["GET", "POST"])
@login_required
def setting():
    current_order = db.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 1")
    if not current_order:
        return apology("You have no available tyre set. Add an order first", 500)
    else:
        order_number = current_order[0]['order_number']

    if request.method == "POST":
        if "addSetting" in request.form:
            rl_press = request.form.get("rlPress")
            rr_press = request.form.get("rrPress")
            fl_press = request.form.get("flPress")
            fr_press = request.form.get("frPress")
            rim_temp = request.form.get("rimTemp")
            heating_temp = request.form.get("heatingTemp")
            heating_start = current_time()
            status = request.form.get("status")

            if not rl_press or not rr_press or not fl_press or not fr_press or not rim_temp or not heating_temp or not status:
                return apology("Invalid input", 400)

            db.execute("INSERT INTO tyre_settings (order_number, rl_press, rr_press, fl_press, fr_press, rim_temp, heating_temp, heating_start, status) VALUES (?,?,?,?,?,?,?,?,?)",
                       order_number, rl_press, rr_press, fl_press, fr_press, rim_temp, heating_temp, heating_start, status)
            flash("Added!")

        elif "delete" in request.form:
            setting_id = request.form.get("delete")
            db.execute("DELETE FROM tyre_settings WHERE id = ?", setting_id)
            flash("Deleted!")

        elif "time-end" in request.form:
            current_endtime = request.form.get("time-end")
            db.execute(
                "UPDATE tyre_settings SET heating_end = ? WHERE id = ( SELECT MAX(id) FROM tyre_settings )", current_endtime)
            flash('Add heating end time!')

        elif "status" in request.form:
            status = request.form.get("status")
            if status == "Status":
                return apology("Choose new status!", 400)

            db.execute(
                "UPDATE tyre_settings SET status = ? WHERE id = ( SELECT MAX(id) FROM tyre_settings )", status)
            flash('Status updated!')

    data = db.execute("SELECT * FROM tyre_settings")
    return render_template("setting.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
