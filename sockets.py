#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets
import json
import logging


import RPi.GPIO as GPIO
import time

servo_vert = 17
servo_horz = 27


aForward=24
aBackward=22

bForward=23
bBackward=25
sleeptime=1


GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_vert, GPIO.OUT)
GPIO.setup(servo_horz, GPIO.OUT)

GPIO.setup(aForward, GPIO.OUT)
GPIO.setup(aBackward, GPIO.OUT)
GPIO.setup(bForward, GPIO.OUT)
GPIO.setup(bBackward, GPIO.OUT)

p_vert = GPIO.PWM(servo_vert, 50)
p_horz = GPIO.PWM(servo_horz, 50) 

center_vert = vert = 6.9
center_horz = horz = 7.9

p_vert.start(vert) # Initialization
p_horz.start(horz) # Initialization

async def stopMotors():
    p_horz.stop()
    p_vert.stop()

async def startMotors():
    p_horz.start()
    p_vert.start()


def forward(a, b):
    if a:        
        GPIO.output(aForward, GPIO.HIGH)
    if b:
        GPIO.output(bForward, GPIO.HIGH)

def backward(a, b):
    if a:
        GPIO.output(aBackward, GPIO.HIGH)
    if b:
        GPIO.output(bBackward, GPIO.HIGH)

def stop(a, b):
    if a:
        GPIO.output(aForward, GPIO.LOW)
        GPIO.output(bForward, GPIO.LOW)
    if b:
        GPIO.output(aBackward, GPIO.LOW)
        GPIO.output(bBackward, GPIO.LOW)

def stopAll():
    GPIO.output(aForward, GPIO.LOW)
    GPIO.output(bForward, GPIO.LOW)
    GPIO.output(aBackward, GPIO.LOW)
    GPIO.output(bBackward, GPIO.LOW)

async def moveHorz(direction):
    global horz
    speed = 0.2
    if direction == 'l' and horz < 12.5:
        horz = round(min(horz + speed, 12.5), 1)
        p_horz.ChangeDutyCycle(horz)
        await asyncio.sleep(speed)
    elif direction == 'r' and horz > 2.5:
        horz = round(max(horz - speed, 2.5), 1)
        p_horz.ChangeDutyCycle(horz)
        await asyncio.sleep(speed)
    print("cd horz {}".format(horz))

async def moveVert(direction):
    global vert
    speed = 0.2
    if direction == 'd' and vert < 12.5:
        vert = round(min(vert + speed, 12.5), 1)
        p_vert.ChangeDutyCycle(vert)
        await asyncio.sleep(speed)
    elif direction == 'u' and vert > 2.5:
        vert = round(max(vert - speed, 2.5), 1)
        p_vert.ChangeDutyCycle(vert)
        await asyncio.sleep(speed)    


async def centerVert():
    speed = 0.2
    vert = center_vert
    p_vert.ChangeDutyCycle(vert)
    await asyncio.sleep(speed)  

async def centerHorz():
    speed = 0.2
    horz = center_horz
    p_horz.ChangeDutyCycle(horz)
    await asyncio.sleep(speed)  

async def centerAll():
    speed = 0.2
    p_vert.ChangeDutyCycle(center_vert)
    p_horz.ChangeDutyCycle(center_horz)
    await asyncio.sleep(speed)  

def checkMove(cmd, content):
    return cmd in content and content[cmd]

async def consumer_handler(websocket, path):
    # register(websocket) sends user_event() to websocket
    
    await websocket.send(json.dumps({"status": "ok"}))
    async for message in websocket:
        data = json.loads(message)
        content = data['data']

        print(content)

        if checkMove("q", content): await centerAll()

        if checkMove("d", content): await moveHorz("r")
        elif checkMove("a", content): await moveHorz("l")

        if checkMove("w", content): await moveVert("u")
        elif checkMove("s", content): await moveVert("d")

        if checkMove("d", content): await moveHorz("r")

        if "ArrowRight" in content and content["ArrowRight"]: 
            if "ArrowUp" in content and content["ArrowUp"]: forward(False, True)
            else: backward(True, False)
        elif "ArrowLeft" in content and content["ArrowLeft"]: 
            if "ArrowUp" in content and content["ArrowUp"]: forward(True, False)
            else: backward(False, True)
        elif "ArrowUp" in content and content["ArrowUp"]: forward(True, True)
        elif "ArrowDown" in content and content["ArrowDown"]: backward(True, True)
        else: stopAll()

def start_sockets(server_url):
    try:
        start_server = websockets.serve(consumer_handler, server_url, 5678)
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Sockets    : Server running at %s", server_url)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        p_horz.stop()
        p_vert.stop()
        GPIO.cleanup()
        
