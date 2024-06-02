# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 20:33:16 2024

@author: Morteza
"""

import cv2
import numpy as np
import random
import time

# Function to generate random stars
def generate_stars(img, num_stars):
    height, width = img.shape[:2]
    stars = []
    num_stars_always_on = num_stars // 3  # One-third of stars always on
    for _ in range(num_stars):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        size = random.randint(1, 3)
        brightness = random.randint(100, 255)
        if num_stars_always_on > 0:
            state = True
            num_stars_always_on -= 1
        else:
            state = random.choice([True, False])  # Randomly assign state (on/off)
        stars.append((x, y, size, brightness, state))
    return stars

# Function to randomly turn on/off stars
def toggle_stars(stars):
    num_to_toggle = 2 * len(stars) // 3  # Two-thirds of stars to toggle
    for _ in range(num_to_toggle):
        index = random.randint(0, len(stars) - 1)
        x, y, size, brightness, state = stars[index]
        brightness = 0 if state else random.randint(100, 255)
        stars[index] = (x, y, size, brightness, not state)

# Function to generate random meteors
def generate_meteor(img, num_meteors):
    height, width = img.shape[:2]
    for _ in range(num_meteors):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        length = random.randint(10, 50)
        angle = random.uniform(0, 2*np.pi)
        end_x = int(x + length * np.cos(angle))
        end_y = int(y + length * np.sin(angle))
        brightness = random.randint(150, 255)
        cv2.line(img, (x, y), (end_x, end_y), (brightness, brightness, brightness), 2)

# Main function to create the night sky simulation
def main():
    width, height = 1920, 1080  # Larger image size
    num_stars = 1000  # Increased number of stars
    num_meteors = 4  # Increased number of meteors

    # Create a black canvas
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # Generate stars
    stars = generate_stars(canvas, num_stars)

    while True:
        canvas.fill(0)  # Reset canvas to black

        # Toggle stars on/off
        toggle_stars(stars)

        # Draw stars on canvas
        for x, y, size, brightness, state in stars:
            if state:
                cv2.circle(canvas, (x, y), size, (brightness, brightness, brightness), -1)

        # Generate meteors
        generate_meteor(canvas, num_meteors)

        # Show the night sky
        cv2.imshow('Night Sky', canvas)

        # Check for user input to exit
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
