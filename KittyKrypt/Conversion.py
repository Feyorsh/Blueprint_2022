import PIL import Image

def convertToPPM(file):
    im = Image.open(file)
    im.save("da_cat.ppm")