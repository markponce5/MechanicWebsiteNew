from flask import Flask , render_template, redirect,request, session 

from flask_app import app

from flask_app.models import build, user, inquire




# dashboard             dashboard               dashboard       dashboard  

@app.route("/builds")
def show_build():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("builds_list.html",user=user.User.get_one({"id":session['user_id']}),all_builds=build.Build.get_all() )

# edit      edit        edit   å             edit            edit



@app.route('/update/build/<int:id>', methods=['POST'])
def update_build(id):
    if 'user_id' not in session:
        return redirect('/')
    if not build.Build.validate_build(request.form):
        return redirect(f'/edit/{id}')

    data = {
        'id': id,
        'name_of_vehicle': request.form['name_of_vehicle'],
        'amount_spent': request.form['amount_spent'],
        'suspension': request.form['suspension'],
        'wheels': request.form['wheels'],
        'other_info': request.form['other_info'],

    }
    build.Build.update(data)
    return redirect("/builds")


@app.route('/edit/<int:id>')
def edit_build(id):
    if 'user_id' not in session:
        return redirect('/')
    this_build=build.Build.get_one({'id':id})
    return render_template('edit_car.html',build=this_build)

@app.route("/create/build")
def create_build():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("new_car.html")





# view              view                view                    view



@app.route("/view/<int:id>")
def view_build(id):
    if 'user_id' not in session:
        return redirect('/')
    this_build=build.Build.get_one({'id':id})
    return render_template("view_car.html",build=this_build,user=user.User.get_one({"id":session['user_id']}))






@app.route('/delete/<int:build_id>')
def delete_build(build_id):
    if 'user_id' not in session:
        return redirect('/')
    build.Build.delete(build_id)
    return redirect("/builds")


# create            create                  create              create






@app.route("/add/build", methods=['POST'])
def add_build():
    if 'user_id' not in session:
        return redirect('/')
    is_valid = build.Build.validate_build(request.form)
    if not is_valid :
        return redirect("/create/build")
    data={
        'name_of_vehicle': request.form['name_of_vehicle'],
        'amount_spent': request.form['amount_spent'],
        'suspension': request.form['suspension'],
        'wheels': request.form['wheels'],
        'other_info': request.form['other_info'],
        "user_id":session["user_id"]
        
    }
    id=build.Build.save(data)
    
    return redirect("/builds")



@app.route("/contact/us")
def contact_us():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("contact.html")

