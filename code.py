# Minimal example displaying an image tiled across multiple RGB LED matrices.
# This is written for MatrixPortal and four 64x32 pixel matrices, but could
# be adapted to different boards and matrix combinations.
# No additional libraries required, just uses displayio.
# Image wales.bmp should be in CIRCUITPY root directory.

import board
import displayio
import framebufferio
import rgbmatrix
from digitalio import DigitalInOut, Direction
import time

# -----------------
# Initial pin setup
# -----------------

bit_depth_value = 6
base_width = 64
base_height = 32
chain_across = 1
tile_down = 1
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down

displayio.release_displays() # Release current display, we'll create our own

# setup GPIO pins for the matrix
R1 = DigitalInOut(board.GP2)
G1 = DigitalInOut(board.GP3)
B1 = DigitalInOut(board.GP4)
R2 = DigitalInOut(board.GP5)
G2 = DigitalInOut(board.GP8)
B2 = DigitalInOut(board.GP9)
CLK = DigitalInOut(board.GP11)
STB = DigitalInOut(board.GP12)
OE = DigitalInOut(board.GP13)

R1.direction = Direction.OUTPUT
G1.direction = Direction.OUTPUT
B1.direction = Direction.OUTPUT
R2.direction = Direction.OUTPUT
G2.direction = Direction.OUTPUT
B2.direction = Direction.OUTPUT
CLK.direction = Direction.OUTPUT
STB.direction = Direction.OUTPUT
OE.direction = Direction.OUTPUT

OE.value = True
STB.value = False
CLK.value = False

MaxLed = 64

c12 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
c13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c12[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 12):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c13[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 13):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

R1.deinit()
G1.deinit()
B1.deinit()
R2.deinit()
G2.deinit()
B2.deinit()
CLK.deinit()
STB.deinit()
OE.deinit()

# ------------------------------
# RGBMatrix Setup
# ------------------------------

# RGB Matrix creation
matrix = rgbmatrix.RGBMatrix(
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=tile_down, serpentine=serpentine_value,
    doublebuffer=True)

# Associate matrix with a Display object
DISPLAY = framebufferio.FramebufferDisplay(matrix, auto_refresh=False, rotation=180)

# -----------------------------------
# Load Image and Set Up Display Group
# -----------------------------------

# Load BMP image, create Group and TileGrid to hold it
# BITMAP = displayio.OnDiskBitmap(open('uidahologo_resized.bmp', 'rb'))
BITMAP = displayio.OnDiskBitmap(open('joevandal_resized.bmp', 'rb'))

GROUP_on = displayio.Group()
tile_grid = displayio.TileGrid(
    BITMAP,
    pixel_shader=displayio.ColorConverter(),
    width=1,
    height=1,
    tile_width=BITMAP.width,
    tile_height=BITMAP.height,
    x=(64 - BITMAP.width) // 2,
    y=(32 - BITMAP.height) // 2
)
GROUP_on.append(tile_grid)

# ------------------------------
# Display Static Image
# ------------------------------

# Show the image
DISPLAY.show(GROUP_on)


# Refresh the display to ensure the image is rendered
DISPLAY.refresh()

# Keep the display static
while True:
    pass


# Create an empty group for the "off" state
GROUP_off = displayio.Group()

# ------------------------------
# Toggle the Image Every 3 Seconds
# ------------------------------

# # Set interval for toggling the image (3 seconds on, 3 seconds off)
# toggle_interval = 3.0  # 3 seconds for each "on" or "off" state

# # Initial timing setup
# next_toggle_time = time.monotonic()
# show_image = True  # Track if the image should be visible or not

# # Animation loop to toggle the image every 3 seconds
# while True:
#     current_time = time.monotonic()

#     # Toggle the image visibility every toggle_interval
#     if current_time >= next_toggle_time:
#         show_image = not show_image  # Toggle visibility state
#         next_toggle_time = current_time + toggle_interval

#         # Show the image or the empty group based on the toggle state
#         if show_image:
#             DISPLAY.show(GROUP_on)  # Show the image
#         else:
#             DISPLAY.show(GROUP_off)  # Show the empty group (off state)

#     # Refresh the display to maintain updates
#     DISPLAY.refresh(target_frames_per_second=50, minimum_frames_per_second=0)

# ------------------------------
# Flicker the Image
# ------------------------------

# Flicker frequency to 20 Hz (25 ms per state)
# flicker_interval = 1  / (20 * 2)  # 20hz aka 0.025 seconds or 25 ms for each "on" or "off" state

# Initial timing setup
# next_flicker_time = time.monotonic()
# show_image = True  # Track if the image should be visible or not

# # Animation loop to flicker the image at 20 Hz
# while True:
#     current_time = time.monotonic()

#     # Toggle the image visibility every flicker_interval
#     if current_time >= next_flicker_time:
#         show_image = not show_image  # Toggle visibility state
#         next_flicker_time = current_time + flicker_interval

#         # Show or hide the group based on the toggle state
#         if show_image:
#             DISPLAY.show(GROUP_on)  # Show the image
#         else:
#             DISPLAY.show(GROUP_off)  # Hide the image

#     # Refresh the display to maintain updates
#     DISPLAY.refresh(target_frames_per_second=50, minimum_frames_per_second=0)