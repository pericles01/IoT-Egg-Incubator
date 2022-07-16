
import time
import RPi.GPIO as GPIO
import serial
# Adafruit_DHT 


#Motordriver
In1Pin = 26
In2Pin = 19
EnPin = 15

GPIO.setmode(GPIO.BCM)

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

def heaterOn():
  value = send_to_arduino(1)
  print(value)

def heaterOff():
  value = send_to_arduino(0)
  print(value)


print("test motor")
motorOn()
time.sleep(2)
motorOff()

print("test heater")
heaterOn()
time.sleep(2)
heaterOff()

while True:
    num = input("Enter a number: ") # Taking input from user
    value = send_to_arduino(num)
    print(value) # printing the value

