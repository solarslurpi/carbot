import logging
import sys
from enum import Enum
import paho.mqtt.client as mqtt
from adafruit_servokit import ServoKit
class Movement(Enum):
    FORWARD=1
    BACKWARD=2
    STOP=3
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
class carbot:
    # The Servos don't turn the way I think they should.
    # The one connected to 0 goes the opposite direction than the other...
    def __init__(self):
        self.throttle_speed = .1
        self.command = None
        self.prev_movement = Movement.STOP
    def forward(self):

        kit.continuous_servo[0].throttle = -self.throttle_speed
        kit.continuous_servo[1].throttle = self.throttle_speed
        logger.debug("^^^ moving forward! ^^^ at speed "+str(self.throttle_speed))
        self.prev_movement = Movement.FORWARD
    def backward(self):
 
        kit.continuous_servo[0].throttle = self.throttle_speed
        kit.continuous_servo[1].throttle = -self.throttle_speed
        self.prev_movement = Movement.BACKWARD
        logger.debug("^^^ moving backward! ^^^ at speed "+str(self.throttle_speed))
    def stop(self):
        kit.continuous_servo[0].throttle = 0
        kit.continuous_servo[1].throttle = 0
        self.prev_movement = Movement.STOP
        logger.debug("^^^ stopped! ^^^")
    def slow_down(self):
        self.throttle_speed = round(self.throttle_speed - .1 if self.throttle_speed > .1 else self.throttle_speed,1)
        if self.prev_movement == Movement.FORWARD:
            self.forward()
        elif self.prev_movement == Movement.BACKWARD:
            self.backward()
        logger.debug("^^^ slowed speed down to "+ str(self.throttle_speed))
    def speed_up(self):
        self.throttle_speed = round(self.throttle_speed + .1 if self.throttle_speed < 1 else self.throttle_speed,1)
        if self.prev_movement == Movement.FORWARD:
            self.forward()
        elif self.prev_movement == Movement.BACKWARD:
            self.backward()
        logger.debug("^^^ speeded up to "+str(self.throttle_speed))

bot = carbot()
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
        bot.forward()
    # STOP THE CAR
    elif message == "s":
        bot.stop()
    # MOVE THE CAR BACKWARD
    elif message == "b":
        bot.backward()
    # SPEED UP THE CAR
    elif message == '+':
        bot.speed_up()
    # SLOW DOWN THE CAR
    elif message == '-':
        bot.slow_down()
        
  

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