from flask_app import app
from flask import render_template, flash, redirect, request, session
from flask_app.models.student import Student
from flask_app.models import student
from flask_app.models.course import Course


@app.route("/students/add")
def new_student():
    if session["user_id"] == []:
        return redirect('/')
    data = {
        "class_id":session["class_id"]
    }
    return render_template("create_student.html",classes = Course.get_by_id(data))

@app.route("/save_new_student", methods=["Post"])
def save_new_student():
    if session["user_id"] == []:
        return redirect('/')
    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "class_id":request.form["class_id"]
    }
    Student.create(data)
    return redirect(f"/class/view/{session['class_id']}")

@app.route("/student/view/<int:student_id>")
def view_student(student_id):
    if session["user_id"] == []:
        return redirect('/')
    data ={
        "id":student_id,
        "student_id":student_id
    }
    return render_template('student.html',student = Student.show_one(data))

@app.route('/student/edit/<int:student_id>')
def edit_student(student_id):
    data ={
        "student_id":student_id
    }
    return render_template('edit_student.html', student = Student.show_one(data))

@app.route('/student/update', methods = ["post"])
def update_student():
    data = {
        "id":request.form["id"],
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "class_id":request.form["class_id"]
    }
    if not Student.validate_class(data):
        return redirect(f'/student/edit/{data["id"]}')
    Student.edit(data)
    return redirect(f'/class/view/{data["class_id"]}')
    
@app.route('/student/delete/<int:id>')
def delete_student(id):
    data={
        "id":id
    }
    Student.delete(data)
    return redirect(f'/class/view/{session["class_id"]}')