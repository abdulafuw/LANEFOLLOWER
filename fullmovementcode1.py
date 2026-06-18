import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# --- Motor Pins (No ENA/ENB) ---
IN1 = 17  
IN2 = 15  
IN3 = 23  
IN4 = 18  

# Setup pins as outputs
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)

# Initialize PWM directly on the directional IN pins at 1000Hz
pwm_in1 = GPIO.PWM(IN1, 1000)
pwm_in2 = GPIO.PWM(IN2, 1000)
pwm_in3 = GPIO.PWM(IN3, 1000)
pwm_in4 = GPIO.PWM(IN4, 1000)

# Start all PWMs at 0% duty cycle (motors stopped)
pwm_in1.start(0)
pwm_in2.start(0)
pwm_in3.start(0)
pwm_in4.start(0)

def set_motor_speed(left_speed, right_speed):
    """Safely constraints speed between 0-100 and applies PWM directly to IN pins."""

    left_speed = max(0, min(100, left_speed))
    right_speed = max(0, min(100, right_speed))

    # To move forward: pulse IN1/IN3, keep IN2/IN4 off.
    # (If your robot moves backward instead, swap IN1 with IN2, and IN3 with IN4 here)
    pwm_in1.ChangeDutyCycle(left_speed)
    pwm_in2.ChangeDutyCycle(0)
    
    pwm_in3.ChangeDutyCycle(right_speed)
    pwm_in4.ChangeDutyCycle(0)

cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)

print("Starting Robot Camera Loop. Press Ctrl+C in terminal to stop")

try:
    while True:

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        roi = frame[140:240, 0:320]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        scan_row = thresh[60, :]
        white_pixel_columns = np.where(scan_row == 255)[0]

        if len(white_pixel_columns) > 0:

            lane_center = int(np.mean(white_pixel_columns))
            image_center = 160

            error = lane_center - image_center

            kp = 0.4
            steering_adjustment = error * kp

            base_speed = 35
            final_left_speed = base_speed + steering_adjustment
            final_right_speed = base_speed - steering_adjustment

            set_motor_speed(final_left_speed, final_right_speed)

        else:
            set_motor_speed(0, 0)

        cv2.imshow("Robot Camera View", thresh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nCtrl+C detected. Shutting down engines...")

finally:
    # Safely stop all PWM signals before cleaning up
    pwm_in1.stop()
    pwm_in2.stop()
    pwm_in3.stop()
    pwm_in4.stop()
    
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
    print("Hardware released safely.")
