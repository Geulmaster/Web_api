from flask import Flask, render_template, flash, request, Blueprint 
from flask_pymongo import PyMongo
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class Details(Form):
    name = TextField('Name:', validators=[validators.DataRequired()])
    email = TextField('Email:', validators=[validators.DataRequired(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.DataRequired(), validators.Length(min=3, max=35)])
    
    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = Details(request.form)
        print(form.errors)

        if request.method == 'POST':
            name=request.form['name']
            password=request.form['password']
            email=request.form['email']
            gender = request.form['options']

            user_collection = mongo.db.users
            user_collection.insert_one({'name' : name, 'email' : email, 'password' : password, 'gender': gender})
            
            print(name, email, password, gender) # In future projects I can jsonify these details
    
        if form.validate():
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')
    
        return render_template('index.html', form=form)
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/add/<name>")
def add(name):
    user_collection = mongo.db.users
    user_collection.insert_one({'name' : str(name), 'email' : 'Python'})
    return '<h1>Added</h1>'

@app.route("/find/<name>")
def find(name):
    user_collection = mongo.db.users
    user = user_collection.find_one({'name' : name})
    return f'<h1>User: { user["name"] } <br> Email: { user["email"] }</h1>'

@app.route("/update/<name>/<newName>")
def update(name, newName):
    user_collection = mongo.db.users
    user = user_collection.find_one({'name' : name})
    user["name"] = newName
    user_collection.save(user)
    return f'<h1>Updated username to {newName}!</h1>'

@app.route("/delete/<name>")
def delete(name):
    user_collection = mongo.db.users
    user = user_collection.find_one({'name' : name})
    user_collection.remove(user)
    return '<h1>Deleted User!</h1>'

@app.route("/args", methods=['GET'])
def args():
    """
    Receives ID and returns it
    """
    poop = request.args.get('id', None)
    print(poop)
    return '<h1>{}</h1>'.format(poop)

if __name__ == "__main__":
    app.run(debug=True)
