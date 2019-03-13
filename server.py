from flask import Flask, request, make_response
import datetime
import os
import json
import pyowm

app = Flask(__name__)
api_key = 'f6582b4d5cad0e9d264cdc29cb229779'
owm = pyowm.OWM(api_key)

#geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):   
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date_orig = parameters.get("date")

    observation = owm.weather_at_place(city)
    weather = observation.get_weather()

    cel = weather.get_temperature('celsius')
    cel_min = str(cel.get('temp_min'))
    cel_max = str(cel.get('temp_max'))
    
    far = weather.get_temperature('fahrenheit')
    far_min = str(far.get('temp_min'))
    far_max = str(far.get('temp_max'))

    status = weather.get_detailed_status()

    if date_orig is None or date_orig == "":
        output = 'Today '
    else:
        output = 'On ' + date_orig[:10]
    output = output + ' in ' + city + ', the forecast is for ' + status + ' with a low of ' + round_temp(cel_min) + ' C or ' + round_temp(far_min) + ' F' + ' and a high of ' + round_temp(cel_max) + ' C or ' + round_temp(far_max) + ' F.'
    
    return {
        'fulfillmentText': output,
    }

def round_temp(temp):
    return str(round(float(temp)))

if __name__ == '__main__':
    app.run(debug=True)