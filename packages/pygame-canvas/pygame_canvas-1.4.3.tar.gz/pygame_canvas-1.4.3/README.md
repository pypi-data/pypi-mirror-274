Canvas
Canvas is a Python module built on top of Pygame, designed to simplify the creation of interactive applications and games. It provides a set of functions and classes for managing graphical elements, handling user input, and implementing game logic.

Features
Window Management: Create resizable windows with customizable properties such as title, size, and icon.
Event Handling: Capture user input events like mouse clicks, keyboard presses, and window resizing.
Sprite Management: Define and manipulate sprites with properties like position, scale, rotation, and collision detection.
Text Rendering: Render text with customizable fonts, sizes, colors, and antialiasing options.
Sound Playback: Play sounds with adjustable volume and manage sound effects associated with sprites.
Physics Simulation: Implement basic physics interactions such as collision resolution and object movement.
Usage
Installation
To use Canvas, you'll need Python installed on your system along with the Pygame library. You can install Pygame using pip:


pip install pygame

Example Usage
Here's a simple example demonstrating how to use Canvas to create a window and display a sprite:

import canvas as c

# Initialize window
c.window(title="My Game")

# Create sprite
sprite = c.sprite(images=[c.rectangle(50, 50, (0, 200, 255))], pos=(240, 180))

# Main game loop
while c.loop(60):
    # Update game logic here
    pass

Documentation
For detailed documentation and usage examples, refer to the Canvas documentation at: https://docs.google.com/document/d/18SMSY5RbigaOX2WOaGQs0iEUvSFnpfpWjsBxBNwq0nA/edit?usp=sharing.