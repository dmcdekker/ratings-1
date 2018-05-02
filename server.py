"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    # print users
    return render_template("user_list.html", users=users)

@app.route('/users/:user_id')
def user_details():

    user_id = request.args.get('user_id')

    return render_template("user_profile.html", user_id=user_id)




@app.route("/register", methods=["GET"])
def show_register():
    """Show registration form."""

    return render_template("register.html")



@app.route("/register", methods=['POST'])
def register_user():
    """Register a new user."""
    
    email = request.form.get('user_email')
    password = request.form.get('password')


    query_db = db.session.query(User).filter_by(email=email).all()

    # flash("query:" + query_db)

    if query_db:
        flash("User email already in use")
        return redirect('/register')

    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash("Sucessfully registered.")    
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
