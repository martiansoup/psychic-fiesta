# SERVER CODE
import dbus
import uuid
import http.server
import http.server
import socketserver
import urllib.parse
import threading

patterns = {
  "solid": 0,
  "wipe": 1,
  "theatre": 2,
  "bands": 3,
  "rainbow": 4,
  "tracer-white": 5,
  "tracer-redgreen": 6,
  "twinkle": 7
}

current_pattern = 0
app_colour = (0,0,255)

def a(p):
  bus = dbus.SystemBus()
  server = dbus.Interface(bus.get_object("org.freedesktop.Avahi", "/"), "org.freedesktop.Avahi.Server")
  entry_proxy = bus.get_object("org.freedesktop.Avahi", server.EntryGroupNew())
  group = dbus.Interface(entry_proxy, "org.freedesktop.Avahi.EntryGroup")
  txt = [bytes("v=1", 'utf-8'), bytes("uuid={}".format(uuid.uuid3(uuid.UUID(int=87289120657916253993124272263640532377), "xmas")), 'utf-8')]
  group.AddService(-1, -1, 0, "Christmas Lights", "_yuwot._tcp", "", "", p, txt)
  group.Commit()

class Handler(http.server.SimpleHTTPRequestHandler):
  def r(self,output):
      self.send_response(http.HTTPStatus.OK)
      self.send_header("Content-type", "application/json")
      self.send_header("Cache-Control", "no-cache")
      self.send_header("Content-Length", str(len(output)))
      self.end_headers()
      self.wfile.write(bytes(output, 'utf-8'))
  def do_GET(self):
    if "describe" in self.path:
      enum = ",".join(patterns.keys())
      output = """{"routes":[
  {"endpoint":"setPattern","name":"Set Pattern","value_type":"enum("""
      output += enum
      output += """)","fn_type":"s"},
  {"endpoint":"setColour","name":"Set Colour","value_type":"colour8","fn_type":"s"},
  {"endpoint":"getColour","name":"Get Colour","value_type":"colour8","fn_type":"g"}
],"links":{"setColour":"getColour"}}"""
      self.r(output)
    elif "getColour" in self.path:
      output = '{{"ok":true,"name":"getStripColour","value":{{"r":{},"g":{},"b":{}}}}}'.format(*app_colour)
      self.r(output)
    else:
      self.r("")
  def do_POST(self):
    global current_pattern,app_colour
    if "setPattern" in self.path:
      p = self.path.split('/')[-2]
      current_pattern = patterns[p]
      self.r('{"ok":true}')
    elif "setColour" in self.path:
      p = self.path.split('/')[-2]
      c = p.replace("(", "").replace(")", "").split(",")
      app_colour = (int(c[0]), int(c[1]), int(c[2]))
      self.r('{"ok":true}')

s = None
def server():
  global s
  with socketserver.TCPServer(("", 0), Handler) as httpd:
    s = httpd
    a(httpd.server_address[1])
    print("Server started at http://{}:{}".format(*httpd.server_address))
    httpd.serve_forever()

threading.Thread(target=server).start()
# SERVER CODE END

# This is written in the python language, '#' at the start
# of the line is a comment

#################################
# Load libraries (don't change) #
#################################

# These are some libraries that the code will use
#  'time' gives some functions to allow delaying for an
#         amount of time
import time
#  'board' gives the definition of which pin the lights
#          are connected to
import board
#  'neopixel' has the code to control the lights themselves
import neopixel
#  'GPIO' allows reading a button
import RPi.GPIO as GPIO
#  'random' for random number generating
import random

#######################
# Setup the neopixels #
#######################

# The LED strip is connected to pin D18 (or GPIO 18) of the
# Raspberry Pi (see diagram at https://pinout.xyz/)
# Pin 18 has the necessary electronics that can control neopixels.
pixel_pin = board.D18

# The number of neopixels that are connected
# The first pixel will be '0' and the last pixel
# will be 'num_pixels-1'.
# E.g. for 50 pixels they will be pixel 0 to
# pixel 49.
num_pixels = 50

# 'pixels' is used to interact with the neopixels, this line is
# setting up the variable that is used to control the neopixels.
# This code says to call the 'Neopixel' function in the 'neopixel'
# library, passing the following values:
#   - the pin the pixels are connected to from above
#   - the number of pixels from above
#   - the brightness (from 0-1)
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1,
                           auto_write=False, pixel_order=neopixel.GRB)

