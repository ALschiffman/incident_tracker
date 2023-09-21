from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex= re.compile(r'^[a-zA-Z]+[0-9]')

class User:
    def __init__(self,db_data):
        self.id=db_data["id"]
        self.first_name = db_data["first_name"]
        self.last_name= db_data["last_name"]
        self.email=db_data["email"]
        self.password = db_data["password"]
        self.classes = []
    
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data["first_name"]) <2:
            is_valid = False
            flash("invalid first name")
        if len(data["last_name"]) <2:
            is_valid = False
            flash("invalid  last_name")
        if not EMAIL_REGEX.match(data["email"]):
            is_valid = False
            flash("invalid email")
        if len(data["password"])<8:
            is_valid=False
            flash("password must be at least 8 charachters long")
        if not password_regex.match(data["password"]):
            is_valid = False
            flash("password must contain a number")
        if not data["password"] == data["conf_password"]:
            is_valid=False
            flash("Password does not match")
        return is_valid

    @classmethod
    def create(cls,data):
        query="insert into users (first_name, last_name, email, password) Values (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL('student_info').query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query="delete from users where id = %(id)s"
        return connectToMySQL('student_info').query_db(query,data)
    
    @classmethod
    def get_all(cls):
        qeury="select * from users;"
        results = connectToMySQL('student_info').query_db(qeury)
        all_users=[]
        for i in results:
            all_users.append(cls(i))
        return all_users
    
    @classmethod
    def get_by_email(cls,raw_data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('student_info').query_db(query,raw_data)
        if len(result) <1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query="Select * from users where id = %(id)s;"
        result= connectToMySQL("student_info").query_db(query,data)
        return cls(result[0])