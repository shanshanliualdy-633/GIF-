from PIL import Image, ImageDraw

def create_test_gif(filename="test.gif"):
    frames = []
    for i in range(5):
        img = Image.new('RGB', (100, 100), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((10, 10), f"Frame {i}", fill=(0, 0, 0))
        frames.append(img)
    
    frames[0].save(filename, save_all=True, append_images=frames[1:], duration=100, loop=0)
    print(f"Created {filename}")

if __name__ == "__main__":
    create_test_gif()
