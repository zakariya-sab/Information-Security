from PIL import Image

with open("recovered.raw", "rb") as f:
    pixels = f.read()

print("Number of bytes:", len(pixels))

image = Image.frombytes("L", (432, 475), pixels)
image.save("recovered.png")