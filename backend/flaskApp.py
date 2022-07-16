from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sock import Sock
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from simple_pid import PID
import serial

app = Flask(__name__) 
sock = Sock(app)
CORS(app)
api = Api(app)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)
sensorPin = 4
heaterPin = 15
humidifierPin = 14
#Motordriver
In1Pin = 26
In2Pin = 19
EnPin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(heaterPin, GPIO.OUT)
GPIO.setup(humidifierPin, GPIO.OUT)
GPIO.setup(In1Pin, GPIO.OUT)
GPIO.setup(In2Pin, GPIO.OUT)
GPIO.setup(EnPin, GPIO.OUT)

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
arduino.flush()
def send_to_arduino(x):
    data = str(x)
    data  = data + '\n' 
    #print(data)
    #print(type(data))
    arduino.write(data.encode('utf-8'))
    time.sleep(0.05)
    #arduino.flush()
    data = arduino.readline().decode('utf-8').rstrip()
    return data


def heaterOn():
  value = send_to_arduino(1)
  print(value)

def heaterOff():
  value = send_to_arduino(0)
  print(value)

def humidifierOn():
    humidifierPin = 14
    GPIO.output(humidifierPin, GPIO.HIGH)

def humidifierOff():
    humidifierPin = 14
    GPIO.output(humidifierPin, GPIO.LOW)

def motorOn():
    In1Pin = 26
    In2Pin = 19
    GPIO.output(In1Pin, GPIO.HIGH)
    GPIO.output(In2Pin, GPIO.LOW)

def motorOff():
    In1Pin = 26
    In2Pin = 19
    GPIO.output(In1Pin, GPIO.LOW)
    GPIO.output(In2Pin, GPIO.LOW)

def getSensorData():
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        #temperature_c, humidity = (24.5, 46.7)
        time.sleep(0.5)
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        #continue
    except Exception as error:
        dhtDevice.exit()
        #temperature_c, humidity = (-1, -1)
        raise error
    print(
            "Temp: {:.1f} °C    Humidity: {}% ".format(
                temperature_c, humidity
            )
        )
    return temperature_c, humidity

def Regler(setTemp, setHum):
    start_time = time.time()
    last_time = start_time
    # Keep track of values for plotting
    yTemp, yHum, x= [0], [0], [0]
    setpointTemp, setpointHum = [0], [0]

    while time.time() - start_time < 120:
        temp, hum = getSensorData()
        if(temp<0 and hum<0):
            continue
        if(temp<setTemp):
            heaterOn()
        else:
            heaterOff()
        if(hum<setHum):
            humidifierOn()
        else:
            humidifierOff()

        time.sleep(0.5)
        current_time = time.time()
        last_time = current_time
        x.append(current_time - start_time)
        yTemp.append(temp)
        yHum.append(hum)
        setpointTemp.append(setTemp)
        setpointHum.append(setHum)
        
    heaterOff()
    humidifierOff()
    GPIO.cleanup()

    plt.plot(x, yHum,'b-', label='Humidity')
    plt.plot(x, yTemp,'r-', label='Temperature')
    plt.plot(x, setpointTemp,'g-', label='Set Temperature')
    plt.plot(x, setpointHum,'m-', label='Set Humidity')
    plt.xlabel('time (s)')
    plt.ylabel('measured')
    plt.legend()
    plt.show()

def Regler2(setTemp, setHum):

    pid = PID(5, 1.6, 2.3, setpoint=setTemp)
    pid.output_limits = (0, 255)

    start_time = time.time()
    last_time = start_time
    # Keep track of values for plotting
    yTemp, yHum, x= [0], [0], [0]
    setpointTemp, setpointHum = [0], [0]
    errorTemp, errorHum = [0], [0]

    while time.time() - start_time < 120:
        temp, hum = getSensorData()
        time.sleep(0.5)
        if(hum<setHum-1):
            humidifierOn()
        else:
            humidifierOff()
             
        dutyCycle = pid(temp)
        print("Output PID: {}".format(dutyCycle))
        #control heater pin/ dimm heater with pid output
        value = send_to_arduino(dutyCycle)
        print(value) 
            
        current_time = time.time()
        last_time = current_time
        T_err = setTemp - temp
        H_err = setHum - hum

        x.append(current_time - start_time)
        yTemp.append(temp)
        yHum.append(hum)
        setpointTemp.append(setTemp)
        setpointHum.append(setHum)
        errorTemp.append(T_err)
        errorHum.append(H_err)

    heaterOff()
    humidifierOff()
    GPIO.cleanup()

    plt.subplot(2, 1, 1)
    plt.plot(x, yHum,'b-', label='Humidity')
    plt.plot(x, yTemp,'r-', label='Temperature')
    plt.plot(x, setpointTemp,'g-', label='Set Temperature')
    plt.plot(x, setpointHum,'m-', label='Set Humidity')
    plt.xlabel('time (s)')
    plt.ylabel('measured')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(x, errorHum,'b-', label='Error Humidity')
    plt.plot(x, errorTemp,'r-', label='Error Temperature')
    plt.xlabel('time (s)')
    plt.ylabel('calculated')
    plt.legend()

    plt.show()

@sock.route('/data')
def datastream(ws):

    temp, hum = 23.7, 48
    while True:
        #data = ws.receive()
        #temp, hum = getSensorData()
        #temp = dhtDevice.temperature
        #hum = dhtDevice.humidity
        data = {"temperature": temp, "humidity": hum}
        time.sleep(5.0)
        ws.send(data)
        temp += 0.5
        hum += 1

class Regulate(Resource):
    def put(self):
        #in Frontend
        #data = {{'x': this.x},{'y':this.y}}
        #axios.put('../job', data)
        put_data = request.get_json()
        x = put_data.get('setTemp')
        x = float(x)
        y = put_data.get('setHum')
        y = float(y)
        #Regler(x, y)
        Regler2(x, y)
        return {"setTemp": x, "setHum": y},200       
api.add_resource(Regulate, "/job")

class ControlHeater(Resource):
    def put(self):
        state = 0
        #data = {'state': this.state1}
        #axios.put('../control/heater', data)
        put_data = request.get_json()
        state = put_data.get('state')
        state = int(state)
        if (state == 1):
            heaterOn()
            print("heater on")
            return {"heater": True}, 201
        if (state == 0):
            heaterOff()
            print("heater off")
            return {"heater": False}, 200
api.add_resource(ControlHeater, "/controlHeater")

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

class ControlMotor(Resource):
    def put(self):
        state = 0
        #data = {'state': this.state1}
        #axios.put('../control/humidifier', data)
        put_data = request.get_json()
        state = put_data.get('state')
        state = int(state)
        if (state == 1):
            motorOn()
            print("motor on")
            return {"motor": True}, 201
        if (state == 0):
            motorOff()
            print("motor off")
            return {"motor": False}, 200
api.add_resource(ControlMotor, "/controlMotor")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 5000, debug=True) #IP-Adress Rpi