import pymel.core as pm

#---------------------------------------------------------------
#Notes:
# Future improvements : Should be able to reduce the amount of code by making a button class and using that rather than referring to each parameter everytime a state changes...

#---------------------------------------------------------------
# Tool Data
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
hookReady = False
#---------------------------------------------------------------
# Window Definition
#---------------------------------------------------------------

class mayaWindow(object):
    def __init__(self):

        self.window = False
        self.title = "Hookup Tool"
        self.size = (320,512)
        self.winWidth = self.size[0]
        self.colReady = ( 0.0, 0.5, 0.7)
        self.colLocked = (0.5, 0.9, 0.0)
        self.marW = 2
        self.marH = 2
        self.marAdjust = self.marW + self.marH

        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window)

        self.window = pm.window(self.window, title=self.title, widthHeight=self.size, s=False)
        self.winLayout = pm.columnLayout(w=self.winWidth)

#----------------------------------------------------------------
        self.bsPanelWidth = self.winWidth
        self.bsPanelLayout = pm.columnLayout(p=self.winLayout, adj=False, w=(self.bsPanelWidth), cal='center')
#----------------------------------------------------------------
        self.paramsLayout = pm.frameLayout(p=self.bsPanelLayout, l='Blendshape Parameters', mh=self.marH, mw=self.marW, w=self.bsPanelWidth)

        self.baseObjName = pm.textFieldGrp(p=self.paramsLayout, l='Set Object:', bgc=self.colReady, cw=(1,64) , cal=(1,'center'), tx=labelDef, ed=False)
        self.activeBs = pm.textFieldGrp(p=self.paramsLayout, l='Blendshape:', bgc=self.colReady, cw=(1,64) , cal=((1,'center'),(2,'center')), tx=labelDef, ed=False)
        self.lockedTar = pm.textFieldGrp(p=self.paramsLayout, l='Targets:',bgc=self.colReady, cw=(1,64) , cal=((1,'center'),(2,'center')), tx=labelDef, ed=False)
        bColWid = (self.bsPanelWidth//4)-self.marAdjust
        self.paramBut = pm.rowLayout(p=self.paramsLayout, nc=4, cl4=('center','center','center','center'))
        self.setBase = pm.button(p=self.paramBut, l=('Set Base'), w=bColWid, c=setBaseObj)
        self.getBs = pm.button(p=self.paramBut, l=('Get Blend'),  w=bColWid, c=getBs)
        self.setObjLock = pm.button(p=self.paramBut, l=(switchVal[0]), bgc=self.colReady, w=bColWid, c=lockBaseObj)
        self.hookBs = pm.button(p=self.paramBut, l=('Hookup'),w=bColWid, c=hookBShapes)

#----------------------------------------------------------------
        self.bsLayout = pm.frameLayout(p=self.bsPanelLayout, l='Blendshapes', cll=True, mh=self.marH, mw=self.marW, w=self.bsPanelWidth)

        self.objBlendsList = pm.textScrollList(p=self.bsLayout, nr=4, fn='smallPlainLabelFont')
        self.labelInput = pm.textFieldButtonGrp(p=self.bsLayout, adj=2, l='Name',cw=((1,32),(2,200)), cal=((1,'center'),(2,'center'),(3,'center')), tx=bsLabel, bl='Create', bc=makeBs)
        bColWid = (self.bsPanelWidth//4)-self.marAdjust
        self.bsButOpt = pm.rowLayout(p=self.bsLayout, nc=4, cl4=('center','center','center','center'))
        self.delBs = pm.button(p=self.bsButOpt, l=('Delete'), w=bColWid, c=delBs)
        self.setBsLock = pm.button(p=self.bsButOpt, l=(switchVal[0]), bgc=self.colReady, w=bColWid, c=setBs)
#----------------------------------------------------------------
        self.targLayout = pm.frameLayout(p=self.bsPanelLayout, l='Target Objects', cll=True, mh=self.marH, mw=self.marW, w=self.bsPanelWidth)

        self.objTargetList = pm.textScrollList(p=self.targLayout, ams=True, nr=8, fn='smallPlainLabelFont')
        bColWid = (self.bsPanelWidth//3)-self.marAdjust
        self.tarButOpt = pm.rowLayout(p=self.targLayout, nc=3, cl3=('center','center','center'))
        self.getTar = pm.button(p=self.tarButOpt, l=('Get'),w=bColWid, c=addTargets)
        self.remTar = pm.button(p=self.tarButOpt, l=('Remove'),w=bColWid, c=remTargets)
        self.setTarLock = pm.button(p=self.tarButOpt, l=(switchVal[0]), bgc=self.colReady, w=bColWid, c=setTargets) # add code to lock targets

#----------------------------------------------------------------

        self.testButton = pm.button(p=self.bsPanelLayout, l=('Print Current Data'),w=self.bsPanelWidth, command=testUI)

#----------------------------------------------------------------

    def showWin(self):
        pm.showWindow()

#----------------------------------------------------------------
# Tool Functions
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
            newBs = pm.blendShape(baseObj[0], n=bsLabel)
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
        print('Selected item {} has been deleted'.format(selBlendshape))

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
            print ('there\'s something wrong here')
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
        

def lockAll(*args):
    global hookReady
    global objLocked
    global bsLocked
    global tarLocked
    if bsLocked and tarLocked and objLocked:
        return
    else:
        print('Missing parameters')
        return False
    
        
def hookBShapes(*args):
    index = 0
    for target in activeTar:
        pm.blendShape(activeBs, e=True, t=[baseObj[0], index, target, 1])
        print('added ', target)
        index += 1
    pm.select(activeBs)
    print('Blendshape has been hooked up. Check the Channel Box for weight sliders')


#----------------------------------------------------------------
# Data contents report
#----------------------------------------------------------------
    
def testUI(self):
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
    print('----------------------------------------------')

#----------------------------------------------------------------
# Initialise tool window and clear console
#----------------------------------------------------------------

hookupWin = mayaWindow()
hookupWin.showWin()

pm.scriptEditorInfo(ch=True)