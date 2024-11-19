from machine import Pin
from neopixel import NeoPixel
import time

# Configuration
PIN = 28  # The GPIO pin connected to the LED panel data line
WIDTH = 64  # Width of the LED panel
HEIGHT = 32  # Height of the LED panel
NUM_PIXELS = WIDTH * HEIGHT

# Initialize the NeoPixel object
np = NeoPixel(Pin(PIN, Pin.OUT), NUM_PIXELS)

# Colors
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# Define the "I" pattern for 32x64 panel
I_PATTERN = [
    [0] * WIDTH for _ in range(HEIGHT)
]

# Create the "I" shape
for y in range(HEIGHT):
    for x in range(WIDTH):
        # Main vertical part of "I"
        if 28 <= x < 36 and 6 <= y < 26:
            I_PATTERN[y][x] = 1
        # Top horizontal part of "I"
        elif 24 <= x < 40 and 6 <= y < 10:
            I_PATTERN[y][x] = 1
        # Bottom horizontal part of "I"
        elif 24 <= x < 40 and 22 <= y < 26:
            I_PATTERN[y][x] = 1

def set_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        np[y * WIDTH + x] = color

def display_pattern(pattern, color):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if pattern[y][x]:
                set_pixel(x, y, color)
            else:
                set_pixel(x, y, BLACK)
    np.write()

# Main loop
while True:
    # Display the golden "I"
    display_pattern(I_PATTERN, GOLD)
    time.sleep(2)
    
    # Clear the display
    np.fill(BLACK)
    np.write()
    time.sleep(1)
