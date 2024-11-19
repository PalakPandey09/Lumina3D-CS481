import tkinter as tk
from tkinter import messagebox
import time
import threading
import board
import displayio
import framebufferio
import rgbmatrix
from digitalio import DigitalInOut, Direction

# Associate matrix with a Display object
DISPLAY = framebufferio.FramebufferDisplay(matrix, auto_refresh=False, rotation=180)

# -----------------------------------
# Load Image and Set Up Display Group
# -----------------------------------

# Load BMP image, create Group and TileGrid to hold it
BITMAP = displayio.OnDiskBitmap(open('uidahologo_resized.bmp', 'rb'))
# BITMAP = displayio.OnDiskBitmap(open('joevandal_resized.bmp', 'rb'))

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

# Create an empty group for the "off" state
GROUP_off = displayio.Group()

def flicker_display():
    messagebox.showinfo("Flicker", "Flicker mode activated!")
    # Flicker frequency to 20 Hz (25 ms per state)
    flicker_interval = 1  / (20 * 2)  # 20hz aka 0.025 seconds or 25 ms for each "on" or "off" state

    # Initial timing setup
    next_flicker_time = time.monotonic()
    show_image = True  # Track if the image should be visible or not

    # Animation loop to flicker the image at 20 Hz
    while True:
        current_time = time.monotonic()

        # Toggle the image visibility every flicker_interval
        if current_time >= next_flicker_time:
            show_image = not show_image  # Toggle visibility state
            next_flicker_time = current_time + flicker_interval

            # Show or hide the group based on the toggle state
            if show_image:
                DISPLAY.show(GROUP_on)  # Show the image
            else:
                DISPLAY.show(GROUP_off)  # Hide the image

        # Refresh the display to maintain updates
        DISPLAY.refresh(target_frames_per_second=50, minimum_frames_per_second=0)

def toggle_display():
    messagebox.showinfo("Toggle", "Toggle mode activated!")
    # Set interval for toggling the image (3 seconds on, 3 seconds off)
    toggle_interval = 3.0  # 3 seconds for each "on" or "off" state

    # Initial timing setup
    next_toggle_time = time.monotonic()
    show_image = True  # Track if the image should be visible or not

    # Animation loop to toggle the image every 3 seconds
    while True:
        current_time = time.monotonic()

        # Toggle the image visibility every toggle_interval
        if current_time >= next_toggle_time:
            show_image = not show_image  # Toggle visibility state
            next_toggle_time = current_time + toggle_interval

            # Show the image or the empty group based on the toggle state
            if show_image:
                DISPLAY.show(GROUP_on)  # Show the image
            else:
                DISPLAY.show(GROUP_off)  # Show the empty group (off state)

        # Refresh the display to maintain updates
        DISPLAY.refresh(target_frames_per_second=50, minimum_frames_per_second=0)

def static_display():
    messagebox.showinfo("Static", "Static mode activated!")
    # Place your static display code here

# Function to handle threading for display modes
def run_display_mode(mode_function):
    thread = threading.Thread(target=mode_function)
    thread.daemon = True  # Allows the program to exit even if thread is running
    thread.start()

# Set up the GUI window
root = tk.Tk()
root.title("LED Board Control Panel")
root.geometry("300x200")

# Create buttons for each display mode
flicker_button = tk.Button(root, text="Flicker Mode", command=lambda: run_display_mode(flicker_display))
flicker_button.pack(pady=10)

toggle_button = tk.Button(root, text="Toggle Mode", command=lambda: run_display_mode(toggle_display))
toggle_button.pack(pady=10)

static_button = tk.Button(root, text="Static Mode", command=lambda: run_display_mode(static_display))
static_button.pack(pady=10)

# Run the GUI loop
root.mainloop()
