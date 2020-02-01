from flask import Flask, render_template, flash, request, Blueprint  
from flask_pymongo import PyMongo
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.DataRequired()])
    email = TextField('Email:', validators=[validators.DataRequired(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.DataRequired(), validators.Length(min=3, max=35)])
    
    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)
    
        print(form.errors)
        if request.method == 'POST':
            name=request.form['name']
            password=request.form['password']
            email=request.form['email']
            gender = request.form['options']
            print(name, email, password, gender) # In future projects I can jsonify these details
    
        if form.validate():
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')
    
        return render_template('index.html', form=form)
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/data")
def data():
    user_collection = mongo.db.users
    user_collection.insert_one({'name' : 'sas'})
    return '<h1>Added</h1>'

@app.route("/find")
def find():
    user_collection = mongo.db.users
    user = user_collection.find_one({'name' : 'sas'})
    return f'<h1>User: { user["name"] }</h1>'

if __name__ == "__main__":
    app.run(debug=True)
