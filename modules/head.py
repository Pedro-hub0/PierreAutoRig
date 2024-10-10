import maya.cmds as cmds
import smallUsefulFct
import math
import os
import importlib
importlib.reload(smallUsefulFct)

def locHeadStructure():
    locator_names = ["Eyelid Up","Eyelid Up","Eye","Head_Pivot_01","Head_Pivot_02","Nind Jaw_down_01"]
    folder_names = ["Pivot_Ball_"+side, "Pivot_Toe_", "Pivot_Toe_Offset"]
    for name in locator_names:
        cmds.spaceLocator(name=name)[0]