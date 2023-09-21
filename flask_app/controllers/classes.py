from flask_app import app
from flask import render_template, flash, redirect, request, session
from flask_app.models.course import Course
from flask_app.models import course
from flask_app.models.user import User
from flask_app.models.student import Student

@app.route ("/all_classes")
def show_all():
    if session["user_id"] == []:
        return redirect('/')
    if session["user_id"] == []:
        return redirect('/')
    data={
        "id":session["user_id"]
    }
    session["class_id"] = []
    return render_template("all_classes.html",classes =Course.show_all_of_mine(data),this_user = User.get_by_id(data) )

@app.route("/class/create")
def create_form():
    if session["user_id"] == []:
        return redirect('/')
    return render_template("create_class.html")

@app.route("/save_new_class", methods =["Post"])
def save_new_class():
    if session["user_id"] == []:
        return redirect('/')
    data = {
        "class_name":request.form["class_name"],
        "subject": request.form["subject"],
        "users_id":session["user_id"]
    }
    if not Course.validate_class(data):
        return redirect("/class_create")
    Course.create(data)
    return redirect("/all_classes")

@app.route("/class/view/<int:class_id>")
def view_class(class_id):
    if session["user_id"] == []:
        return redirect('/')
    data ={
        "class_id":class_id
    }
    session["class_id"]= class_id
    return render_template('class.html',students = Student.show_class(data),course = Course.get_by_id(data))

@app.route('/class/update/<int:class_id>')
def update(class_id):
    data={
        "class_id":class_id
    }
    return render_template("edit_class.html", course= Course.get_by_id(data))

@app.route('/class/edit', methods = ["post"])
def edit():
    data = {
        "class_id":request.form["id"],
        "class_name":request.form["class_name"],
        "subject":request.form["subject"]
    }
    if not Course.validate_class(data):
        return redirect(f'/class/update/{data["class_id"]}')
    Course.edit(data)
    return redirect('/all_classes')

@app.route('/class/delete/<int:class_id>')
def delete_class(class_id):
    data = {
        "id":class_id
    }
    Course.delete(data)
    return redirect('/all_classes')