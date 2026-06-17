import cv2
import numpy as np
import RPi.GPIO as GPIO
import smbus 
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
ENA=12
IN1=5
IN2=6
ENB=13
IN3=19
IN4=26
GPIO.setup([IN1,IN2,IN3,IN4,ENA,ENB],GPIO.OUT)
pwm_left=GPIO.PWM(ENA,1000)
pwm_right=GPIO.PWM(ENB,1000)
pwm_left.start(0)
pwm_right.start(0)
try
    bus=smbus.SMBus(1)
    bus.write_byte_data(0x68,0x6B,0)
    print("MPU6050 initialized successfully.")
except:
    print("Warning:MPU6050 not detected. Check I2C wiring.")
def set_motor_speed(left_speed,right_speed):
    """Safely constraints speed between 0-100 and applies them."""

    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)

    left_speed=max(0,min(100,left_speed))
    right_speed=max(0,min(100,right_speed))

    pwm_left.ChangeDutyCycle(left_speed)
    pwm_right.ChangeDutyCycle(right_speed)

cap = cv2.videoCapture(0)
cap.set(3,320)
cap.set(4,240)


print("Starting Robot Camera Loop. Press Ctrl+C in terminal to stop")


try:
    while True:

        ret,frame=cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        roi = frame[140:240,0:320]

        gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray,100,255,cv2.THRESH_BINARY)

        scan_row = thresh[60,:]
        white_pixel_columns = np.where(scan_row ==255)[0]

        if len(white_pixel_columns) > 0

            lane_center = int(np.mean(white_pixel_columns))
            image_center = 160

            error = lane_center - image_center

            kp=0.4
            steering_adjustment = error * kp

            base_speed = 35
            final_left_speed = base_speed+steering_adjustment
            final_right_speed= base_speed-steering_adjustment

            set_motor_speed(final_left_speed,final_right_speed)

        else:

            set_motor_speed(0,0)

        cv2.imshow("Robot Camera View",thresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
   cept KeyboardInterrupt:
     print("\nCtrl+C detected. Shutting down engines...")

   nally:


     pwm_left.stop()
     pwm_right.stop()
     GPIO.cleanup()
     cap.release()
     cv2.destroyAllWindows()
     print("Hardware released safely.")
    
                      