import pymel.core as pm

#---------------------------------------------------------------
#Notes:
# Future improvements : Should be able to reduce the amount of code by making a button class and using that rather than referring to each parameter everytime a state changes...
#---------------------------------------------------------------
#Testvars
#---------------------------------------------------------------
nameColWidth = 0

#---------------------------------------------------------------
# Control Creation Variables
#---------------------------------------------------------------
selCTL = []
ctlFACSAttr = []
weightList = [] #currently locked blendshape's targets
matchList = []
nodeMatchList = []
ctlList = []
creaPos = (0,0,0)
ctlMaxRange = 4
ctlMinRange = 4
ignoreSuffix = []
prefString = ''

#---------------------------------------------------------------
# Tool Data
#---------------------------------------------------------------
# BlendShape Hookup
#---------------------------------------------------------------
bsLabel = "New Blendshape"
labelDef = "Not Set"
baseObj = []
objLocked = False
bsList = []
activeBs = []
bsLocked = False
bsTargets = []
activeTar = []
tarLocked = False
switchVal = ('Lock','Locked')
selectedbs = []
oriOptSel = ('world','local','user')
baseOri = 0
targetType = ('Object','Tangent','Transform')
baseTarType = 0
readyOrNot = False
#---------------------------------------------------------------
#Control Creator
#---------------------------------------------------------------
ctlShape = (
('Circle', 'ctl_Circle'),
('Square', 'ctl_Square'),
('Triangle', 'ctl_Triangle'),
('RoundSquare', 'ctl_RoundSquare'),
('Movement', 'ctl_Move'),
('Movement A', 'ctl_Arrow_MovementA'),
('Movement B', 'ctl_Arrow_MovementB'),
('Movement C', 'ctl_Arrow_MovementC'),
('Rotation A', 'ctl_Arrow_RotationA'),
('Rotation B', 'ctl_Arrow_RotationB'))
#---------------------------------------------------------------
# Window Definition
#---------------------------------------------------------------

