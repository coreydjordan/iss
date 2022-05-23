from __future__ import print_function
import requests, sys
from dotenv import dotenv_values
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods= ['POST', 'GET'])
def index():

    if request.method == 'POST':
        
        ENV = dotenv_values()
        response = requests.get(ENV["URL"])
        # print(response.json())

        latitude = response.json()['iss_position']['latitude']
        longitude = response.json()['iss_position']['longitude']

        loc_query = {
            "key": ENV["ACCESS_TOKEN"],
            "lon": longitude,
            "lat": latitude,
            "format": "json"
        }

        loc_res = requests.get(ENV["LOCATION_URL"], params=loc_query).json()
        iss_location = None
        if 'error' in loc_res:
            iss_location = 'Over water'
        else:
            iss_location = loc_res['address']['country']
       
     
        res = {
            'location': location
        }
       
        return render_template('results.html', **res)
    return render_template('index.html')

@app.route('/inspace', methods=['POST', 'GET'])
def in_space():
    if request.method == 'POST':
        ENV = dotenv_values()
        respon = requests.get(ENV['PPL_IN_SPACE'])
        people_in_space = respon.json()['number']
        print(people_in_space)
        r = {
            'number' : people_in_space
        }
        return render_template('inspace.html', **r)
    return render_template('index.html')


if __name__ == '__main__':
    # you could add these things to the .env file if you
    # i.e.  HOST=127.0.0.1 .. etc 

    app.run(host='127.0.0.1', port=8002, debug=True)