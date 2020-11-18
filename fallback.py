# Fallback program to indicate an error
import time
import board
import neopixel

pixel_pin = board.D18
num_pixels = 10
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1,
                           auto_write=False, pixel_order=neopixel.GRB)

while True:
    for val in range(25):
      for index in range(num_pixels):
          pixels[index] = (val*10, 0, 0)
      pixels.show()
      time.sleep(0.01)
    for val in range(25):
      for index in range(num_pixels):
          pixels[index] = (250 - val*10, 0, 0)
      pixels.show()
      time.sleep(0.01)
