from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Course:
    def __init__(self,db_data):
        self.id=db_data["id"]
        self.class_name = db_data["class_name"]
        self.subject=db_data["subject"]
        self.user_id=db_data["users_id"]
        self.students = []
        
    @staticmethod
    def validate_class(data):
        is_valid = True
        if len(data["class_name"]) <2:
            is_valid = False
            flash("invalid class name")
        if len(data["subject"]) <3:
            is_valid = False
            flash("invalid subject name")
        return is_valid
    
    @classmethod
    def create(cls,data):
        query="insert into class (class_name, subject, users_id, created_at) values (%(class_name)s,%(subject)s, %(users_id)s, NOW());"
        return connectToMySQL('student_info').query_db(query,data)
    
    @classmethod
    def edit(cls,data):
        query = "update class set class_name = %(class_name)s, subject = %(subject)s, updated_at = NOW() where id = %(class_id)s;"
        return connectToMySQL('student_info').query_db(query,data)

    @classmethod
    def show_all_of_mine(cls,data):
        query = "select * from class where users_id =%(id)s;"
        results = connectToMySQL('student_info').query_db(query,data)
        all_classes = []
        if results == False:
            return False
        for i in results:
            all_classes.append(cls(i))
        return all_classes
    
    @classmethod
    def get_by_id(cls,data):
        query= "select * from class where id = %(class_id)s;"
        result = connectToMySQL('student_info').query_db(query,data)
        return cls(result[0])
    @classmethod
    def delete (cls,data):
        query="delete from class where id =%(id)s"
        return connectToMySQL('student_info').query_db(query,data)
    