# Pixel Art Editor

## Overview
This Pixel Art Editor is a simple tool designed for creating pixel art images. It allows users to draw and modify images pixel by pixel, with a variety of tools and features to enhance the creative process.

The project focuses on implementing object-oriented coding skills as well as array handling.

## Features
- Drawing: Users can draw pixel art images using a selected color and brush size.
- Color Palette: Choose from a selection of colors to use while drawing.
- Zoom: Zoom In and Out of the canvas to work on finer details or get an overview of the entire image.
- Transformation Tools: Rotate, mirror, and apply various transformations to the image.
- Shape Drawing: Quickly draw squares and rhombuses onto the canvas.
- High Contrast and Negative Effects: Apply special effects to the entire image.
- Edge Display: Toggle the display of grid edges for better visualization.
- ASCII Art Rendering: View the image as ASCII art.
- Save and Open Files: Save and load pixel art images in .txt format.

# Requirements 
- Python Version : 3.12.2 64-bit
- Pygame
- Screeninfo
- Tkinter.filedialog

## Shortcuts and Key Functions
The Pixel Art Editor provides several keyboard shortcuts to enhance your editing experience. Here's a summary of the key sequences and their corresponding functions:

| Key Sequence | Function |
| ------------ | -------- |
| Arrow Keys   | Move the canvas view. |
| Mouse Scroll | Zoom In and Out. |
| Left Click   | Draw pixels on the canvas. |
| Right Click  | Select eraser. |
| Number Keys (0-9) | Change the current drawing color. |
| Ctrl + Plus (+) | Zoom in. |
| Ctrl + Minus (-) | Zoom out. |
| Ctrl + SPACE  | Cover / Erase all canvas. |
| Ctrl + Z      | Undo changes. |
| Ctrl + S      | Save the current image. |
| Ctrl + O      | Open a new image file. |

## Additional Notes
It's worth noting that loading a .txt file requires a specific format.

Additionally, please consider that the resolution of the canvas can impact the software's performance. Higher resolutions may lead to slower response times, whereas lower resolutions may result in faster editing speeds. Adjusting the canvas resolution according to your preferences and system capabilities can optimize your editing experience.

By default, new documents will have a resolution of 12x12. However, this can be manually changed by modifying the corresponding .txt file.