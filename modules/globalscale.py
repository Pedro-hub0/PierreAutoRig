import maya.cmds as cmds
import smallUsefulFct
import math
import os
import importlib
importlib.reload(smallUsefulFct)

def CreateGlobal():
    if not cmds.objExists('GlobalMove'):
        raise ValueError("You need to finish your rig before ")
