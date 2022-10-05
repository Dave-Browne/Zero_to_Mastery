from PIL import Image, ImageFilter

img1 = Image.open('./pikachu.jpeg')
img2 = Image.open('./Dave.jpeg')

filtered_img1 = img2.filter(ImageFilter.CONTOUR)
filtered_img2 = img2.filter(ImageFilter.EMBOSS)

new_img = img2.copy()
new_img.thumbnail((400, 400))
print(new_img.size)
new_img.show()

