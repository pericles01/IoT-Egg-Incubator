import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from simple_pid import PID
import serial

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
sensorPin = 4
humidifierPin = 14
#Motordriver
In1Pin = 17
In2Pin = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(humidifierPin, GPIO.OUT)
GPIO.setup(In1Pin, GPIO.OUT)
GPIO.setup(In2Pin, GPIO.OUT)

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
    In1Pin = 17
    In2Pin = 27
    GPIO.output(In1Pin, GPIO.HIGH)
    GPIO.output(In2Pin, GPIO.LOW)

def motorOff():
    In1Pin = 17
    In2Pin = 27
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
    errorTemp, errorHum = [0], [0]

    while time.time() - start_time < 120:
        temp, hum = getSensorData()
        time.sleep(0.5)
        if(temp<setTemp-1):
            heaterOn()
        else:
            heaterOff()
        if(hum<setHum-1):
            humidifierOn()
        else:
            humidifierOff()

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

def Regler2(setTemp, setHum):

    pid = PID(300, 10.7, 9.8, setpoint=setTemp-1)
    pid.output_limits = (0, 255)

    start_time = time.time()
    last_time = start_time
    # Keep track of values for plotting
    yTemp, yHum, x= [0], [0], [0]
    setpointTemp, setpointHum = [0], [0]
    errorTemp, errorHum = [0], [0]

    while time.time() - start_time < 600:
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
        print(" ") 
        print("- - - - - - - - - - - - - -")
        print(" ") 
            
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

setTemp, setHum = (30, 60)
Regler2(setTemp, setHum)
"""
while True:
    print("motor on")
    motorOn()
    time.sleep(3)
    print("motor off")
    motorOff()
    print("heater on")
    heaterOn()
    time.sleep(3)
    print("heater off")
    heaterOff()
    print("humidifier on")
    humidifierOn()
    time.sleep(6)
    print("humidifier off")
    humidifierOff()
    print("test sensor")
    getSensorData()

    time.sleep(2.0)
"""