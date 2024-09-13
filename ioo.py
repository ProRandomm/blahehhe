import tkinter as tk
from PIL import ImageGrab
import requests
from threading import Thread
from fastapi import FastAPI
import uvicorn
import time

# Emoji color mappings
emoji_colors = {
    "🖤": (0, 0, 0),
    "🤍": (255, 255, 255),
    "🍒": (128, 0, 0),
    "❤️": (255, 0, 0),
    "💜": (128, 0, 128),
    "🌸": (255, 0, 255),
    "🌳": (0, 128, 0),
    "📗": (0, 255, 0),
    "🦖": (128, 128, 0),
    "🍋": (255, 255, 0),
    "🔵": (0, 0, 128),
    "📘": (0, 0, 255),
    "🧪": (0, 128, 128),
    "🐋": (0, 255, 255),
}

app = FastAPI()

# Global variable for storing emoji text
current_text = ""

# Function to calculate closest emoji based on pixel color
def get_closest_emoji(r, g, b):
    closest_emoji = None
    smallest_distance = float('inf')
    
    for emoji, (er, eg, eb) in emoji_colors.items():
        distance = ((r - er) ** 2 + (g - eg) ** 2 + (b - eb) ** 2) ** 0.5
        if distance < smallest_distance:
            smallest_distance = distance
            closest_emoji = emoji

    return closest_emoji

# Function to process the screen and convert pixels to emoji
def update_screen_colors():
    global current_text
    while True:
        screenshot = ImageGrab.grab()
        screen_width, screen_height = screenshot.size

        # Define the resolution of the output (higher resolution for better quality)
        num_columns = 120  # Number of columns of emojis
        num_rows = 60      # Number of rows of emojis

        emoji_width = screen_width // num_columns
        emoji_height = screen_height // num_rows

        current_text = ""
        for y in range(num_rows):
            for x in range(num_columns):
                # Calculate the position in the screenshot
                px = x * emoji_width + (emoji_width // 2)
                py = y * emoji_height + (emoji_height // 2)
                
                # Get the color of the pixel in the center of the emoji area
                r, g, b = screenshot.getpixel((px, py))
                emoji = get_closest_emoji(r, g, b)
                current_text += emoji
            current_text += "\n"

        time.sleep(1 / 30)  # Update at approximately 30 FPS

# Endpoint to serve the emoji text
@app.get("/get_text")
def get_text():
    return {"text": current_text}

# Start screen processing in a separate thread
if __name__ == "__main__":
    screen_thread = Thread(target=update_screen_colors)
    screen_thread.start()
    uvicorn.run(app, host="127.0.0.1", port=8002)
