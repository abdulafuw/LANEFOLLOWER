import cv2
import numpy as np
import RPi.GPIO as GPIO
import smbus 
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
ENA=12
IN1=