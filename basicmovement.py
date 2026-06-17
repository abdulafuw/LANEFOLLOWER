import RPi.GPIO as GPIO
import time

# ==========================================
# 1. HARDWARE SETUP
# ==========================================
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Pin Definitions (matching your wiring matrix)
IN1 = 17  # Left Forward
IN2 = 15  # Left Reverse
IN3 = 23  # Right Forward
IN4 = 18  # Right Reverse

# Setup pins as outputs
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)

# Set up PWM on the direction pins directly
pwm_in1 = GPIO.PWM(IN1, 1000)
pwm_in2 = GPIO.PWM(IN2, 1000)
pwm_in3 = GPIO.PWM(IN3, 1000)
pwm_in4 = GPIO.PWM(IN4, 1000)

# Start with motors stopped (0% speed)
pwm_in1.start(0) 
pwm_in2.start(0)
pwm_in3.start(0) 
pwm_in4.start(0)

# ==========================================
# 2. MOVEMENT FUNCTIONS
# ==========================================
def move_forward():
    print("Moving Forward...")
    pwm_in1.ChangeDutyCycle(50)
    pwm_in2.ChangeDutyCycle(0)
    pwm_in3.ChangeDutyCycle(50)
    pwm_in4.ChangeDutyCycle(0)

def move_backward():
    print("Moving Backward...")
    pwm_in1.ChangeDutyCycle(0)
    pwm_in2.ChangeDutyCycle(50)
    pwm_in3.ChangeDutyCycle(0)
    pwm_in4.ChangeDutyCycle(50)

def turn_right():
    print("Turning Right... (Left wheel forward, Right wheel backward)")
    pwm_in1.ChangeDutyCycle(50)
    pwm_in2.ChangeDutyCycle(0)
    pwm_in3.ChangeDutyCycle(0)
    pwm_in4.ChangeDutyCycle(50)

def turn_left():
    print("Turning Left... (Left wheel backward, Right wheel forward)")
    pwm_in1.ChangeDutyCycle(0)
    pwm_in2.ChangeDutyCycle(50)
    pwm_in3.ChangeDutyCycle(50)
    pwm_in4.ChangeDutyCycle(0)

def stop_motors():
    print("Stopping.")
    pwm_in1.ChangeDutyCycle(0)
    pwm_in2.ChangeDutyCycle(0)
    pwm_in3.ChangeDutyCycle(0)
    pwm_in4.ChangeDutyCycle(0)

# ==========================================
# 3. EXECUTE TEST SEQUENCE
# ==========================================
try:
    print("Starting chassis test in 3 seconds...")
    time.sleep(3)

    move_forward()
    time.sleep(2)  # Drive for 2 seconds

    stop_motors()
    time.sleep(1)  # Pause for 1 second

    move_backward()
    time.sleep(2)

    stop_motors()
    time.sleep(1)

    turn_right()
    time.sleep(1.5)

    stop_motors()
    time.sleep(1)

    turn_left()
    time.sleep(1.5)

except KeyboardInterrupt:
    print("\nTest interrupted by user.")

finally:
    # Always turn everything off when finished
    stop_motors()
    pwm_in1.stop()
    pwm_in2.stop()
    pwm_in3.stop()
    pwm_in4.stop()
    GPIO.cleanup()
    print("Test complete. Hardware secured.")
