from flask import render_template, request, redirect, session, flash

from flask_app import app

from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/')
def index():
    return render_template('login_register.html')



@app.route("/register", methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    if not is_valid :
        return redirect('/')
    hash= bcrypt.generate_password_hash(request.form['password'])
    if 'is_mechanic' not in request.form:
            is_mechanic = 0
    else:
        is_mechanic = 1

    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':hash,
        'is_mechanic':is_mechanic
        
    }
    id=User.save(data)
    session["user_id"]= id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



