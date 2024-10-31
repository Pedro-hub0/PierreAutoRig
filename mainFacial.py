
import maya.cmds as cmds
import sys
import os
import importlib

# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)

import modules.smallUsefulFct


importlib.reload(modules.smallUsefulFct)



"""Script created by Pierre LIPPENS """

def create_window():
    """
    Create a window with a button.
    """
    # Check if the window already exists, and delete it if it does
    if cmds.window("myWindow", exists=True):
        cmds.deleteUI("myWindow", window=True)

    # Create the window
    window_name = cmds.window("myWindow", title="MatchIkFk_PierreAuto", widthHeight=(310, 100), sizeable=False)
    # Create a layout for the window
    column_layout= cmds.columnLayout(adjustableColumn=True)


    cmds.separator(h=8)
    cmds.text(label="TOOLS", font = "boldLabelFont" , w = 300, align = "center")
    cmds.separator(h=8)

    cmds.text(label=" JntOnRivet ", font = "boldLabelFont" , w = 300, align = "left")
    cmds.separator(h=5)
    # Create a text field
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[75,75,75,75])
    cmds.text(label="Speed", font = "boldLabelFont" , w = 50, align = "left")
    speed = cmds.floatField(value=1.3,width=75)
    cmds.text(label="length", font = "boldLabelFont" , w = 50, align = "left")
    number = cmds.intField(value=5,width=75)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnWidth2=[100,100])
    cmds.button(label='Jnt', command=lambda x:createJnt(),width=75)
    cmds.button(label='Blend', command=lambda x:createBlend(speed,number),width=75)
    cmds.setParent('..')


    # Show the window
    cmds.showWindow(window_name)

def createJnt():
    jnts=[]

    selection=cmds.ls(selection=True)
    length=5
    for sel in selection:
        tr=cmds.xform(sel, query=True, worldSpace=True, translation=True)
        cmds.select(clear=True)
        jnt=cmds.joint(n=f'Bind_{sel}',p=tr)
        jnts.append(jnt)
        cmds.xform(jnt,translation=tr,worldSpace=True)
        if not cmds.attributeQuery(f'Zip', node='Zip_Ctrl', exists=True):
            cmds.addAttr('Zip_Ctrl', longName=f'Zip',attributeType='float', defaultValue=0,min=0,max=1,keyable=True)

        
def createBlend(speed,l):   
    attrZipL="Zip_Ctrl.Zip_L"
    attrZipR="Zip_Ctrl.Zip_R"
    selection=cmds.ls(selection=True)
    sp=cmds.floatField(speed, query=True, value=True) 
    length=cmds.intField(l, query=True, value=True)   
    for i in range(1,length+1):
        if not cmds.attributeQuery(f'Zip_R', node='Zip_Ctrl', exists=True):
            cmds.addAttr('Zip_Ctrl', longName=f'Zip_R',attributeType='float', defaultValue=0,min=0,max=1,keyable=True)
        if not cmds.attributeQuery(f'Zip_L', node='Zip_Ctrl', exists=True):
            cmds.addAttr('Zip_Ctrl', longName=f'Zip_L',attributeType='float', defaultValue=0.5,min=0,max=1,keyable=True)
        if not cmds.attributeQuery(f'Zip_Avg', node='Zip_Ctrl', exists=True):
            cmds.addAttr('Zip_Ctrl', longName=f'Zip_Avg',attributeType='float', defaultValue=0.5,min=0,max=1,keyable=True)
               
        ##NODES
        zipremap01= cmds.createNode('setRange', name=f'Zip_setRange_{i}')
        val=(length-i)*(1/length)
        val2=(length-i)*(1/length)+sp/length
        initialiseRemap(zipremap01,0,1,val,val2,'X')
        initialiseRemap(zipremap01,0,1,1-val2,1-val,'Y')
        initialiseRemap(zipremap01,0,1,0,1,'Z')
        blendavg = cmds.createNode('blendColors', name=f'Zip_blendavg_{i}')
        blendup = cmds.createNode('blendColors', name=f'Zip_blendup_{i}')
        blendwn = cmds.createNode('blendColors', name=f'Zip_blendwn_{i}')
        pmaLR = cmds.createNode('plusMinusAverage', name=f'Zip_pmaLR_{i}')
        cmds.setAttr(f'{pmaLR}.operation',1)


        ##NODES Connexions
        
        
        #Set Range
        cmds.connectAttr(attrZipR,f'{zipremap01}.valueX')
        cmds.connectAttr(attrZipL,f'{zipremap01}.valueY')
        cmds.connectAttr(f'Riv_Dwn_0{i}.translate',f'{blendavg}.color2')
        cmds.connectAttr(f'Riv_Up_0{i}.translate',f'{blendavg}.color1')
        cmds.connectAttr(f'Zip_Ctrl.Zip_Avg',f'{blendavg}.blender')

        #System L R
        cmds.connectAttr(f'{zipremap01}.outValueX',f'{pmaLR}.input1D[0]')
        cmds.connectAttr(f'{zipremap01}.outValueY',f'{pmaLR}.input1D[1]')
        cmds.connectAttr(f'{pmaLR}.output1D',f'{zipremap01}.valueZ')

        #Blend
        cmds.connectAttr(f'{zipremap01}.outValueZ',f'{blendup}.blender')
        cmds.connectAttr(f'{zipremap01}.outValueZ',f'{blendwn}.blender')
        cmds.connectAttr(f'{blendavg}.output',f'{blendup}.color1')
        cmds.connectAttr(f'{blendavg}.output',f'{blendwn}.color1')

        cmds.connectAttr(f'Riv_Dwn_0{i}.translate',f'{blendup}.color2')
        cmds.connectAttr(f'Riv_Up_0{i}.translate',f'{blendwn}.color2')

        #Connect to joints
        cmds.connectAttr(f'{blendup}.output',f'Bind_Riv_Dwn_0{i}.translate')
        cmds.connectAttr(f'{blendwn}.output',f'Bind_Riv_Up_0{i}.translate')


def initialiseRemap(n,a,b,c,d,axe):
        cmds.setAttr(f'{n}.min{axe}', a)
        cmds.setAttr(f'{n}.max{axe}', b)
        cmds.setAttr(f'{n}.oldMin{axe}', c)
        cmds.setAttr(f'{n}.oldMax{axe}', d)