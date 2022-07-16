from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sock import Sock
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

app = Flask(__name__) 
sock = Sock(app)
CORS(app)
api = Api(app)

humidifierPin = 14

GPIO.setmode(GPIO.BCM)

GPIO.setup(humidifierPin, GPIO.OUT)

def humidifierOn():
    humidifierPin = 14
    GPIO.output(humidifierPin, GPIO.HIGH)

def humidifierOff():
    humidifierPin = 14
    GPIO.output(humidifierPin, GPIO.LOW)


class ControlHumidifier(Resource):
    def put(self):
        state = 0
        #data = {'state': this.state1}
        #axios.put('../control/humidifier', data)
        put_data = request.get_json()
        state = put_data.get('state')
        state = int(state)
        if (state == 1):
            humidifierOn()
            print("humidifier on")
            return {"humidifier": True}, 201
        if (state == 0):
            humidifierOff()
            print("humidifier off")
            return {"humidifier": False}, 200
api.add_resource(ControlHumidifier, "/controlHumidifier")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000, debug=True) #IP-Adress Rpi