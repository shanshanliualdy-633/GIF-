import argparse
from PIL import Image
import math
import os

def convert_gif_to_sprite_sheet(gif_path, output_path=None, columns=None, horizontal=False):
    """
    Converts a GIF file to a sprite sheet image.
    
    Args:
        gif_path (str): Path to the input GIF file.
        output_path (str, optional): Path to save the output sprite sheet. 
                                     Defaults to [gif_name]_sheet.png.
        columns (int, optional): Number of columns in the sprite sheet. 
                                 If None, calculates a square-ish grid.
        horizontal (bool, optional): If True, arranges all frames in a single row.
                                     Overrides columns.
    """
    try:
        gif = Image.open(gif_path)
    except IOError:
        print(f"Error: Could not open {gif_path}")
        return

    frames = []
    try:
        while True:
            # Copy the frame to avoid issues when seeking
            frames.append(gif.copy())
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    frame_count = len(frames)
    if frame_count == 0:
        print("Error: No frames found in GIF.")
        return

    frame_width, frame_height = frames[0].size
    print(f"Found {frame_count} frames. Top-left frame size: {frame_width}x{frame_height}")

    if horizontal:
        columns = frame_count
    elif columns is None:
        columns = math.ceil(math.sqrt(frame_count))
    
    rows = math.ceil(frame_count / columns)
    
    sheet_width = columns * frame_width
    sheet_height = rows * frame_height
    
    sprite_sheet = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))
    
    for i, frame in enumerate(frames):
        col = i % columns
        row = i // columns
        x = col * frame_width
        y = row * frame_height
        
        # Handle transparency and different modes
        if frame.mode != 'RGBA':
            frame = frame.convert('RGBA')
            
        sprite_sheet.paste(frame, (x, y))

    if output_path is None:
        base_name = os.path.splitext(gif_path)[0]
        output_path = f"{base_name}_sheet.png"

    sprite_sheet.save(output_path)
    print(f"Sprite sheet saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert GIF to Sprite Sheet")
    parser.add_argument("input", help="Input GIF file path")
    parser.add_argument("-o", "--output", help="Output Sprite Sheet file path")
    parser.add_argument("-c", "--columns", type=int, help="Number of columns in sprite sheet")
    parser.add_argument("-H", "--horizontal", action="store_true", help="Arrange frames in a single row")

    args = parser.parse_args()
    
    convert_gif_to_sprite_sheet(args.input, args.output, args.columns, args.horizontal)
