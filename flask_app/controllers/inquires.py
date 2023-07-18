from flask import Flask , render_template, redirect,request, session 

from flask_app import app

from flask_app.models import inquire,build,user




# dashboard             dashboard               dashboard       dashboard  
# @app.route("/inquires/dashboard")
# def show_inquire():
#     if 'user_id' not in session:
#         return redirect('/')
#     return render_template("dashboard.html",user=user.User.get_all())


@app.route("/dashboard")
def show_dashboard():
    if 'user_id' not in session:
        return redirect('/')
    print("this is the user id")
    print(session['user_id'])
    this_user=user.User.get_one({'id':session['user_id']})
    items=inquire.Inquire.get_all()

    return render_template("dashboard.html",items=items,this_user=this_user)


# edit      edit        edit                edit            edit


@app.route('/update/inquire/<int:id>', methods=['POST'])
def update_inquire(id):
    if 'user_id' not in session:
        return redirect('/')
    if not inquire.Inquire.validate_inquire(request.form):
        return redirect('/create')

    data = {
        'id': id,
        'make_of_vehicle': request.form['make_of_vehicle'],
        'model_of_vehicle': request.form['model_of_vehicle'],
        'service_needed': request.form['service_needed'],
        'aftermarket': request.form['aftermarket']
    }

    inquire.Inquire.update(data)
    return redirect('/dashboard')


@app.route('/make/inquire', methods=['POST'])
def make_inquire(id):
    if 'user_id' not in session:
        return redirect('/')
    if not inquire.Inquire.validate_inquire(request.form):
        return redirect('/create')

    data = {
        'id': id,
        'make_of_vehicle': request.form['make_of_vehicle'],
        'model_of_vehicle': request.form['model_of_vehicle'],
        'service_needed': request.form['service_needed'],
        'aftermarket': request.form['aftermarket']
    }

    inquire.Inquire.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_inquire(id):
    if 'user_id' not in session:
        return redirect('/')
    this_inquire=inquire.Inquire.get_one({'id':id})
    return render_template('edit_car.html',inquire=this_inquire)





@app.route("/create/inquire")
def create_inquire():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("inquires.html")



# view              view                view                    view










@app.route('/delete/<int:inquire_id>')
def delete_inquire(inquire_id):
    if 'user_id' not in session:
        return redirect('/')
    build.Build.delete(inquire_id)
    return redirect('/inquires/dashboard')


# create            create                  create              create






@app.route("/add/inquire", methods=['POST'])
def add_inquire():
    if 'user_id' not in session:
        return redirect('/')
    is_valid = inquire.Inquire.validate_inquire(request.form)
    if not is_valid :
        return redirect("/create/inquire")
    data={
        'make_of_vehicle': request.form['make_of_vehicle'],
        'model_of_vehicle': request.form['model_of_vehicle'],
        'service_needed': request.form['service_needed'],
        'aftermarket': request.form['aftermarket'],
        "user_id":session["user_id"]
        
    }
    id=inquire.Inquire.save(data)
    
    return redirect('/dashboard')



