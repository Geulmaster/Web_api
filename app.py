from flask import Flask, render_template, flash, request 
from flask_pymongo import PyMongo
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from utils.handler import read_config, JSONEncoder

app = Flask(__name__)
app.config["MONGO_URI"] = read_config()
mongo = PyMongo(app)

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

user_collection = mongo.db.users

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

            user_collection.insert_one({'name' : name, 'email' : email, 'password' : password, 'gender': gender})
            
            print(name, email, password, gender) # In future projects I can jsonify these details
    
        return render_template('index.html', form=form)
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/add/<name>")
def add(name):
    user_collection.insert_one({'name' : str(name), 'email' : 'Python'})
    return '<h1>Added</h1>'

@app.route("/find/<name>")
def find(name):
    user = user_collection.find_one({'name' : name})
    return f'<h1>User: { user["name"] } <br> Email: { user["email"] }</h1>'

@app.route("/update/<name>/<newName>")
def update(name, newName):
    user = user_collection.find_one({'name' : name})
    user["name"] = newName
    user_collection.save(user)
    return f'<h1>Updated username to {newName}!</h1>'

@app.route("/delete/<name>")
def delete(name):
    user = user_collection.find_one({'name' : name})
    if user:
        user_collection.remove(user)
        return render_template("details.html", msg =  f'User {name} has been deleted successfuly') 
    else:
        return render_template("details.html", msg = f'Did not find {name}')

@app.route("/args", methods=['GET'])
def args():
    """
    Receives ID and returns it:
    http://127.0.0.1:5000/args?id=654321 returns 654321
    """
    args_method = request.args.get('id', None)
    print(args_method)
    return f'<h1>{args_method}</h1>'

@app.route("/find")
def find_users():
    docs = []
    str_docs = []
    cursor = user_collection.find()
    for doc in cursor: docs.append(doc)
    for i in docs:
        str_doc = JSONEncoder().encode(i)
        str_docs.append(str_doc)
    formatted_str_docs = "\n".join(str_docs)
    return render_template("details.html", msg = formatted_str_docs)

if __name__ == "__main__":
    app.run(debug=True, port=80)