############
# Patterns #
############
# This section defines the patterns available

# A function to draw a fixed colour on all pixels
# This says to define ('def') a function called 'fixed_colour' which
# takes a single parameter, which is the colour to be drawn.
# This colour will be in the format '(R, G, B)' where each of
# R, G and B are a number from 0 to 255.
# E.g. solid red would be '(255, 0, 0)'
def fixed_colour(colour):
    # Now the contents of the function are defined,
    # in python this is done by indenting the code by 4 spaces.

    # Now we want to loop over every pixel, so we say that we
    # want a range from 0 to the number of pixels 'range(num_pixels)'
    # then we say to assign each number in this list to 'index'
    # E.g. if there were 2 pixels this loop would be run 2 times,
    #      with 'index' having a value of 0, and then a value of 1
    for index in range(num_pixels):
        # As we are now inside the loop, the code is indented
        # again by 4 spaces, this indicates the code here is
        # within the 'for' loop

        # This code uses the 'pixels' variable we created before to
        # set a colour of a single pixel.
        # 'pixels[index]' says we want to control the pixel at
        # 'index' and then it is set to 'colour'
        # This doesn't actually change the colour yet, just says
        # that we want the pixel at 'index' to be 'colour' when we
        # next update.
        pixels[index] = colour

    # Now that all pixels have been looped over, the code is
    # un-indented.
    # This indicates that the code for the loop is done, and
    # this will be run after the loop has been run for each pixel.

    # As we have now said that we want each pixel to be 'colour'
    # we can now say we want to update the pixels.
    # 'pixels.show()' takes the values we said we want the pixels
    # to be and updates the physical pixels.
    pixels.show()

    # Now that we have updated the colour of every pixel we wait for
    # 0.1 seconds (so we're not updating things continuously)
    time.sleep(0.1)

# If there are no more indented lines then this is the end of the
# 'fixed_colour' function.

# This function performs a wipe effect, starting with all pixels off
# and turning them on in order, starting from one end of the strip.
# After all the pixels are turned on the pixels are turned off one
# by one in reverse order.
def wipe():
    # To start we want to turn all pixels off, so we set red, green
    # and blue to zero. This ensures anything "left over" from a
    # previous pattern isn't shown.
    pixels.fill((0, 0, 0))
    # Update the pixels to all off.
    pixels.show()

    # Again we want to loop over all the pixels, and will turn each
    # one on in turn. The loop index indicates the last pixel that
    # should be turned on, so it is named 'max_pixel'.
    for max_pixel in range(num_pixels):
        # Now we want to loop over pixels from zero until 'max_pixel'
        # and turn each of them on.
        # This time we want to light up 'max_pixel' as well so we
        # add one, as 'range' goes up to one below the maximum.
        for index in range(max_pixel+1):
            # We set the pixel at 'index' to be white.
            # All of red, green and blue set to 255 which is fully
            # on.
            pixels[index] = (255, 255, 255)
        # After updating all the pixels from 0 until 'max_pixel'
        # we want to update the pixels themselves.
        # (This is un-indented once so we have ended one loop)
        pixels.show()

        # After turning on leds from 0 to 'max_pixel' we want
        # to delay for a bit before we move to the next iteration
        # of the loop where we light up from 0 to 'max_pixel+1'
        time.sleep(0.01)

    # Now we do the same loop(s) again to turn the lights off
    for max_pixel in range(num_pixels):
        for index in range(max_pixel+1):
            # This time though we want to turn the pixels off
            # in reverse so we start at 'num_pixels' and
            # subtract the index.
            # E.g. if there are 50 pixels:
            #   index 0  -> 50 - 1 - 0 = 49
            #   index 1  -> 50 - 1 - 1 = 48
            #   ...
            #   index 49 -> 50 - 1 - 49 = 0
            # And so we turn off pixel 49 first, then go down
            # to pixel 0.
            i = num_pixels - 1 - index
            # Turn this pixel off
            pixels[i] = (0, 0, 0)

        # Again after looping over each index, display the new
        # values and then wait before turning off the next pixel
        pixels.show()
        time.sleep(0.01)

# This is the end of the wipe pattern.

