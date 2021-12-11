import logging
import sys
import paho.mqtt.client as mqtt
from adafruit_servokit import ServoKit
# Declare the servo motors...
kit = ServoKit(channels=16)
# 
#  Set up logging to go to journalctl.
# 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
# 
# Handle the throttle speed across requests for speed changes.
def car_speed(direction='up'):
    logger.debug('--> in car_speed direction = ' + direction)
    if not hasattr(car_speed,'throttle'):
        car_speed.throttle = .5
    if direction == 'up':
        car_speed.throttle = round(car_speed.throttle + .1 if car_speed.throttle < 1 else car_speed.throttle,1)
    elif direction == 'down':
        car_speed.throttle = round(car_speed.throttle - .1 if car_speed.throttle > .1 else car_speed.throttle,1)
    else:
        pass
    logger.debug('The throttle speed has been set to '+car_speed.throttle)
    return car_speed.throttle
# 
#  Set up mosquitto sub.
client_name='carbot'
sub_name='carbot/move'
serverAddress = 'doctorgrowbuddy'
mqttClient = mqtt.Client(client_name)
# 
# 
# def on_log(client,userdata,level,buf):
#     logger.debug('log: '+buf)
# 
# 
def on_connect(client, userdata, flags, rc):
    logger.debug("subscribing")
    mqttClient.subscribe(sub_name)
    logger.debug("subscribed")
# 
# 
def on_message(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')

    # MOVE THE CAR FORWARD
    if message == "f":
        logger.debug("^^^ moving forward! ^^^")
        kit.continuous_servo[0].throttle = car_speed('none')
        kit.continuous_servo[1].throttle = car_speed('none')
    # STOP THE CAR
    elif message == "s":
        logger.debug("!!! stopping!")
        kit.continuous_servo[0].throttle = 0
        kit.continuous_servo[1].throttle = 0
    # MOVE THE CAR BACKWARD
    elif message == "b":
        logger.debug("\/ backward \/")
        kit.continuous_servo[0].throttle = -car_speed('none')
        kit.continuous_servo[1].throttle = -car_speed('none')
    # SPEED UP THE CAR
    elif message == '+':
        logger.debug("!!! speeding up!")
        kit.continuous_servo[0].throttle = car_speed('up')
        kit.continuous_servo[1].throttle = car_speed('up')
        
    # SLOW THE CAR DOWN
    elif message == '-':
        logger.debug("!!! slowing down!")
        kit.continuous_servo[0].throttle = car_speed('down')
        kit.continuous_servo[1].throttle = car_speed('down')
    else:
        logger.debug('-- Did not understand the command -- :' + message)

# # 
# 
# Set up calling functions to mqttClient
logger.debug('starting up!')
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
# mqttClient.on_log = on_log

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.

mqttClient.connect(serverAddress)
mqttClient.loop_forever()