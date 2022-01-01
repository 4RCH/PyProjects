# Is a factor of b
def is_factor():
    
    valA = int(input("input value a:"))
    valB = int(input("input value b:"))    
    
    if valB % valA == 0:
        return True
    else:
        return False
    
    print (is_factor(valA, valB))

#Get all factors of X
def factors():
    valA = input("Provide a value to find factors for (make it a positive integer... or else...): ")
    
    try:
        valA = float(valA)
        if valA > 0 and valA.is_integer():
            valA = int(valA)
            for i in range (1,valA+1):
                if valA % i == 0:
                    print (i)        
        else:
            print ("Enter a valid positive integer!!")
    except ValueError:
        print("that wasn't even a number")    

# Show the times table for a user provided value
def timesTable():
    
    userVal = (input("Which times table do you want to see?\n"))
    multiple = (input("to what multiple should I multiply?\n"))
    timesTable (float(userVal),int(multiple))
    
    for i in range (1,multiple+1):
        wholeVal = userVal*i
        print ("{0} x {1} = {2:.2f}".format(userVal,i,wholeVal))

# Measurement conversion Inches to Meters
def inchToMet(userVal):
    inchVal = 2.54
    valInMet = (userVal * inchVal)/100
    print ("That is {0:.4f} meters".format(valInMet))

# Measurement conversion Meters to Inches
def metToInc(userVal):
    inchVal = 2.54
    valInInch = (userVal * 100) / inchVal
    print ("That is {0:.4f} inches".format(valInInch))

# Measurement conversion Kilometers to Miles    
def kilToMile(userVal):
    milVal = 1.609
    valInMil = (userVal/milVal)
    print ("That is {0:.4f} Miles".format(valInMil))

# Measurement conversion Miles to Kilometers    
def MileToKil(userVal):
    milVal = 1.609
    valInKil = (milVal * userVal)
    print ("That is {0:.4f} Kilometers".format(valInKil))

def askLength(choice):
    choiceType = ("Inches","Meters","Miles","Kilometers")
    option = ()
    if choice == 1:
        option = (choiceType[0],choiceType[1])
    elif choice == 2:
        option = (choiceType[1],choiceType[0])
    elif choice == 3:
        option = (choiceType[3],choiceType[2])
    elif choice == 4:
        option = (choiceType[2],choiceType[3])
        
    userVal = (input("Length in {0} to transform to {1}: ".format(option[0],option[1])))
    return userVal

# Measurement conversion menu
def measureConvert():
    print ("Choose a conversion from the following:\n",
           "1 - Inches to Meters\n",
           "2 - Meters to Inches\n",
           "3 - Kilometers to Miles\n",
           "4 - Miles to Kilometers")
    userchoice = int(input())    
    userVal = askLength(userchoice)
    
    if userchoice == 1:
        inchToMet(float(userVal))
    
    elif userchoice == 2:
        metToInc (float(userVal))
    
    elif userchoice == 3:    
        kilToMile (float(userVal))
        
    elif userchoice == 4:
        MileToKil (float(userVal))
    else:
        print("Not a valid choice!")



# Temperature conversion Celsius > Farenheit and viceversa
def tempConvert():
    userVars = askWhich()
    option = userVars[0]
    userVal = userVars[1]
    
    if option == 1:
        convCels = userVal/(5/9) + 32
        print("{0:.2f} degrees Celsius = {1:.2f} Farenheit".format(userVal,convCels))
    elif option == 2:
        convCels = (userVal - 32) * 5/9
        print("{0:.2f} degrees Farenheit = {1:.2f} Celsius".format(userVal,convCels))
    else:
        print ("That was not an option...")

def askWhich():
    print("Which temperature would you like to convert from?\n",
          "1 - Celsius to Farenheit\n",
          "2 - Farenheit to Celsius")
    option = int(input())
    userVal = input ("What value do you want to convert? :")
    return (option,float(userVal))



# Solve a quadratic equation
def quadEq(a,b,c):
    D = (b*b - 4*a*c)**0.5
    
    x_1 = (-b + D) / (2 * a)
    x_2 = (-b - D) / (2 * a)
    
    result = (x_1,x_2)
    
    print ("x1 : {0}\nx2 : {1}".format(result[0],result[1]))

# request the values for the quadratic equation
def askQuadEq():
    valA = input("Enter the value of a: ")
    valB = input("Enter the value of b: ")
    valC = input("Enter the value of c: ")
    quadEq(float(valA), float(valB), float(valC))  

#3D object volumes
def sphere_vol(r):
    return (4/3)*math.pi*r*r*r
def cube_vol(lwh):
    return lwh * lwh * lwh
def box_vol(l,w,h):
    return l * w * h
def cone_vol(r,h):
    return (math.pi*r*r) * h/3

#Run program
if __name__ == '__main__':

    while True:
    
        #factors()
        #measureConvert()
        #tempConvert()
        #askQuadEq()
        
        print ("Press x to quit or any other key to continue!")
        userAns = input()
        if userAns == 'x':
            break