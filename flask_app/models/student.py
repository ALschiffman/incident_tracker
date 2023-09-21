from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.incident import Incident
from flask_app.models import incident

class Student:
    def __init__(self,db_data):
        self.id=db_data["id"]
        self.first_name = db_data["first_name"]
        self.last_name =db_data["last_name"]
        self.class_id=db_data["class_id"]
        self.incidents = []
        
    @staticmethod
    def validate_class(data):
        is_valid = True
        if len(data["first_name"]) <2:
            is_valid = False
            flash("invalid first name")
        if len(data["last_name"]) <1:
            is_valid = False
            flash("invalid last name")
        return is_valid
    
    @classmethod
    def create(cls,data):
        query="insert into student (first_name, last_name, class_id, created_at) values (%(first_name)s,%(last_name)s, %(class_id)s, NOW());"
        return connectToMySQL('student_info').query_db(query,data)
    
    @classmethod
    def edit(cls,data):
        query = "update student set first_name = %(first_name)s, last_name = %(last_name)s, class_id = %(class_id)s, updated_at = NOW() where id = %(id)s;"
        return connectToMySQL('student_info').query_db(query,data)

    @classmethod
    def show_one(cls,data):
        query = "select * from student left join incident on student.id = incident.student_id where student.id = %(student_id)s;"
        results = connectToMySQL('student_info').query_db(query,data)
        if not results:
            return False
        student = cls(results[0])
        for i in results:
            incident_data = {
                "id":i["incident.id"],
                "happened":i["happened"],
                "date":i["date"],
                "student_id":i["student_id"]
            }
            incident_instance = Incident(incident_data)
            #student.incidents = incident_instance
            student.incidents.append(incident_instance)
        return student
    
    @classmethod
    def delete (cls,data):
        query="delete from student where id =%(id)s;"
        return connectToMySQL('student_info').query_db(query,data)
    
    @classmethod
    def show_class(cls,data):
        query = "select * from student where class_id = %(class_id)s;"
        results = connectToMySQL('student_info').query_db(query,data)
        if not results:
            return False
        all_students = []
        for i in results:
            all_students.append(cls(i))
        return all_students