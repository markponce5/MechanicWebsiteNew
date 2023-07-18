from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash
from flask_app.models import user,inquire, build

class Build:
    db='cars_users_in'
    def __init__(self, data):
        self.id = data['id']
        self.name_of_vehicle = data['name_of_vehicle']
        self.amount_spent = data['amount_spent']
        self.suspension = data['suspension']
        self.wheels = data['wheels']
        self.other_info = data['other_info']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None


    @classmethod
    def get_all(cls):
        query= "SELECT * FROM builds LEFT JOIN users ON builds.user_id=users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        builds=[]
        for row in results:
            this_build= cls(row)
            data={
                "id":row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'is_mechanic':row['is_mechanic'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            this_build.creator=user.User(data)
            builds.append(this_build)
        return builds


    @classmethod
    def get_one(cls,data):
        query = """
                SELECT * FROM builds
                JOIN users on builds.user_id = users.id
                WHERE builds.id = %(id)s;
                """
        result = connectToMySQL(cls.db).query_db(query,data)
        if not result:
            return []

        result = result[0]
        this_builds = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": result['password'],
                'is_mechanic':result['is_mechanic'],
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_builds.creator = user.User(user_data)
        return this_builds



    # SAVE      SAVE        SAVE        SAVE        SAVE        SAVE
    @classmethod
    def save(cls,data):
        query = """INSERT INTO builds (name_of_vehicle,amount_spent,suspension,wheels,other_info,user_id)
                    VALUES(%(name_of_vehicle)s,%(amount_spent)s,%(suspension)s,%(wheels)s,%(other_info)s,%(user_id)s);
                """
        result = connectToMySQL(cls.db).query_db(query,data)
        return result



    
        # UPDATE    UPDATE     UPDATE   UPDATE  UPDATE  UPDATE  UPDATE
    @classmethod
    def update(cls,data):
        query = """UPDATE builds 
                    SET name_of_vehicle=%(name_of_vehicle)s,
                    amount_spent=%(amount_spent)s,
                    suspension=%(suspension)s,wheels=%(wheels)s,
                    other_info=%(other_info)s,
                    updated_at=NOW()
                    WHERE id = %(id)s;
                """
        return connectToMySQL(cls.db).query_db(query,data)


        # DELETE    DELETE  DELETE  DELETE  DELETE  DELETE  DELETE  DELETE 
    @classmethod
    def delete(cls, build_id):
        query  = "DELETE FROM builds WHERE id = %(id)s;"
        data = {"id": build_id}
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_build(build):
            is_valid = True # we assume this is true

            if len(build['name_of_vehicle']) < 2:
                flash("Name of Car must be at least 3 characters.")
                is_valid = False
            if len(build['amount_spent']) < 1:
                flash("Amount spent can not be blank, enter N/A if needed")
                is_valid = False
            if len(build['suspension']) < 1:
                flash("Suspension can not be blank, enter N/A if needed")
                is_valid = False
            if len(build['wheels']) < 1 :
                flash("Wheels can not be blank, enter N/A if needed")
                is_valid = False
            if len(build['other_info']) < 1 :
                flash("Other info can not be blank, enter N/A if needed")
                is_valid = False

            return is_valid