# This function performs a 'theatre chase' effect, lighting
# up each third light and moving them in a marquee.
# (As in a now playing sign outside a theatre)
def theatre():
    # Set the size of the pattern to 3, this can be modified
    # so, for example, only 1 in 5 pixels is lit.
    num_steps = 3
    # Each 3 pixels should take the following steps in
    # the pattern:
    #   (on , off, off)
    #   (off, on , off)
    #   (off, off, on )
    # So it looks like the lit pixel is moving from
    # left to right.
    # As the pattern has 3 steps we want to loop this
    # many times to draw each step of the pattern.
    for step in range(num_steps):
        # For each step of the pattern we want to
        # check each pixel and see if it should be
        # on or off. So we loop over every pixel
        for index in range(num_pixels):
            # A pixel is lit if the remainder when
            # divided by 3 is zero. This means that
            # each third pixel will be lit.
            # Modulo '%' will give the remainder
            # E.g. 5 % 3 = 2
            is_lit = (index + step) % num_steps == 0
            if is_lit:
                # Indented for the 'if', this is
                # executed if is_lit is true.
                # Set the pixel to white.
                pixels[index] = (255, 255, 255)
            else:
                # If it is not true, set the
                # pixel to off.
                pixels[index] = (0, 0, 0)
        # After we have set if each pixel should be
        # on or off we send this to the pixels.
        pixels.show()
        # Then wait for a delay until we draw the
        # next step of the pattern.
        time.sleep(0.25)

# This is the end of the theatre pattern.

