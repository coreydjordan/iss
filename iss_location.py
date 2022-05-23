import requests
from dotenv import dotenv_values


from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():

    
    ENV = dotenv_values()

    query = {
        "lat": '45',
        "lon": '180'
    }

    response = requests.get(ENV["URL"], params=query)
    # print(response.json())

    latitude = response.json()['iss_position']['latitude']
    longitude = response.json()['iss_position']['longitude']

    loc_query = {
        "key": ENV["ACCESS_TOKEN"],
        "lon": longitude,
        "lat": latitude,
        "format": "json"
    }

    loc_res = requests.get(ENV["LOCATION_URL"], params=loc_query)
    print(f"Over {loc_res.json()['address']['country']}")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)