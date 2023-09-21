from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Incident:
    def __init__(self,db_data):
        self.id=db_data["id"]
        self.happened = db_data["happened"]
        self.date=db_data["date"]
        self.student_id=db_data["student_id"]
        
    @staticmethod
    def validate_input(data):
        is_valid = True
        if len(data["happened"]) <5:
            is_valid = False
            flash("invalid description")
        if len(data["date"]) <1:
            is_valid = False
            flash("invalid date")
        return is_valid
    
    @classmethod
    def create(cls,data):
        query="insert into incident (happened, date, student_id, created_at) values (%(happened)s,%(date)s, %(student_id)s, NOW());"
        return connectToMySQL('student_info').query_db(query,data)
    
    @classmethod
    def edit(cls,data):
        query = "update incident set happened = %(happened)s, date = %(date)s, student_id = %(student_id)s, updated_at = NOW() where id = %(id)s;"
        return connectToMySQL('student_info').query_db(query,data)

    @classmethod
    def show_one(cls,data):
        query = "select * from incident where id = %(id)s;"
        results = connectToMySQL('student_info').query_db(query,data)
        return cls(results[0])
    @classmethod
    def show_all_of_student(cls,data):
        query = "select * from incidents where student_id = %(student_id)s;"
        results = connectToMySQL('student_info').query_db(query,data)
        all_incidents = []
        for i in results:
            all_incidents.append(cls(i))
        return all_incidents
    
    @classmethod
    def delete (cls,data):
        query="delete from incident where id =%(id)s"
        return connectToMySQL('student_info').query_db(query,data)
    