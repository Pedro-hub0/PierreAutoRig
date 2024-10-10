import maya.cmds as cmds
import smallUsefulFct
import math
import os
import importlib
importlib.reload(smallUsefulFct)

locator_names = ["Loc_Eyelid_Down_L","Loc_Eyelid_Up_L","Loc_Eye_L","Loc_Jaw_Up_End","Loc_Teeth_Up","Loc_Jaw_Up_01","Loc_Jaw_down_End","Loc_Teeth_Down","Loc_Jaw_Down_01","Loc_Head_Pivot_02","Loc_Head_Pivot_01"]
joints_names = ["Bind_Eyelid_Down_L","Bind_Eyelid_Up_L","Bind_Eye_L","Bind_Jaw_Up_End","Bind_Teeth_Up","Bind_Jaw_Up_01","Bind_Jaw_Down_End","Bind_Teeth_Down","Bind_Jaw_Down_01","Bind_Head_Pivot_02","Bind_Head_Pivot_01"]
CTRL_names = ["CTRL_Eyelid_Down_L","CTRL_Head_01","CTRL_Head_02","CTRL_Skull"]
Folder_names = ["Master_Head_01","Master_Head_02","CTRL_Skull","Master_Skull"]



def CreatelocHeadStructure(cb_org):
    cb_org=cmds.checkBox(cb_org, query=True, value=True)
    for loc in locator_names:
        cmds.spaceLocator(name=loc)[0]
    
    if cb_org:
        #Organisation
        #In Eye Joint
        cmds.parent(locator_names[0],locator_names[2])
        cmds.parent(locator_names[1],locator_names[2])
        #In Jaw Up Joint
        cmds.parent(locator_names[2],locator_names[5])
        cmds.parent(locator_names[3],locator_names[5])
        cmds.parent(locator_names[4],locator_names[5])
        #In Jaw Down Joint
        cmds.parent(locator_names[6],locator_names[8])
        cmds.parent(locator_names[7],locator_names[8])
        #In Jaw Head Pivot 02 Joint
        cmds.parent(locator_names[5],locator_names[9])
        cmds.parent(locator_names[8],locator_names[9])
        #In Jaw Head Pivot 01 Joint
        cmds.parent(locator_names[9],locator_names[10])
    if cmds.objExists('Grp_temp_Locs'):   
        cmds.parent(locator_names[10],'Grp_temp_Locs')
    
def HeadStructure():
    ##Initialisation##
    IfBindNeck=cmds.objExists("Bind_neck_end")
    #Creation
    for i in range(len(joints_names)):
        tr_Loc=cmds.xform(locator_names[i], query=True, translation=True, worldSpace=True)
        cmds.select(clear=True)
        cmds.joint(n=f'{joints_names[i]}',p=tr_Loc)
        if not IfBindNeck and  i == (len(locator_names)-1):
            cmds.select(clear=True)
            cmds.joint(n=f'Bind_neck_end',p=tr_Loc)

            
    ##Organisation##
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

    # mirror Eyes
    jnt_eye_R = cmds.mirrorJoint(joints_names[2], mirrorYZ=True, mirrorBehavior=True, searchReplace=["_L", "_R"])
    
    ##Orientation##
    #joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;
    jntsHierarchy = cmds.listRelatives(joints_names[10], allDescendents=True)
    cmds.joint(joints_names[10], e=True, oj='xyz', sao='xup', ch=True, zso=True)  
    for j in  jntsHierarchy:
        ischild = cmds.listRelatives(j, children=True)
        if ischild == None:
            cmds.joint(j, e=True, oj='none', ch=True, zso=True)


    ##Move##
    offset_jnt_hdpiv01=smallUsefulFct.move(joints_names[10])
    if cmds.objExists('JNT'):
        cmds.parent(offset_jnt_hdpiv01,'JNT')
        cmds.parent(f'Bind_neck_end','JNT')