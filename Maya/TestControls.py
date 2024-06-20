import maya.cmds as ma
import pymel.core as pm


objNames = ['Cube','Cube_Small','Cube_Large','Cube_X','Cube_Y','Cube_Z']
objSDef = [(1,1,1), (0.5,0.5,0.5), (2,2,2), (2,1,1), (1,2,1), (1,1,2)]
cubeList = []#List of objects

ctlList = []
ctlNames = []
asocNodes = [] #list of setRange nodes
asocNodeNames = [] #list of setRange node names

zippedList = []

movVal = 1 #object position movement value when layout function is called

ctlMaxRange = 4
ctlMinRange = -4
minMaxNodes = []
minMaxLabels = ['Slider_Max_Value', 'Slider_Min_Value']

bsBase = ''
bsObjs = []
bsList = []

activeBs = ''

#Create the Test cubes
def testCubes(names,scaleVals):
    count = 0
    for name in names:
        sizeVals = scaleVals[count]
        pm.polyCube(n=name)
        selObj = pm.ls(sl=True)
        pm.scale(selObj, sizeVals[0] , sizeVals[1] , sizeVals[2], r=True)
        cubeList.append(pm.ls(sl=True))
        count += 1
    for i in range(1,len(cubeList)):
        pm.setAttr( (cubeList[i])[0] + ".v", 0)


#Create blendshape and targets for a given object
def setBShape(bsObjs, bsName):
    index = 0
    
    bsList.append(pm.blendShape(bsObjs[0],name=bsName))
    bsBase = bsObjs[0]
    bsTargets = bsObjs.copy()
    del bsTargets[0]

    for target in bsTargets:
        pm.blendShape(bsList[0], e=True, ts=True, o='world', t=[bsBase[0], index, target[0],  1])
        index +=1
    
    
#Create the circle controls aligned to normal-z
def makeCTL(name,pos,rad):
    pm.circle(n=name, nr=(0,0,1), c=(pos), r=(rad))
    pm.transformLimits(ety=(True,True),ty=( ctlMinRange, ctlMaxRange))
    ctlList.append(pm.ls(sl=True))

#Create a Control box and attach all given controls to a group
def makeCTLBox():
    print('TODO!!!')

#Create the setRange nodes and store them in a list
def creaNodes(CTLName):
    nodeName = CTLName + '_rangeConverter'
    pm.shadingNode('setRange', asUtility=True)
    pm.rename(('setRange'+str(1)), nodeName)
    pm.setAttr(nodeName + '.maxX', 1)
    asocNodes.append(ma.ls())
    asocNodeNames.append(nodeName)

#Create limit nodes and set them to the ctlMaxRange and ctlMinRange variables
def creaLimitNodes(labels):
    pm.shadingNode('floatConstant', asUtility=True)
    pm.rename('floatConstant'+str(1), labels[0])
    pm.setAttr((labels[0] + ".inFloat"), ctlMaxRange)
    minMaxNodes.append(ma.ls())

    
    pm.shadingNode('floatConstant', asUtility=True)
    pm.rename('floatConstant'+str(1), labels[1])
    pm.setAttr((labels[1] + ".inFloat"), ctlMinRange)
    minMaxNodes.append(ma.ls())
    
    
#Setup the channelbox locks and visibility
def setupCTL(nameList):
    for CTLname in nameList:
        pm.setAttr((CTLname + ".tx"), cb = False, k=False, l=True)
        pm.setAttr((CTLname + ".tz"), cb = False, k=False, l=True)
        pm.setAttr((CTLname + ".rx"), cb = False, k=False, l=True)
        pm.setAttr((CTLname + ".ry"), cb = False, k=False, l=True)
        pm.setAttr((CTLname + ".rz"), cb = False, k=False, l=True)
        pm.setAttr((CTLname + ".sx"), cb = False, k=False, l=True)
        pm.setAttr((CTLname + ".sy"), cb = False, k=False, l=True)
        pm.setAttr((CTLname + ".sz"), cb = False, k=False, l=True)

#Move controlers
def layoutCTL(ctlList):
    for i in range (0,len(ctlList)):      
        pm.move( i, ctlList[i], x=True, relative=True )
        #print("Object {0} has been moved {1} units".format(ctlList[i],i))


#Hook-up controls,range nodes and min/max nodes
def hookUp(ctlList,rngNodeList,objList,bsToHook):
    cubeBase = objList[0]

    weightIndex = 0
    ranNodes = rngNodeList.copy()
    
    ctlRng = zip(ctlList,ranNodes)

    for item in ctlRng:
        pm.connectAttr(item[0] + '.translateY', item[1] + '.valueX.')
        pm.connectAttr(minMaxLabels[0] + '.outFloat', item[1] + '.oldMax.oldMaxX')
        pm.connectAttr(minMaxLabels[1] + '.outFloat', item[1] + '.oldMin.oldMinX')
    
    activeBs = bsToHook[0]
    weightList = pm.listAttr(bsToHook[0], multi=True, string='weight')
    rngWeight = zip(ranNodes,weightList)


######TODO!!!!!!!!! 
    for item in rngWeight:
        pm.connectAttr(item[0] + '.outValue.outValueX' , activeBs[0] + '.' + item[1])   
   


#Run makeCTL and create the SetRange nodes for it

def CTLSetup(objectNames):
    objects = objectNames.copy()
    del objects[0]
    count = 0
    numCTLs = len(objects)    

    for i in range(1,(numCTLs+1)):
        ctlName = objects[count] + "_CTL"
        ctlNames.append(ctlName)
        creaPos = (0,0,0)
        rad = 0.25
        makeCTL(ctlName,creaPos,rad)
        creaNodes(ctlName)
        count += 1

    layoutCTL(ctlList) #works
    setupCTL(ctlNames) #works
    creaLimitNodes(minMaxLabels) #works
    hookUp(ctlNames,asocNodeNames,cubeList, bsList) #In progress

#print('This is the control list: ',ctlList)
#print('These are the control names: ', ctlNames)
#print('These are the utility node Names', asocNodeNames)
#print(minMaxNodes)


#TESTS!!!! =  Test Cubes
testCubes(objNames,objSDef)

bsLabel = "My_Blendshape"
bsObjs = cubeList
setBShape(bsObjs, bsLabel)
CTLSetup(objNames)

