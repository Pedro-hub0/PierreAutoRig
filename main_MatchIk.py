
import maya.cmds as cmds
import sys
import os
import importlib

# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)

import modules.tools


importlib.reload(modules.tools)



"""Script created by Pierre LIPPENS """

def create_window():
    """
    Create a window with a button.
    """
    # Check if the window already exists, and delete it if it does
    if cmds.window("myWindow", exists=True):
        cmds.deleteUI("myWindow", window=True)

    # Create the window
    window_name = cmds.window("myWindow", title="PierreAutoRig01", widthHeight=(310, 100), sizeable=False)
    # Create a layout for the window
    column_layout= cmds.columnLayout(adjustableColumn=True)


    cmds.separator(h=8)
    cmds.text(label="TOOLS", font = "boldLabelFont" , w = 300, align = "center")
    cmds.separator(h=8)


    cmds.text(label=" Match Ik/Fk ", font = "boldLabelFont" , w = 300, align = "left")
    cmds.separator(h=5)
    # Create a text field
    txt_mamespace = cmds.textField(placeholderText="Namespace")
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[150, 75,75])
    cmds.button(label='Match Auto', command=lambda x:tools.matchIkFk(2,txt_mamespace),width=150)
    cmds.button(label='Fk/Ik', command=lambda x:tools.matchIkFk(0,txt_mamespace),width=75)
    cmds.button(label='Ik/Fk', command=lambda x:tools.matchIkFk(1,txt_mamespace),width=75)
    # Show the window
    cmds.showWindow(window_name)
