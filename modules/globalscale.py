import maya.cmds as cmds
import smallUsefulFct
import math
import os
import importlib
importlib.reload(smallUsefulFct)

def CreateGlobal(sz):
    if not cmds.objExists('GlobalMove'):
        raise ValueError("You need to finish your rig before ")
    membres=['Shoulder','Elbow','Leg','Knee']
    lettres=['A','B','C','D','E']
    side={'L','R'}
    size=smallUsefulFct.GetDistLocScale(sz)*4
    grplGeneral=cmds.listRelatives('GlobalMove',parent=True)[0]

    #Create Ctrl
    ctrlGeneral=cmds.circle(name=f'CTRL_General',radius=size,nr=[0,1,0])[0]
    #Organiser
    cmds.parent(ctrlGeneral,grplGeneral)

    #Contraintes
    cmds.scaleConstraint(ctrlGeneral,'GlobalMove', maintainOffset=True, weight=1)
    cmds.parentConstraint(ctrlGeneral,'GlobalMove', maintainOffset=True, weight=1)
    for m in membres:
        for s in side:
            if cmds.objExists(f'Ctrl_Global_Ribbon_01_{m}_{s}'):
                cmds.scaleConstraint(ctrlGeneral,f'Ctrl_Global_Ribbon_01_{m}_{s}', maintainOffset=True, weight=1)

            for l in lettres:
                if cmds.objExists(f'Bind_Ribbon_{l}01_Move_{m}_{s}'):
                    cmds.scaleConstraint(ctrlGeneral,f'Bind_Ribbon_{l}01_Move_{m}_{s}', maintainOffset=True, weight=1)
    #Bind_Ribbon_A01_Move_Shoulder_L
    #Ctrl_Global_Ribbon_01_Shoulder_L


