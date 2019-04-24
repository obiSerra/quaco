#!/usr/bin/env python3



import logging
import threading
import time
import RPi.GPIO as GPIO

from camera import start_camera
from sockets import start_sockets

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

def main():
    try:
        server_url = '192.168.1.101'

        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Main    : Initializing the camera")
        camera = threading.Thread(target=start_camera, args=(server_url,))
        logging.info("Main    : starting camera")
        camera.start()
        logging.info("Main    : Starting sockets ")
        start_sockets(server_url)
    except KeyboardInterrupt:
        logging.info("Main    : all done")
        GPIO.cleanup()

if __name__ == '__main__':
    main()

