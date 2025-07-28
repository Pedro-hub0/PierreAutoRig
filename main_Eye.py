
import maya.cmds as cmds
import sys
import os
import importlib


# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)

import modules.tools
import modules.smallUsefulFct

importlib.reload(modules.tools)
importlib.reload(modules.smallUsefulFct)



"""Script created by Pierre LIPPENS """

def create_window():
    """
    Create a window with a button.
    """
    # Check if the window already exists, and delete it if it does
    if cmds.window("w_Pierre_Cartoon_Eyes", exists=True):
        cmds.deleteUI("w_Pierre_Cartoon_Eyes", window=True)

    # Create the window
    window_name = cmds.window("w_Pierre_Cartoon_Eyes", title="Cartoon_Eyes_Pierre", widthHeight=(310, 150), sizeable=False)
    # Create a layout for the window
    column_layout= cmds.columnLayout(adjustableColumn=True)


    cmds.separator(h=8)
    cmds.text(label="Cartoon Eyes Pierre", font = "boldLabelFont" , w = 300, align = "center")
    cmds.separator(h=8)



    cmds.text(label=" - Select Edge or Curve ", w = 300, align = "left")
    cmds.separator(h=7)
    txt_nom_Centre = cmds.textField(placeholderText="Obj Centre")
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cmds.text(label="Nbr DrvJnt",w=150)
    int_DrvJnt = cmds.intField(value=5)
    cmds.setParent('..')
    cmds.separator(h=7)
    cmds.button(label='Create Eye Shit', command=lambda x:modules.tools.aimOnCurveAdapt(txt_nom_Centre,int_DrvJnt),width=150)
    cmds.button(label='Unit Ctrls', command=lambda x:modules.tools.UnitCtrls(),width=150)

    cmds.showWindow(window_name)
