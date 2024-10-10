import maya.cmds as cmds
import smallUsefulFct
import math
import os
import importlib
importlib.reload(smallUsefulFct)

def locHeadStructure():
    #Initialisation
    locator_names = ["Loc_Eyelid_Down","Loc_Eyelid_Up","Loc_Eye","Loc_Jaw_Up_End","Loc_Teeth_Up","Loc_Jaw_Up_01","Loc_Jaw_down_End","Loc_Teeth_Down","Loc_Jaw_Down_01","Loc_Head_Pivot_02","Loc_Head_Pivot_01"]
    joints_names = ["Bind_Eyelid__Down","Bind_Eyelid_Up","Bind_Eye","Bind_Jaw_Up_End","Bind_Teeth_Up","Bind_Jaw_Up_01","Bind_Jaw_down_End","Bind_Teeth_Down","Bind_Jaw_Down 01","Bind_Head_Pivot_02","Bind_Head_Pivot_01"]
    IfBindNeck=cmds.objExists("Bind_neck_end")

    #Creation
    for i in range(len(locator_names)):
        cmds.spaceLocator(name=locator_names[i])[0]
        tr_Loc=cmds.xform(locator_names[i], query=True, translation=True, worldSpace=True)
        cmds.select(clear=True)
        cmds.joint(n=f'{joints_names[i]}',p=tr_Loc)
        if not IfBindNeck and  i == (len(locator_names)-1):
            cmds.joint(n=f'Bind_neck_end',p=tr_Loc)

            
    #Organisation
    #In Eye Joint
    cmds.parent(joints_names[0],joints_names[2])
    cmds.parent(joints_names[1],joints_names[2])
    #In Jaw Up Joint
    cmds.parent(joints_names[2],joints_names[5])
    cmds.parent(joints_names[3],joints_names[5])
    cmds.parent(joints_names[4],joints_names[5])
    #In Jaw Down Joint
    cmds.parent(joints_names[6],joints_names[8])
    cmds.parent(joints_names[7],joints_names[8])
    #In Jaw Head Pivot 02 Joint
    cmds.parent(joints_names[5],joints_names[9])
    cmds.parent(joints_names[8],joints_names[9])
    #In Jaw Head Pivot 01 Joint
    cmds.parent(joints_names[9],joints_names[10])


    #Orientation