'''
In this program we try to hide a text inside an image using steganography
Here we code the algorithm for steganography from scratch using Python 3.6 or
    above
Steganography is a technique of hiding information behind the scene. It’s is
    not like cryptography which focuses on encrypting data(through different
    algorithms like SHA1, MD5 etc), steganography focuses more on hiding the
    data (data can be a file, image, message or video) within another file,
    image, message or video to avoid any attraction.

Encode the data in odds and evens :

Every byte of data is converted to its 8-bit binary code using ASCII values.
Now pixels are read from left to right in a group of 3 containing a total of
    9 values.
The first 8-values are used to store the binary data.
The value is made odd, if 1 occurs and even, if 0 occurs.
'''


__author__ = ["Rishit Dagli", ]
__copyright__ = ""
__credits__ = ["Rishit Dagli", ]
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Rishit Dagli"
__email__ = "rishit.dagli@gmail.com"
__status__ = "Development"

# We will use PIL module is used to extract pixels of image and modify it as
#    required
from PIL import Image

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):
    '''
    @author Rishit Dagli
    Convert the data by encoding it into 8-bit binary format
    So, use the ASCII value of characters
    '''

    newd = []
#   Make a list called new data

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    '''
    @author Rishit dagli
    This our most important function and we will do all the computation part
        here
    Modify the pixels according to 8-bit binary data and return them
    '''

#   First we of course need to encode it
    datalist = genData(data)

    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extract 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                  imdata.__next__()[:3] +
                                  imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
#           We only need to check 8 pixels

            if (datalist[i][j]=='0') and (pix[j]% 2 != 0):
#               Thsi is the logic we discussed being even or odd

                if (pix[j]% 2 != 0):
                    pix[j] -= 1

                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

#       8 th pixel of every set tells  whether to stop ot read further.
#       As we defined earlier:
#       0 means keep reading, 1 means the message is over.

        if (i == lendata - 1):
            # Our last pixel row

            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    '''
    @author Rishit Dagli
    In this function we change the pixels of image for all characters
    Using the 'modPix' function we made earlier
    '''

    w = newimg.size[0]

#   Initialise x and y as 0, 0
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encodeText():
    '''
    @author Rishit dagli
    Finally encode the data into an image
    '''

    img = input("Enter image name: ")
    print()

#   Here we will use PIL module to open the image and extract pixels
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded : ")
    print()

    if (len(data) == 0):

#       If user does not enter anything
        raise ValueError('Data is empty')

#   make a new image where we will apply our algorithm
#   PIL comes to our rescue
    newimg = image.copy()

    encode_enc(newimg, data)

    new_img_name = input("Enter the name of new image: ")

# Finally save the new Image
# Again PIL helps us
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

    print("Image stored: " + new_img_name)

def decode():
    '''
    @author Rishit Dagli
    We read 3 pixels at a time and use the same logic to decode an image
    '''

    img = input("Enter image name :")
    print()
    image = Image.open(img, 'r')

    data = ''

#   Get the image pixel data PIL again
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3] +
                                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
#           8 pixels at a time
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))

        if (pixels[-1] % 2 != 0):
#           This implies we do not have any more data
            return data

def main():
    '''
    @author Rishit Dagli
    The main function
    '''

    print("1 to encode")
    print("2 to decode")

    a=int(input())

    if (a == 1):
        encodeText()

    elif (a == 2):
        print("Decoded word is " + decode())

    else:
        raise Exception("Enter correct input")

if __name__ == '__main__' :

    main()

'''
print("functions- main, genData, modPix, encode_enc, encodeText, decode")
print("Docs")
print(main.__doc__)
print(genData.__doc__)
print(modPix.__doc__)
print(encode_enc.__doc__)
print(encodeText.__doc__)
print(decode.__doc__)
'''
