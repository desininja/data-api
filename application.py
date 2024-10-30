from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Define the Food model
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

# Routes
@app.route('/')
def index():
    return "Hi Hello"

@app.route('/foods')
def get_foods():

    foods = Food.query.all()
    output = []
    for food in foods:
        output.append({'name':food.name,'description':food.description})

    return {"Foods":output}

@app.route('/foods/<id>')
def get_food_with_id(id):
    food = Food.query.get_or_404(id)

    return {"Food Name": food.name, "Description":food.description}

@app.route('/foods',methods=['POST'])
def add_food():
    food = Food(name=request.json['name'],description=request.json['description'])
    db.session.add(food)
    db.session.commit()

    return {'id' : food.id}

@app.route('/foods/<id>',methods=['DELETE'])
def delete_food(id):
    food = Food.query.get(id)
    if food is None:
        return {"Error": "Food id not found"}
    db.session.delete(food)
    db.session.commit()
    return {"Message":"YEET!!!"}