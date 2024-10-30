from flask import Flask
import requests
app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get('http://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')
    for data in response.json()['items']:
        if data['answer_count']==0:
            print(data['title'])
            print(data['link'])
        else:
            print('Skipped')
        print("--------------------------------------")
    print("This is after loop")


    return {'title':data['title'], 'link':data['link']}



with app.app_context():
    food = Food(name='Mutton Gravy', description='Spicy Aromatic Gravy with Mutton')
    db.session.add(food)
    db.session.commit()