from tempsensor import Thermistor
from WiFiNetwork import WiFi
from ThingSpeak import ThingSpeakApi
from time import sleep
from mq2 import MQ2
from machine import Pin, PWM
import urequests

#just a edit
#Sensor Initialization
pin =26
sensor1 = Thermistor(pin)

#ThingSpeak Initialization
thingspeak = ThingSpeakApi()

#Network Initialization
network = WiFi()
ip = network.ConnectWiFi()

#mq 2 sensor Initialization
pin=27

sensor2 = MQ2(pinData = pin, baseVoltage = 3.3)
print("Calibrating MQ- 2 sensor")
sensor2.calibrate()
print("Calibration completed")
print("Base resistance:{0}".format(sensor2._ro))

#mq 135 initialization
mq135 = Pin(17, Pin.IN)
buzzer = PWM(Pin(15))

#Main Program
while True:
    temperature = sensor1.ReadTemperature()
    print(f"T = {temperature}°C")
    
    temperatureF = round((temperature*1.8) + 32, 2)
    
    smoke = sensor2.readSmoke()
    print("Smoke: {:.1f}".format(smoke)+" - ", end="")
    LPG = sensor2.readLPG()
    print("LPG: {:.1f}".format(LPG)+" - ", end="")
    methane = sensor2.readMethane()
    print("Methane: {:.1f}".format(methane)+" - ", end="")
    hydrogen = sensor2.readHydrogen()
    print("Hydrogen: {:.1f}".format(hydrogen))
    #print("Smoke: " + smoke + "- LPG: " + LPG + "- Methane: " + methane + "- Hydrogen: " + hydrogen)
    
    field_data = (temperature, smoke, LPG, methane, hydrogen)
    thingspeak.WriteMultipleFields(field_data)
    
    if mq135.value() == 1:
        url2 = 'https://maker.ifttt.com/trigger/toohot/with/key/mytSXwpPleLNBIiJnOZttXPTAas2_QjQqH5FtEOtEY9'
        request = urequests.post(url2)
        request.close()
        #buzzer.freq(500)
        #uzzer.duty_u16(1000)
        #sleep(5)
        #buzzer.duty_u16(0)
        
    sleep(20)