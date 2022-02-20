from PIL import Image

def convertToPPM(file):
    im = Image.open(file)
    im.save(file[:-4]+".ppm")