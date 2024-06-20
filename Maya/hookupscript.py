import maya.cmds as ma

class gWindow(object):
#------------------------------------------------------------------------------
#Window creation parameters
#------------------------------------------------------------------------------    
    def __init__(self):
        self.newWindow = "BSHookupWin"
        self.winTitle = "Blendshape Hook-Up"
        self.winWidth = 320
        self.winHeight = 480
        self.winWH = (self.winWidth, self.winHeight)
        self.sepHeight = 12
        self.padding = 8

        if ma.window(self.newWindow, exists=True):
            ma.deleteUI(self.newWindow, window=True)
        self.window = ma.window(self.newWindow, title=self.winTitle, widthHeight=self.winWH, s=False)

        colNum=1
        colWidth = self.winWidth//colNum
        winLayout = ma.columnLayout(adjustableColumn=False)
#------------------------------------------------------------------------------
#Blendshape Label
#------------------------------------------------------------------------------
        colNum = 2
        colWidth = [self.winWidth*0.6,self.winWidth*0.4]
        
        ma.text(label='\nBlendshape Node Name')
        
        ma.rowColumnLayout(nc=2, cw=[(1,colWidth[0]),(2,colWidth[1])])

        self.bsLabel = ma.textField()
        ma.button(l="Set Label", command=params.setBsLabel)
        
        self.bsLabelUser = ma.text(label='No Label Set')
        self.bsLabelStatus = ma.text(label='',bgc=(0,0,0))
        
        ma.setParent(winLayout)
        ma.separator("bsLabelEndSeparator", w=self.winWidth ,h=self.sepHeight)

#------------------------------------------------------------------------------
# Define and Create Blendshape
#------------------------------------------------------------------------------
        colNum = 2
        colWidth = [self.winWidth*0.3,self.winWidth*0.7]

        ma.text(label='Blendshape Base Object:')        
        ma.rowColumnLayout(nc=2, cw=[(1,colWidth[0]),(2,colWidth[1])])
        
        
        ma.text(label='Base Object Name:')
        self.baseObj = ma.textField()
        ma.text(label='Object Type:')
        self.baseType = ma.text('None')
        ma.text(label='Status:')
        self.creaStatus = ma.text('Not created yet',bgc=(0,0,0))
        
        ma.separator("bsObjStartSeparator", w=self.winWidth ,h=self.sepHeight)
        ma.setParent(winLayout)
        
        colNum = 3
        colWidth = self.winWidth//colNum
        
        ma.rowColumnLayout(nc=3, cw=[(1,colWidth),(2,colWidth),(3,colWidth)])
        ma.button("setbaseObject", l="Set Base Object", command=params.setBase)
        ma.text(label='')
        ma.button("createBlendshape", l="Create Blendshape", command=params.printObjData)        

        ma.setParent(winLayout)
 
        ma.separator("bsObjEndSeparator", w=self.winWidth ,h=self.sepHeight)
        ma.showWindow()
#------------------------------------------------------------------------------
#End of UI
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
#Parameter setup
#------------------------------------------------------------------------------





#------------------------------------------------------------------------------
#Parameter storage functions
#------------------------------------------------------------------------------
class params(object):
    def __init__(self):
        self.bsindex = 0
        self.bsLabel = ''
        self.bsBaseObj = ''
        self.baseType = []
        self.bsList = []
        self.tarList = []
        
    def printObjData(self):
        print('Index Value: ', self.bsindex)
        print('Blendshape Label: ', self.bsLabel)
        print('Base Object: ', self.bsBaseObj)
        print('Existing Blendshapes: ', self.bsList)
        print('Target Objects: ', self.tarList)
            
    def setBsLabel(self):
        self.bsLabel = ma.textField(BSHookup.bsLabel, q=True, text=True)
    
        ma.text(BSHookup.bsLabelUser, e=True, label=self.bsLabel)
        ma.text(BSHookup.bsLabelStatus, e=True, label='',bgc=(0,1,0))
        print('Blendshape label: ', self.bsLabel)
           
    def setBase(self):
        selData = ma.ls(sl=True)
        self.bsBaseObj = selData[0]
        self.baseType = ma.nodeType(selData[0])
        ma.textField(BSHookup.baseObj, e=True,tx=self.bsBaseObj)
        ma.text(BSHookup.baseType, e=True,label=self.baseType)
        print('Blendshape base: ', self.bsBaseObj)
        print('Blendshape object type:', self.baseType)
        
#------------------------------------------------------------------------------
#Data Processing class - TODO
#------------------------------------------------------------------------------

def creaBS(self):
    bsList = ma.ls(ma.listHistory(BSData.bsBaseObj), type='blendShape')
    print(bsList)
    if BSData.bsLabel in bsList:
        ma.text(BSHookup.creaStatus,e=True,label='Failed!',bgc=(1,0,0))
        print('You must choose a unique name')
    else:
        ma.blendShape(BSData.bsBaseObj,name=BSData.bsLabel)
        ma.text(BSHookup.creaStatus,e=True,label='Success!',bgc=(0,1,0))







def main():
    BSHookup = gWindow()
    BSData = params()
    
    ma.scriptEditorInfo(ch=True)
     

if __name__ == "__main__":
    main()