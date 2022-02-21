from Crypto.Cipher import AES
import requests
import json
from PIL import Image

def encryptFile(file, key):
    # match for different encryption schemes
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce

    with open(file, 'rb') as f:
        ciphertext, tag = cipher.encrypt_and_digest(f.read())
    return ciphertext + b'\xff\xff\xff\xff\xff' + nonce

def decryptFile(file, key, nonce):
    with open(file, 'rb') as f:
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(f.read())

def keyFromCat(file):
    with open(file, 'rb') as f:
        contents = f.read() # num pixels * 3 + 4

        #(width, height) = [int(i) for i in contents[2].split(" ")]
        #assert(int(contents[3]) == 255)
        #max_length = width*height-20

        # we need key length
        # we'll start from rc4, that seems the easiest to implement
        # let's say keys can be 1000 somethings long, so +-5 on each rgb value

        lenny = (int(contents[50]) % 10) * 100 + (int(contents[51]) % 10) * 10 + (int(contents[52]) % 10)
        #assert(max_length > lenny)
        #print(f"Max length: {max_length}, actual length: {lenny}")

        #key_in_int = [int("0o" + str(int(contents[i]) % 8) + str(int(contents[i+1]) % 8) + str(int(contents[i+2]) % 8), base=8) for i in range(7, 7+lenny*3, 3)]
        key_in_int = [int(contents[i]) % 16 for i in range(53, lenny+53)]
        if (t := len(key_in_int)) < 16:
            ValueError("try a bigger image")
        elif t < 24:
            return bytes(key_in_int[:16])
        elif t < 24:
            return bytes(key_in_int[:24])
        else:
            return bytes(key_in_int[:32])

def applyKeyToCat(key, file): # never implemented...
    pass


def getRandomCat():
    while True:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        js = json.loads(response.text)
        if js[0]['url'][-4:] == ".gif":
            continue
        return (js[0]['url'][-4:], requests.get(js[0]['url']).content)

def convertToPPM(file):
    im = Image.open(file)
    im.save(file[:-4]+".ppm")
    

if __name__ == "__main__":
    keyFromCat("Cat.ppm")