import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request


app = Flask(__name__)
load_dotenv()
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/find_iss', methods = ['POST', 'GET'])
def index():

    if request.method == 'POST':
        
        # query = {
        #     "lat": '45',
        #     "lon": '180'
        # }
        access_token = os.getenv("ACCESS_TOKEN")
        response = requests.get(os.getenv('URL'))
        latitude = response.json()['iss_position']['latitude']
        longitude = response.json()['iss_position']['longitude']
    

        # print(response.json())

     

        loc_query = {
            "key": access_token,
            "lon": longitude,
            "lat": latitude,
            "format": "json"
        }

        loc_res = requests.get(os.getenv("LOCATION_URL"), params=loc_query).json()
        
        
        if 'error' in loc_res:
            over_water = 'Over Water'
            return over_water
        
        res = {
            'location': loc_res['address']['country']
        }
        print(loc_res)
        return render_template('results.html', **res)
    return render_template('find_iss.html')

@app.route('/inspace', methods=['POST', 'GET'])
def in_space():
    if request.method == 'POST':
        respon = requests.get(os.getenv('PPL_IN_SPACE'))
        
        people_in_space = respon.json()['number']

        
        r = {
            'number' : people_in_space
        }
        return render_template('inspace.html', **r)
    return render_template('people_in_space.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=True)