# This function draws bands of colours which move
# along the strip.
# The parameter 'num_in_band' is the number
# of pixels wide each band is.
def bands(num_in_band):
    # Each band needs to move by it's full width,
    # so the number of steps in the pattern is
    # equal to the number of pixels in each band.
    # So we create a loop of this size.
    for step in range(num_in_band*2):
        # Now we loop over each pixel determining
        # which colour it should be.
        for index in range(num_pixels):
            # Colour is true for the first colour
            # or false for the second colour
            colour = ((index + step) // num_in_band) % 2 == 0
            #colour = ((index // num_in_band) + step) % 2 == 0
            # 0 = 0/5
            if colour:
                # Set the pixel to the first colour, which
                # here is red
                pixels[index] = (255, 0, 0)
            else:
                # Set the pixel to the second colour, green.
                pixels[index] = (0, 255, 0)

        # Again show the pixels and wait before
        # drawing the next step of the pattern.
        pixels.show()
        time.sleep(0.1)

# This is the end of the bands pattern.

# This function provides a colour wheel, taking a
# value from 0-255 it will output a colour that
# smoothly changes between red, green and blue
# and then back to red.
def wheel(pos):
    if pos < 85:
        r = pos * 3
        g = 255 - pos * 3
        b = 0
    elif pos < 170:
        pos -= 85
        r = 255 - pos * 3
        g = 0
        b = pos * 3
    else:
        pos -= 170
        r = 0
        g = pos * 3
        b = 255 - pos * 3
    return (r, g, b)

# This function draws a rainbow effect along the strip
# using the function above to fade smoothly between colours.
def rainbow():
    # The pattern has 255 steps, so create a loop for this
    # many times
    for step in range(255):
        # Now we want to determine the colour for each
        # pixel, so we loop over every pixel.
        for index in range(num_pixels):
            # This creates the index in the pattern,
            # dividing by 'num_pixels' so that the rainbow
            # extends along the whole strip.
            # 'step' is added so that the colours 'move'
            # along the strip.
            pattern_index = (index * 256 // num_pixels) + step

            # Set the pixel at 'index' to the colour
            # determined by the function above. The pattern
            # index is used modulo 256, which ensures it
            # is in the range 0 to 255 as required by
            # the 'wheel' function.
            pixels[index] = wheel(pattern_index % 256)

        # Now we display this step of the pattern
        pixels.show()

        # And wait a bit before drawing the next step
        time.sleep(0.01)

# This is the end of the rainbow pattern.

# This pattern creates a number of fully lit pixels that
# move along the strip with a gradually fading tail.
# The parameter 'colours' is a list of colours of the lit
# pixels.
def tracer(colours):
    for step in range(num_pixels):
        # Set all pixels off
        pixels.fill((0, 0, 0))
        # Loop over each colour
        for i, colour in enumerate(colours):
            # Get the position of the lit pixel
            start = (((num_pixels // len(colours)) * i) + step) % num_pixels
            pixels[start] = colour

            # Draw the tail
            tail_len = 25 // len(colours)
            for t in range(tail_len):
                pos = (start - (t + 1)) % num_pixels
                r = colour[0] - 100 - ((255 // tail_len) * t)
                g = colour[1] - 100 - ((255 // tail_len) * t)
                b = colour[2] - 100 - ((255 // tail_len) * t)
                if r < 0: r = 0
                if g < 0: g = 0
                if b < 0: b = 0
                pixels[pos] = (r, g, b)
        # Show and wait
        pixels.show()
        time.sleep(0.1)
# This is the end of the tracer function.

# This function twinkles random pixels on and off.
# It's a bit involved so I haven't documented it in detail.
to_light = []
to_drop = []
lit = []
processing = []
twinkle_colours = {}

def twinkle():
    global to_light, to_drop, lit, processing, twinkle_colours

    if len(processing) < 20:
        tolightid = random.randrange(num_pixels)
        if tolightid not in processing:
            to_light.append([tolightid, 0])
            processing.append(tolightid)
            twinkle_colours[tolightid] = (random.randrange(255), random.randrange(255), random.randrange(255))

    if len(lit) >= 10:
        random.shuffle(lit)
        id = lit.pop()
        to_drop.append([id, 250])

    for i in range(len(to_drop)):
        e = to_drop[i]
        e[1] = e[1] - 25
        colour = twinkle_colours[e[0]]
        r = ((e[1] * colour[0]) // 255) & 255
        g = ((e[1] * colour[1]) // 255) & 255
        b = ((e[1] * colour[2]) // 255) & 255
        pixels[e[0]] = (r, g, b)
        if e[1] != 0:
            to_drop[i] = e
        else:
            processing.remove(e[0])
    to_drop = [e for e in to_drop if e[1] != 0]

    for i in range(len(to_light)):
        e = to_light[i]
        e[1] = e[1] + 25
        colour = twinkle_colours[e[0]]
        r = ((e[1] * colour[0]) // 255) & 255
        g = ((e[1] * colour[1]) // 255) & 255
        b = ((e[1] * colour[2]) // 255) & 255
        pixels[e[0]] = (r, g, b)
        if e[1] >= 250:
            lit.append(e[0])
        else:
            to_light[i] = e
    to_light = [e for e in to_light if e[1] < 250]

    pixels.show()
    time.sleep(0.05)
# This is the end of the twinkle function

########################
# Setup button presses #
########################

# Index of the current pattern, starting at 0. This
# will increase by one if the button is pressed.
current_pattern = 0
increment_pattern = False
last_press_time = time.time()

# This function will be called when the button is
# pressed.
# Check if the button has been pressed in the last
# half a second, and if not, increment the pattern.
def on_press(channel):
    global increment_pattern, last_press_time
    now = time.time()
    if (now - last_press_time) > 0.5:
        increment_pattern = True
        last_press_time = now

#GPIO.setwarnings(False)
# This sets up pin 24 (the pin the button is connected to)
# as an input and says to call the 'on_press' function
# when it is pressed.
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24,GPIO.RISING,callback=on_press)

#####################
# Running a pattern #
#####################

# This section is the code that is actually executed when the
# program is run.
# Previously we defined some functions, but until a function
# is called it doesn't do anything.

# This is also a loop similar to 'for' but one that is executed
# until a condition is false.
# The condition here is 'True' and so it will never become false
# which means the loop will run forever.
# This is what we want as we want the patterns to keep repeating.
try:
    while True:
        if current_pattern == 0:
            # Draw the 'fixed_colour' pattern with a red colour.
            # The arguement to the function is a vector of red, green
            # and blue elements.
            # E.g. Red is '[255, 0, 0]'
            colour = app_colour
            # Call the function with the colour we set
            fixed_colour(colour)
        elif current_pattern == 1:
            wipe()
        elif current_pattern == 2:
            theatre()
        elif current_pattern == 3:
            bands(5)
        elif current_pattern == 4:
            rainbow()
        elif current_pattern == 5:
            colours = [
                (255, 255, 255),
                (255, 255, 255)
            ]
            tracer(colours)
        elif current_pattern == 6:
            colours = [
                (255, 0, 0),
                (0, 255, 0),
                (255, 0, 0),
                (0, 255, 0)
            ]
            tracer(colours)
        elif current_pattern == 7:
            twinkle()
        else:
            # Gone past the end of the patterns so we reset the
            # index to zero to start again at the first pattern.
            current_pattern = 0

        if increment_pattern:
            current_pattern += 1
            increment_pattern = False
            pixels.fill((0, 0, 0))
except:
    s.shutdown()
