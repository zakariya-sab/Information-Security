from PIL import Image
shades = {} 
pixels = [] # encrypted block → chosen shade
with open("classified.enc", "rb") as f:
    data = f.read()

width = 432
height = 475

# Skip the header and keep only the image blocks, excluding padding.
ciphertext = data[16:16 + width * height]
for i  in range(0 , len(ciphertext),16):
    block = ciphertext[i:16+i]
    if block not in shades:
        shades[block] = (len(shades) * 73) % 256
    shade = shades[block]   
    pixels.extend([shade] * 16)

image = Image.new("L", (width, height))
image.putdata(pixels)
image.save("pattern_ecb.png")
total_blocks = len(ciphertext) // 16
unique_blocks = len(shades)

print("Total blocks:", total_blocks)
print("Unique blocks:", unique_blocks)
print("Repeated occurrences:", total_blocks - unique_blocks)