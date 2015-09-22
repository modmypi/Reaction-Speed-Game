# Here we import the libraries and function that we will be using in our script
import sys
import time
import atexit
import random
import RPi.GPIO as GPIO

# Set the GPIO numbering mode to BCM
GPIO.setmode(GPIO.BCM)

# Define our tuples
leds = (5,12,17,22,25)
switches = (6,13,19,23,24)
# Define our variables
random_number = -1
correct_button = False
incorrect_button = False
button_pressed = False
max_points = 10
deduction = 5

# Define some functions that our script will use
def buttonPress(channel):
	# This function gets called every time a button is pressed, if the button pressed is the same as the button that is illuminated, then we set the "correct_button" variable to True, otherwise we set the "incorrect_button" variable to True.
	global correct_button, incorrect_button, button_pressed
	# We need to set some variables to global so that this function can change their value.
	print("button pressed %s") % channel
	button_pressed = True
	if channel == switches[random_number]:
		correct_button = True
	else:
		incorrect_button = True

def exit():
	# This function gets called when we exit our script, using Ctrl+C
	print("GPIO Clean Up!")
	GPIO.cleanup()

# This tells our script to use the "exit()" without this, our "exit()" function would never be called.
atexit.register(exit)

# Check that we have defined the same amount of leds as switches
if len(leds) == len(switches):
	max = (len(leds) - 1)
else:
	print("There isn't the same number of LEDS as SWITCHES")
	exit()

# Loop through our switches to set them up
for switch in switches:
	GPIO.setup(switch, GPIO.IN) # Set the switch to be an input
	GPIO.add_event_detect(switch, GPIO.RISING, bouncetime=300) # Add rising edge detection
	GPIO.add_event_callback(switch, buttonPress) # Add the function "buttonPress" to be called when switch is pressed.

# Loop through our leds to set them up
for led in leds:
	GPIO.setup(led, GPIO.OUT) # Set the led to be an ouput
	GPIO.output(led,False) # Turn the led off

# Create an infinite loop, so we can play the game as many times as we want
while(True):

	loop = 10 # This loop tells us how many buttons are going to be illuminated per game.
	counter = 0 # Create a variable to count how many buttons get illuminated.
	score = 0 # Set our score variable to 0.
	
	print("Press the illuminated button to start")
	GPIO.output(leds[2],True) # Turn on the middle led

	while GPIO.input(switches[2]) == GPIO.LOW: # Wait until the middle switch has been pressed.
		time.sleep(0.01)

	for led in leds: # Loop through all the leds and turn them on.
		GPIO.output(led,True)
	
	# Start our countdown
	print("Starting in 5!")
	time.sleep(1) # Wait 1 second

	GPIO.output(leds[0],False) # Turn off the first led.
	print("4!")
	time.sleep(1) # Wait 1 second

	GPIO.output(leds[1],False) # Turn off the second led.
	print("3!")
	time.sleep(1) # Wait 1 second

	GPIO.output(leds[2],False)
	print("2!")
	time.sleep(1)

	GPIO.output(leds[3],False)
	print("1!")
	time.sleep(1)

	GPIO.output(leds[4],False)
	print("Go Go Go!")
	time.sleep(1)
	
	# Start the game
	while counter < loop:
		correct_button = False
		incorrect_button = False
		button_pressed = False
		
		counter += 1 # Increment our counter variable by 1.
		random_delay = random.randint(500,1500) / 1000 # Create a random number to be used as a delay to turn on a led. 
		random_number = random.randint(0,max) # Create another random number to be used to turn on one of the leds.
		
		time.sleep(random_delay) # Wait for a random amount of time, as defined above
		
		GPIO.output(leds[random_number],True) # Turn on a random led, as defined above
		start = time.time() # Take a note of the time when the led was illuminated (so we can see how long it takes for the player to press the button)
		
		while button_pressed == False: # Wait until a button is pressed.
			time.sleep(0.01)
			
		end = time.time() # Take note of the time when the button was pressed.
		time_taken = end - start # Calculate the time it took to press the button.
		GPIO.output(leds[random_number],False) # Turn off the led.
		
		print("Time taken: %f") % time_taken
		
		if correct_button:
			points = round(10 - ((time_taken*10)-1),2) # Crude points system. Score between 0 - 10 points. If you take longer than 1 second you score 0. If you take less than 0.1 seconds you score 10.
			if points < 0: # This just makes sure you don't get a negative point
				points = 0
			print("%f points added to your score!") % points
			score += points # Add your points to your total score
		
		if incorrect_button: # If you press the wrong button (not the button illuminated) you will lose some points!! 
			print("%f points deducted from your score!") % deduction
			score -= deduction
			
		print("New score: %f") % score
			
		time.sleep(1)
	
	# Once the game is over do a little flashy sequence.
	for x in range(0,5):
		for y in range(0,len(leds)):
			GPIO.output(leds[y], 1)
			time.sleep(0.2)
			GPIO.output(leds[y], 0)