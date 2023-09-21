from flask_app import app
from flask import request,redirect, render_template, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('index.html')

@app.route('/login_register',methods=["Post"])
def register():
    raw_data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":request.form["password"],
        "conf_password":request.form["conf_password"]
    }
    if not User.validate_user(raw_data):
        return redirect('/')
    user_in_db = User.get_by_email(raw_data)
    if user_in_db:
        flash("invalid email")
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data ={
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash
    }
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect('/all_classes')

@app.route('/login', methods = ["Post"])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/all_classes")

@app.route("/logout", methods=["Post"])
def logout():
    session['user_id'] = []
    return redirect("/")