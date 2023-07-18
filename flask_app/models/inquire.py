from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
from flask_app.models import user,build,inquire

class Inquire:
    db='cars_users_in'
    def __init__(self, data):
        self.id = data['id']
        self.make_of_vehicle = data['make_of_vehicle']
        self.model_of_vehicle = data['model_of_vehicle']
        self.service_needed = data['service_needed']
        self.aftermarket = data['aftermarket']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None


    @classmethod
    def get_one(cls):
        query= "SELECT * FROM inquires LEFT JOIN users ON inquires.user_id=users.id WHERE inquires.id=%(id)s ;"
        results = connectToMySQL(cls.db).query_db(query)
        inquires=[]
        for row in results:
            this_inquires= cls(row)
            data={
                "id":row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            this_inquires.creator=user.User(data)
            inquires.append(this_inquires)
        return inquires

    @classmethod
    def save(cls,data):
        query = """INSERT INTO inquires(make_of_vehicle,model_of_vehicle,service_needed,aftermarket,user_id)
                    VALUES(%(make_of_vehicle)s,%(model_of_vehicle)s,%(service_needed)s,%(aftermarket)s,%(user_id)s);
                """
        result = connectToMySQL(cls.db).query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM inquires
                JOIN users on inquires.user_id = users.id
                """
        result = connectToMySQL(cls.db).query_db(query)
        if not result:
            return []

        inquires = []
        for x in result:
            this_inquire = cls(x)
            user_data = {
                    "id": x['users.id'],
                    "first_name": x['first_name'],
                    "last_name": x['last_name'],
                    "email": x['email'],
                    "password": x['password'],
                    "is_mechanic":x['is_mechanic'],
                    "created_at": x['users.created_at'],
                    "updated_at": x['users.updated_at']
            }
            this_inquire.creator = user.User(user_data)
            inquires.append(this_inquire)

        return inquires





    





    @staticmethod
    def validate_inquire(inquire):
            is_valid = True # we assume this is true
            if len(inquire['make_of_vehicle']) < 2:
                flash("Make of Car must be at least 3 characters.")
                is_valid = False
            if len(inquire['model_of_vehicle']) < 2:
                flash("Model of Car must be at least 3 characters.")
                is_valid = False
            if len(inquire['service_needed']) < 1:
                flash("Service needed can not be blank, enter N/A if needed")
                is_valid = False
            if len(inquire['aftermarket']) < 1:
                flash("Aftermarket Install can not be blank, enter N/A if needed")
                is_valid = False

            return is_valid