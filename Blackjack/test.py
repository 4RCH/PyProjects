import math

from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from fractions import Fraction

argsList =[]

def addStuff(*args):
    for i in args:
        argsList.append(i)
    print (argsList)
    totalAdded = 0
    del i
    for i in range(0,len(argsList)):
        totalAdded = argsList[i] + totalAdded
    return totalAdded

def inputFraction():
    try:
        frC = Fraction(input("Enter a fraction: \n"))
        floatC = float(frC)
        print (floatC)
    except ZeroDivisionError:
        print ("your fraction is a division by zero")
    except ValueError:
        print ("That\'s not a fraction...")

def inputFloat():
    try:
        gNum = float(input("Enter a floating point value: \n"))
        gNumCheck = gNum.is_integer()
        print("Is the value an Integer? ", gNumCheck)
        if gNumCheck == True:
            gNumFloat = float(gNum)
            print ("Converting to floating point", gNumFloat)
    except ValueError:
        print ("That's not a floating point value")

def quadEq(valA,valB,valC):
    a = valA
    b = valB
    c = valC

    D = (b*b - 4*a*c)**0.5
    
    x_1 = (-b + D) / (2 * a)
    x_2 = (-b - D) / (2 * a)
    return (x_1,x_2)

def mathStuff():
    
    for x in argsList:
        xarg = math.sin(x)
        print (xarg)
        
    x = list(range(0,22))
    print (x) 
    
    print (addStuff(10,20,30,18))
    #Fractions
    frA = Fraction (1,2)
    frB = Fraction (3,4)
    
    #Complex numbers
    comA = 1 + 2j
    comB = complex(3,5)
    comC = comA + comB
    
    #Formula to calculate the absolute value of a number
    comD = (comC.real ** 2 + comC.imag ** 2) ** 0.5
    
    #A python function that returns the absolute value just like the formula above
    comE = abs(comD)
    
    print (frA, frB, comA, comB)
    print (comC.conjugate())
    print (comC.real, comC.imag, comD)

 
def cardNames():
    cardNum = []
    cardNames = ["The Fool",
                 "The Magician",
                 "The high Priestess",
                 "The Empress",
                 "The Emperor",
                 "The Hierophant",
                 "The Lovers",
                 "The Chariot",
                 "Strength",
                 "The Hermit",
                 "The Wheel of Fortune",
                 "Justice",
                 "The Hanged Man",
                 "Death",
                 "Temperance",
                 "The Devil",
                 "The Tower",
                 "The Star",
                 "The Moon",
                 "The Sun",
                 "Judgement",
                 "The World"]
    
    cardNum = list(range(0,len(cardNames)+1))
    listZip = zip(cardNum,cardNames)
    cardList = list(listZip)
    for i in range(len(cardList)):
        print(cardList[i])
    
def dateToday():
    now = dt.now()
    print (now)

def slicingTest():
    aList = list(range(0,10))
    print (aList)
    
    #show everything from the initial value (left as no value declared) to the 5th value on the list
    print(aList[:5])
    #show everything from the 5th value to the end of the list in steps of 2
    print(aList[5::2])
    #show everything in the list, using a negative step (running backwards) - reversing the list (at least on the print statement, the list remains as is)
    print(aList[::-1])

def whateverExer():    
    a = int (input("value a: "))
    b = int (input("value b: "))
    aModAB = (a % b) == 0
    aModBA = (b % a) == 0
    
    if aModAB or aModBA:
        print ("Divisible")
        
    if b != 0:
        answerDiv = a / b
        print ("The division returns: {0}".format(answerDiv))
    
    namA = input("name A: ")
    namB = input("name B: ")
    namC = input("name C: ")
    
    if namA.lower == namB.lower == namC.lower:
        print("equal")
    else:
        print ("Names are not the same")


def stringRev():
    stringVal = input("Enter a string: ")
    tempStr = stringVal[::-1]
    return(stringVal,tempStr)

def isPali():
    a = stringRev()
    if a[0] == a[1]:
        print("This is a palindrome")
    else:
        print("This is NOT a palindrome")


#Shift cypher... OMFG xD
def encryptString(usrString, encShift):
    
    alphaKey = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 ")
    encString = ""
    for char in usrString:
        index = alphaKey.index(char)
        shiftIndex = (index + encShift) % len(alphaKey)
        encString += alphaKey[shiftIndex]
    return encString

def decryptString(usrString, key):
    alphaKey = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 ")
    decString = ""
    for char in usrString:
        index = alphaKey.index(char)
        shiftIndex = (index - key) % len(alphaKey)
        decString += alphaKey[shiftIndex]
    return decString


def exponentiation(a,e):
    if e == 0:
        return 1
    return exponentiation(a, (e-1)) * a


def digitSum(n):
    if n == 0:
        return 0
    return digitSum(n//10) + n % 10


def scaleImage(imageName = "TestImage.png", scaling = 200):
    x = Image.open(imageName)
    boundaries = x.getbbox()
    scale = []
    size = (boundaries[2],boundaries[3])
    for i in range(len(size)):
        n = size[i] * (scaling/100)
        scale.append(int(n))
    print (scale)
    newImage = x.resize(scale)
    newImage.save("scaled_"+ imageName)

def cropImage(imageName = "TestImage.png"):
    x = Image.open(imageName)
    newImage = x.crop((128,96,192,160))
    newImage.save("cropped_"+ imageName)

def processImage(imageName = "TestImage.png"):
    x = Image.open(imageName)
    greyImage = x.convert("L")
    newImage = greyImage.filter(ImageFilter.FIND_EDGES)
    newImage.save("edgeDetect_"+ imageName)

def invertImage(imageName = "TestImage.png"):
    x = Image.open(imageName).convert("RGB")
    newImage = ImageOps.invert(x)
    newImage.save("Negative_"+ imageName)

def cardScale(scale_value = 1):
    standard_card = (63,88)
    card_scaled = []
    for i in standard_card:
        card_scaled.append(i*scale_value)
    return card_scaled

def cube_create_verts(origin = (0.0,0.0,0.0),size = 1):
    
    vertsList = ((origin[0], origin[1], origin[2]),
                 ((origin[0] + size), origin[1], origin[2]),
                 ((origin[0] + size), (origin[1] + size), origin[2]),
                 (origin[0], (origin[1] + size), origin[2]),
                 (origin[0], origin[1], (origin[2] + size)),
                 ((origin[0] + size), origin[1], (origin[2] + size)),
                 ((origin[0] + size), (origin[1] + size), (origin[2] + size)),
                 (origin[0], (origin[1] + size), (origin[2] + size)))
    
    vertsList = centerCube(size, vertsList)
    return vertsList

def centerCube(size, vertsList, center = (0,0,0)):
    offset = size / 2
    verts_offset = ()
    offset_coord = (offset, offset, offset)
    print ("offset is:", offset_coord)
    for vert in vertsList:
        vert_newpos = tuple(map(lambda x, y: x - y, vert, offset_coord))
        verts_offset += (vert_newpos,)                                          
    return verts_offset
    
def main():
    origin_x = 0.0
    origin_y = 0.0
    origin_z = 0.0
    origin = (origin_x, origin_y, origin_z)
    
    vertList = cube_create_verts(origin, 1)
    for i in vertList:
        print(i)


if __name__ == "__main__":
    main()