class mayaWindow(object):
    def __init__(self):

        self.window = False
        self.title = "Hookup Tool"
        self.size = (640,512)
        self.winWidth = self.size[0]
        self.colReady = ( 0.0, 0.5, 0.7)
        self.colLocked = (0.5, 0.9, 0.0)
        self.marW = 2
        self.marH = 2
        self.marAdjust = self.marW + self.marH

        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window)

        self.window = pm.window(self.window, title=self.title, widthHeight=self.size, s=False)
        
        panWidth = (self.winWidth//2)
        self.winLayout = pm.rowColumnLayout(nc=2, cw=(panWidth,panWidth), w=self.winWidth)

#----------------------------------------------------------------
#Blendshape Creation Panel
#----------------------------------------------------------------
        self.bsPanelWidth = self.winWidth//2
        self.bsPanelLayout = pm.columnLayout(p=self.winLayout, adj=False, w=(self.bsPanelWidth), cal='left')
#----------------------------------------------------------------
        self.paramsLayout = pm.frameLayout(p=self.bsPanelLayout, l='Blendshape Parameters', mh=self.marH, mw=self.marW)

        self.baseObjName = pm.textFieldGrp(p=self.paramsLayout, l='Set Object:', bgc=self.colReady, cw=(1,64) , cal=(1,'center'), tx=labelDef, ed=False)
        self.activeBs = pm.textFieldGrp(p=self.paramsLayout, l='Blendshape:', bgc=self.colReady, cw=(1,64) , cal=((1,'center'),(2,'center')), tx=labelDef, ed=False)
        self.lockedTar = pm.textFieldGrp(p=self.paramsLayout, l='Targets:',bgc=self.colReady, cw=(1,64) , cal=((1,'center'),(2,'center')), tx=labelDef, ed=False)
        parmsColWid = (self.bsPanelWidth//4)-self.marAdjust
        self.paramBut = pm.rowLayout(p=self.paramsLayout, nc=4, cl4=('center','center','center','center'))
        self.setBase = pm.button(p=self.paramBut, l=('Set Base'), w=parmsColWid, c=setBaseObj)
        self.getBs = pm.button(p=self.paramBut, l=('Get Blend'),  w=parmsColWid, c=getBs)
        self.setObjLock = pm.button(p=self.paramBut, l=(switchVal[0]), bgc=self.colReady, w=parmsColWid, c=lockBaseObj)
        self.hookBs = pm.button(p=self.paramBut, l=('Hookup'),w=parmsColWid, c=hookBShapes)

#----------------------------------------------------------------
        self.bsLayout = pm.frameLayout(p=self.bsPanelLayout, l='Blendshapes', cll=True, mh=self.marH, mw=self.marW, w=self.bsPanelWidth)

        self.objBlendsList = pm.textScrollList(p=self.bsLayout, nr=4, fn='smallPlainLabelFont', sc=selBs)
        self.labelInput = pm.textFieldButtonGrp(p=self.bsLayout, adj=2, l='Name',cw=((1,32),(2,200)), cal=((1,'center'),(2,'center'),(3,'center')), tx=bsLabel, bl='Create', bc=makeBs)
        bsColWid = (self.bsPanelWidth//4)-self.marAdjust
        self.bsButOpt = pm.rowLayout(p=self.bsLayout, nc=4, cl4=('center','center','center','center'))
        self.selBs = pm.button(p=self.bsButOpt, l=('Select'), w=bsColWid, c=selBs)
        self.delBs = pm.button(p=self.bsButOpt, l=('Delete'), w=bsColWid, c=delBs)
        self.setBsLock = pm.button(p=self.bsButOpt, l=(switchVal[0]), bgc=self.colReady, w=bsColWid, c=setBs)
#----------------------------------------------------------------
        self.targLayout = pm.frameLayout(p=self.bsPanelLayout, l='Target Objects', cll=True, mh=self.marH, mw=self.marW, w=self.bsPanelWidth)

        self.objTargetList = pm.textScrollList(p=self.targLayout, ams=True, nr=8, fn='smallPlainLabelFont')
        tarColWid = (self.bsPanelWidth//3)-self.marAdjust
        self.tarButOpt = pm.rowLayout(p=self.targLayout, nc=3, cl3=('center','center','center'))
        self.getTar = pm.button(p=self.tarButOpt, l=('Get'),w=tarColWid, c=addTargets)
        self.remTar = pm.button(p=self.tarButOpt, l=('Remove'),w=tarColWid, c=remTargets)
        self.setTarLock = pm.button(p=self.tarButOpt, l=(switchVal[0]), bgc=self.colReady, w=tarColWid, c=setTargets)

#----------------------------------------------------------------
#Options
#----------------------------------------------------------------
        self.optLayout = pm.frameLayout(p=self.bsPanelLayout, l='Options', mh=self.marH, mw=self.marW, w=self.bsPanelWidth)
        oColWid = (self.bsPanelWidth//2)-self.marAdjust
        self.optButLayout = pm.rowLayout(p = self.optLayout, nc=2, cl2=('center','center'))
        self.objOrigin = pm.optionMenu(p = self.optButLayout , l='Object Origin',cc=setObjOri, w=oColWid)
        pm.menuItem(p=self.objOrigin, l=oriOptSel[0])
        pm.menuItem(p=self.objOrigin, l=oriOptSel[1])
        pm.menuItem(p=self.objOrigin, l=oriOptSel[2])
        self.targetType = pm.optionMenu(p=self.optButLayout , l='Target Type', en=False, w=oColWid) ###This is based on the deformation order (bf flag I think) setting it can only be set before geometry is added
        pm.menuItem(l=targetType[0]) 
        pm.menuItem(l=targetType[1])
        pm.menuItem(l=targetType[2])

#----------------------------------------------------------------

        self.testButton = pm.button(p=self.bsPanelLayout, l=('Print Current Data'),w=self.bsPanelWidth, command=testUI)

#----------------------------------------------------------------
#Control Creation Layout
#----------------------------------------------------------------
        ctlPanelWidth = self.winWidth//2
        self.ctlCreaLayout = pm.columnLayout(p=self.winLayout, adj=False, w=(ctlPanelWidth), cal='left')
        
#----------------------------------------------------------------
#Control Creator Panel
#----------------------------------------------------------------

        self.ctlCreaParams = pm.frameLayout(p=self.ctlCreaLayout, l='Control Naming', mh=self.marH, mw=self.marW)
        
        ctlNamLayWidth = ctlPanelWidth//4
        self.newCtlName = pm.textFieldGrp(p=self.ctlCreaParams, l='Control name: ', cw=(1,ctlNamLayWidth))
        self.newCtlSuf = pm.textFieldGrp(p=self.ctlCreaParams, l='Suffix: ', cw=(1,ctlNamLayWidth), tx='_L,_R,_B,_F')
        self.newCtlPre = pm.textFieldGrp(p=self.ctlCreaParams,l='Prefix: ', cw=(1,ctlNamLayWidth), tx='FACS_')

        
        self.ctlParLay = pm.frameLayout(p=self.ctlCreaParams, l='Other Parameters',cl=True, cll=True, mh=self.marH, mw=self.marW)

        self.ctlSize = pm.intFieldGrp(p=self.ctlParLay, l='Size: ')
        self.ctlCount = pm.intFieldGrp(p=self.ctlParLay, l='Number: ')
        self.ctlRelation = pm.optionMenuGrp(p=self.ctlParLay, l='Relation: ')
        pm.menuItem(l='Default')
        pm.menuItem(l='Parent')
        pm.menuItem(l='Child')
        self.ctlPosition = pm.optionMenuGrp(p= self.ctlParLay, l='Position: ')
        pm.menuItem(l='Selected')
        pm.menuItem(l='World')
        pm.menuItem(l='Origin')
        self.ctlShape = pm.optionMenuGrp(p=self.ctlParLay, l="IK Icons: ")
        pm.menuItem(label=ctlShape[0][0])
        pm.menuItem(label=ctlShape[1][0])
        pm.menuItem(label=ctlShape[2][0])
        pm.menuItem(label=ctlShape[3][0])
        pm.menuItem(label=ctlShape[4][0])
        pm.menuItem(label=ctlShape[5][0])
        pm.menuItem(label=ctlShape[6][0])
        pm.menuItem(label=ctlShape[7][0])
        pm.menuItem(label=ctlShape[8][0])
        pm.menuItem(label=ctlShape[9][0])


        self.ctlPanelWidth = self.winWidth//2
        self.ctlHooks = pm.frameLayout(p=self.ctlCreaParams, l='Hook Control Box Attributes', mh=self.marH, mw=self.marW, w=self.ctlPanelWidth)
        
        self.testButton = pm.button(p=self.ctlHooks, l=('get CTL attributes'),w=self.bsPanelWidth, command=getCTLAttributes)
        self.testButton = pm.button(p=self.ctlHooks, l=('get ControlBox MatchNames'),w=self.bsPanelWidth, command=matchCTLAttrWeight)
        self.testButton = pm.button(p=self.ctlHooks, l=('Connect channel Box Controls'),w=self.bsPanelWidth, command=connCtlToTar)
        self.testButton = pm.button(p=self.ctlHooks, l=('get RangeConverter MatchNames'),w=self.bsPanelWidth, command=matchRngConvToWeight)
        self.testButton = pm.button(p=self.ctlHooks, l=('Connect range converters'),w=self.bsPanelWidth, command=connRngConvToTar)
        
        self.rangeVsWeight = pm.columnLayout(p=self.ctlHooks)
        self.ranNodeList = pm.textScrollList(p=self.rangeVsWeight, nr=16, ams=True, fn='smallPlainLabelFont', w=self.winWidth)
        
        pm.button(p=self.rangeVsWeight, l='Remove items', w=self.bsPanelWidth, command=remConnFromList )


#----------------------------------------------------------------
#----------------------------------------------------------------


    def showWin(self):
        pm.showWindow()

#----------------------------------------------------------------
# Tool Functions
#----------------------------------------------------------------
# Blendshape Creation Panel
#----------------------------------------------------------------

def setBaseObj(self):
    global baseObj

    selObj = pm.ls(sl=True)
    try:
        if len(selObj) == 1 and selObj[0] not in bsTargets:
            baseObj = selObj
            hookupWin.baseObjName.setText(baseObj[0])
        elif selObj[0] in bsTargets:
            print('Object already in the target list')
        else:
            print('You have too many objects selected')
    except:
        print('Select an object to set as the BaseObject')

def lockBaseObj(*args):
    global objLocked
    if not objLocked:
        if baseObj != []:
            hookupWin.setBase.setEnable(False)
            hookupWin.baseObjName.setBackgroundColor(hookupWin.colLocked)
            hookupWin.setObjLock.setBackgroundColor(hookupWin.colLocked)
            hookupWin.setObjLock.setLabel(switchVal[1])
            objLocked = True
            print(objLocked)
        else:
            if objLocked:
                objLocked = False
                print(objLocked)
            print('no base object has been set')
    else:
        hookupWin.setBase.setEnable(True)
        hookupWin.baseObjName.setBackgroundColor(hookupWin.colReady)
        hookupWin.setObjLock.setBackgroundColor(hookupWin.colReady)
        hookupWin.setObjLock.setLabel(switchVal[0])
        objLocked = False
        print(objLocked)

def makeBs(*args):
    global bsLabel
    bsLabel = hookupWin.labelInput.getText()
    if bsLocked == False:
        global bsList
        try:
            newBs = pm.blendShape(baseObj[0],o=oriOptSel[baseOri], n=bsLabel)
            hookupWin.objBlendsList.append(newBs)
            bsList.append(newBs)
        except IndexError:
            print('You need to set a BaseObject')
        
def getBs(*args):
    if bsLocked == False:
        global bsList
        if baseObj:
            bsList = pm.ls(pm.listHistory(baseObj), type='blendShape')
            hookupWin.objBlendsList.removeAll()
            for item in bsList:
                hookupWin.objBlendsList.append(item)
        else:
            print ('no object has been set as the base object')
        return

def delBs(*args):
    if bsLocked == False:
        global bsList
        selBlendshape = hookupWin.objBlendsList.getSelectItem()
        hookupWin.objBlendsList.removeItem(selBlendshape)
        pm.delete(selBlendshape)
        bsList = pm.ls(pm.listHistory(baseObj), type='blendShape')

def selBs(*args):
    try:
        global baseOri
        pm.select(hookupWin.objBlendsList.getSelectItem())
        originType = pm.getAttr('{0}.origin'.format(pm.ls(sl=True)[0]))
        baseOri = originType
        menuVal = originType + 1
        hookupWin.objOrigin.setSelect(sl=(menuVal))

    except TypeError:
        print('Selected blendshape has been deleted')
        
        
def setBs(*args):
    global activeBs
    global bsLocked
    if bsLocked == False:
        activeBs = hookupWin.objBlendsList.getSelectItem()
        if activeBs != []:
            hookupWin.objBlendsList.setEnable(False)
            hookupWin.setBsLock.setLabel(switchVal[1])
            hookupWin.setBsLock.setBackgroundColor(hookupWin.colLocked)
            hookupWin.activeBs.setBackgroundColor(hookupWin.colLocked)
            hookupWin.getBs.setEnable(False)
            hookupWin.delBs.setEnable(False)
            bsLocked = True
            hookupWin.activeBs.setText(activeBs[0])
            hookupWin.labelInput.setEnable(False)
            getBSTargets()
        else:
            print('No Blendshape selected')
    else:
        bsLocked = False
        hookupWin.objBlendsList.setEnable(True)
        hookupWin.setBsLock.setLabel(switchVal[0])
        hookupWin.setBsLock.setBackgroundColor(hookupWin.colReady)
        hookupWin.activeBs.setBackgroundColor(hookupWin.colReady)
        hookupWin.activeBs.setText(labelDef)
        hookupWin.labelInput.setEnable(True)
        activeBs.clear()
        hookupWin.getBs.setEnable(True)
        hookupWin.delBs.setEnable(True)
        print('No blendshape locked')

def addTargets(*args):
    global bsTargets
    currSel = pm.ls(sl=True)
    if baseObj != []:
        if baseObj[0] in currSel:
            pm.select(baseObj, tgl=True)
            currSel = pm.ls(sl=True)
    hookupWin.objTargetList.removeAll()            
    for target in currSel:
        if target not in bsTargets:
            print(target)
            bsTargets.append(target)
        hookupWin.objTargetList.append(target)

def remTargets(*args):
    global bsTargets
    selTar = hookupWin.objTargetList.getSelectItem()
    for tar in selTar:
        hookupWin.objTargetList.removeItem(tar)
        bsTargets.remove(tar)

def setTargets(*args):
    global tarLocked
    global activeTar
    if tarLocked == False:
        if bsTargets != []:
            activeTar = hookupWin.objTargetList.getSelectItem()
            hookupWin.setTarLock.setLabel(switchVal[1])
            hookupWin.setTarLock.setBackgroundColor(hookupWin.colLocked)
            hookupWin.objTargetList.setEnable(False)
            hookupWin.getTar.setEnable(False)
            hookupWin.remTar.setEnable(False)
            hookupWin.lockedTar.setText(len(activeTar))
            hookupWin.lockedTar.setBackgroundColor(hookupWin.colLocked)
            tarLocked = True
        else:
            print ('No Targets selected!!')
    else:
        activeTar.clear()
        hookupWin.setTarLock.setLabel(switchVal[0])
        hookupWin.setTarLock.setBackgroundColor(hookupWin.colReady)
        hookupWin.lockedTar.setBackgroundColor(hookupWin.colLocked)
        hookupWin.objTargetList.setEnable(True)
        hookupWin.getTar.setEnable(True)
        hookupWin.remTar.setEnable(True)
        hookupWin.lockedTar.setText(len(bsTargets))
        hookupWin.lockedTar.setBackgroundColor(hookupWin.colReady)
        tarLocked = False

def setObjOri(*args):
    global baseOri
    if bsList == []:
        baseOri = hookupWin.objOrigin.getSelect() - 1
    else:
        sel = pm.ls(sl=True)
        newOrigin = hookupWin.objOrigin.getSelect()
        baseOri = newOrigin - 1
        #pm.setAttr('{0}.origin'.format(sel[0]), baseOri)
        #currently this can edit the selected blendshape origin BUT it can cause problems when creating a new blendshape... will rethink it

def lockAll(*args):
    print('lockall ran')
    global readyOrNot
    global objLocked
    global bsLocked
    global tarLocked
    if bsLocked and tarLocked and objLocked:
        readyOrNot = True
    else:
        print('Missing parameters')
        readyOrNot = False

def hookBShapes(*args):
    lockAll()
    print(readyOrNot)
    if readyOrNot:
        index = 0
        getBSTargets
        if (len(weightList)) != index:
            index = (len(weightList))
        for target in activeTar:
            pm.blendShape(activeBs, e=True, t=[baseObj[0], index, target, 1])
            index += 1
        pm.select(activeBs)
        getBSTargets
        print('Blendshape has been hooked up. Check the Channel Box for weight sliders')
    else:
        print ('Nope')

#----------------------------------------------------------------
# Blendshape Data Panel
#----------------------------------------------------------------
def loadBsTargets(*args):
    hookupWin.paramBut.append(bsList)


#----------------------------------------------------------------
# Data contents report
#----------------------------------------------------------------
    
def testUI(self):
    """
    print('----------------------------------------------')
    print(' Label (bsLabel) : ', hookupWin.labelInput.getText())
    print(' Target (baseObj) : ', baseObj)
    print(' blendshape list (bsList): ', bsList)
    print(' Locked blendshape (activeBs) : ', activeBs)
    print(' Blendshape Targets (bsTargets) : ', bsTargets)
    print(' Locked targets (activeTar) :', activeTar)
    print(' Objlock status (objLocked) : ', objLocked)
    print(' Bslock status (bsLocked) : ', bsLocked)
    print(' Tarlock status (tarLocked) : ', tarLocked)
    print(' Blendshape Origin: {0} value {1}'.format(oriOptSel[baseOri],baseOri))
    print('----------------------------------------------')
    print('nameColWidth = ', nameColWidth)
    """
#----------------------------------------------------------------
    print('----------------------------------------------')
    print('selCTL (selCTL): ',selCTL)
    print('ctlFACSAttr (ctlFACSAttr): ', ctlFACSAttr)
    print('weightList (weightList): ', weightList)
    print('matchList (matchList): ', matchList)
    print('ctlList (ctlList): ', ctlList)
    print('Ignore Suffix (ignoreSuffix): ', ignoreSuffix)
    print('Prefix (prefString): ', prefString)
    print('Range Conversion nodes: ', nodeMatchList)
    print('----------------------------------------------')
#----------------------------------------------------------------
# Initialise tool window and clear console
#----------------------------------------------------------------

def creaCTLs(*args):
    global ctlList
    for i in weightList:
        ctlName = ('{0}_CTL'.format(i))
        ctlCircle = pm.circle(n=ctlName, nr=(0,0,1), c=(creaPos), r=(1))
        pm.transformLimits(ety=(True,True),ty=( ctlMinRange, ctlMaxRange))
        ctlList.append(ctlCircle)        

def getCTLAttributes(*args): # GetControlAttributes in the selected CTL
    global selCTL
    global ctlFACSAttr
    selCTL = pm.ls(sl=True)
    ctlFACSAttr = pm.listAttr(ud=True)
    ctlFACSAttr.sort()

def getBSTargets(*args): #Grab all blendshape targets in the locked (ActibeBs) blendshape node
    global weightList
    weightList = pm.listAttr(activeBs, multi=True, string='weight')
    weightList.sort()

#def makeCTLList(*args): #This needs fleshing out a lot
#    controlList = pm.ls(sl=True)
#    print(controlList) # Currently not stored anywhere
def getConnAttrs(*arg):
    global prefString
    suffixFilter()
    prefString = hookupWin.newCtlPre.getText()
    

def suffixFilter(*args):
    global ignoreSuffix
    sufString = hookupWin.newCtlSuf.getText()
    filterString = sufString.split(',')
    print(filterString)
    for i in filterString:
        ignoreSuffix.append(i)
    
def matchCTLAttrWeight(*args):
    
    global matchList
    baseNameList = []
    matchList = []
    indexVal = 0
    
    getConnAttrs()
    for ctlAttr in ctlFACSAttr:
        splitName = ctlAttr.split('_')
        baseName = splitName[0]
        baseNameList.append(baseName)
    for name in baseNameList:
        weightName = '{0}{1}'.format(prefString,name)
        matchList.append((ctlFACSAttr[indexVal], weightName))
        indexVal += 1
    print('matchList: ', matchList)

def matchRngConvToWeight(*args):
    global nodeMatchList
    nodeMatchList.clear()
    getConnAttrs()
    newWeightList = []

    for suf in ignoreSuffix:
        for weight in weightList:
            if suf in weight:
                newWeightList.append(weight)
    print('NewList:', newWeightList)
    
    for weight in newWeightList:
        newName = weight.replace(prefString,'')
        newName = ('{0}_CTL_rangeConverter'.format(newName))
        nodeMatchList.append((newName, weight))
    nodeMatchList.sort()
    populateList()

def populateList(*args):
    hookupWin.ranNodeList.removeAll()
    for nodePair in nodeMatchList:
        itemInList = '{0}_VS_{1}'.format(nodePair[0],nodePair[1])
        hookupWin.ranNodeList.append(itemInList)
    
def connCtlToTar(*args):
    for item in matchList:
        pm.connectAttr('{0}.{1}'.format(selCTL[0],item[0]) , activeBs[0] + '.' + item[1])

def connRngConvToTar(*args):
    connectValue = '.outValue.outValueX'

    for item in nodeMatchList:
        pm.select(item[0])
        node = pm.ls(sl=True)
        print(node)
        pm.connectAttr(node[0] + connectValue , activeBs[0] + '.' + item[1] )

def remConnFromList(*args):
    global nodeMatchList
    remTupleList = []
    itemToRemove = hookupWin.ranNodeList.getSelectItem()
    for i in itemToRemove:
        tupleParts = i.split('_VS_')
        remTuple = (tupleParts[0],tupleParts[1])
        remTupleList.append(remTuple)
    print('removing these: ',remTupleList)
    for item in remTupleList:
        nodeMatchList.remove(item)
    populateList()


hookupWin = mayaWindow()
hookupWin.showWin()

pm.scriptEditorInfo(ch=True)