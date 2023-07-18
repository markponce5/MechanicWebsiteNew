from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db='cars_users_in'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.is_mechanic = data['is_mechanic']
        


    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users=[]
        for user in results:
            users.append(cls(user))
        return users

    # SAVE      SAVE        SAVE        SAVE        SAVE        SAVE
    @classmethod
    def save(cls,data):
        print(cls.db)
        query = """INSERT INTO users (first_name,last_name,email,password,is_mechanic)
                    VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(is_mechanic)s);
                """
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id= %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return []
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return []
        return cls(results[0])




    @staticmethod
    def validate_user(user):
            is_valid = True # we assume this is true
            if len(user['first_name']) < 3:
                flash("First Name must be at least 3 characters.")
                is_valid = False
            if len(user['last_name']) < 3:
                flash("Last Name must be at least 3 characters.")
                is_valid = False
            if len(user['email']) < 1:
                flash("Email must not be blank.")
                is_valid = False
            if len(user['password']) < 8:
                flash("password must be at least 8 characters.")
                is_valid = False
            if not user['confirm_password'] == user['password']:
                flash("Passwords must match.")
                is_valid = False
            return is_valid


