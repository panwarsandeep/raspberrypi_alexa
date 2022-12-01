import logging
import os

from time import sleep
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as gpio 

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on','high']
STATUSOFF = ['off','low']
STATUSDANCE = ['dance', 'dancing']
STATUSRED = ['red']
STATUSGREEN = ['green']
STATUSYELLOW = ['yellow']

R=8
G=10
Y=12

def light(col=R, ctrl=0):
  gpio.output(col, ctrl)

def on_off_all(ctrl=0):
  gpio.output(R, ctrl)
  gpio.output(G, ctrl)
  gpio.output(Y, ctrl)

def dance(wait=0.5):
  on_off_all()
  ctr = 1
  while ctr < 3:
    ctr += 1
    on_off_all()
    light(R, 1)
    sleep(wait)
    on_off_all()
    light(G, 1)
    sleep(wait)
    on_off_all()
    light(Y, 1)
    sleep(wait)

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('GpioIntent', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)
    gpio.setup(8, gpio.OUT, initial=gpio.LOW)
    gpio.setup(10, gpio.OUT, initial=gpio.LOW)
    gpio.setup(12, gpio.OUT, initial=gpio.LOW)
    if status in STATUSON:
	GPIO.output(17,GPIO.HIGH)
        on_off_all(1)
	return statement('turning on all the lights')
    elif status in STATUSOFF:
        on_off_all(0)
        return statement('turning off all the lights')
    elif status in STATUSDANCE:
        dance(0.1)
        #on_off_all(0)
        return statement('made the lights dance')
    elif status in STATUSRED:
        light(R, 1)
        #dance(0.1)
        return statement('turning on red light')
    elif status in STATUSGREEN:
        light(G, 1)
        return statement('turning on green light')
    elif status in STATUSYELLOW:
        light(Y, 1)
        return statement('turning on yellow light')
    else:
        return statement('Sorry not possible.')
 
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
