from flask import Flask, request, make_response
import os
import json
import pyowm

app = Flask(__name__)
api_key = '9545837c17264ab0938215537191003'
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
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    observation = owm.weather_at_place(city)
    weather = observation.get_weather()

    cel = weather.get_temperature('celsius')
    cel_min = str(cel.get('temp_min'))
    cel_max = str(cel.get('temp_max'))
    
    far = weather.get_temperature('fahrenheit')
    far_min = str(far.get('temp_min'))
    far_max = str(far.get('temp_max'))

    status = weather.get_detailed_status()

    output = 'Current conditions in ' + city + ' is ' + status + ' with a low of ' + cel_min + ' C or ' + far_min + ' F' + ' and a high of ' + cel_max + ' C or ' + far_max + ' F.'
    
    return {
        'fullfilmentText': output
    }
    
if __name__ == '__main__':
    app.run(debug=True)