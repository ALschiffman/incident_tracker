from flask_app import app
from flask import render_template, flash, redirect, request, session
from flask_app.models.student import Student
from flask_app.models import student
from flask_app.models.course import Course
from flask_app.models.incident import Incident

@app.route("/incident/record/<int:student_id>")
def record_incident(student_id):
    if session["user_id"] == []:
        return redirect('/')
    data = {
        "student_id":student_id
    }
    return render_template('create_incident.html',student= Student.show_one(data))

@app.route("/save_new_incident", methods =["post"])
def save_incident():
    if session["user_id"] == []:
        return redirect('/')
    data = {
        "happened":request.form["happened"],
        "date":request.form["date"],
        "student_id":request.form["student_id"]
    }
    if not Incident.validate_input(data):
        return redirect(f"/incident/record/{data['student_id']}")
    Incident.create(data)
    return redirect(f"/student/view/{data['student_id']}")

@app.route('/incident/update/<int:incident_id>')
def update_incident(incident_id):
    data = {
        "id":incident_id
    }
    return render_template("edit_incident.html", incident = Incident.show_one(data))

@app.route('/incident/edit', methods = ["post"])
def edit_incident():
    data= {
        "id":request.form["id"],
        "happened":request.form["happened"],
        "date":request.form["date"],
        "student_id":request.form["student_id"]
    }
    if not Incident.validate_input(data):
        return redirect(f'/incident/update/{data["id"]}')
    Incident.edit(data)
    return redirect(f"/student/view/{data['student_id']}")

@app.route('/incident/delete/<int:id>/<int:student_id>')
def delete_incident(id,student_id):
    data={
        "id":id
    }
    Incident.delete(data)
    return redirect(f'/student/view/{student_id}')