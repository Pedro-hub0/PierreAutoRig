import maya.cmds as cmds
import smallUsefulFct
import math
import os
import importlib
importlib.reload(smallUsefulFct)

locator_names = ["Loc_Eyelid_Down_L","Loc_Eyelid_Up_L","Loc_Eye_L","Loc_Jaw_Up_End","Loc_Teeth_Up","Loc_Jaw_Up_01","Loc_Jaw_down_End","Loc_Teeth_Down","Loc_Jaw_Down_01","Loc_Head_Pivot_02","Loc_Head_Pivot_01","Eye_End_L"]
joints_names = ["Bind_Eyelid_Down_End_L","Bind_Eyelid_Up_End_L","Bind_Eye_L","Bind_Jaw_Up_End","Bind_Teeth_Up","Bind_Jaw_Up_01","Bind_Jaw_Down_End","Bind_Teeth_Down","Bind_Jaw_Down_01","Bind_Head_Pivot_02","Bind_Head_Pivot_01","Bind_Eye_End_L"]



def CreatelocHeadStructure(cb_org):
    cb_org=cmds.checkBox(cb_org, query=True, value=True)
    for loc in locator_names:
        cmds.spaceLocator(name=loc)[0]

    if cb_org:
        #Organisation
        #In Eye Joint
        cmds.parent(locator_names[0],locator_names[2])
        cmds.parent(locator_names[1],locator_names[2])
        cmds.parent(locator_names[11],locator_names[2])
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
    Eyes=[]
    IfBindNeck=cmds.objExists("Bind_neck_end")
    #Creation
    for i in range(len(joints_names)):
        tr_Loc=cmds.xform(locator_names[i], query=True, translation=True, worldSpace=True)
        cmds.select(clear=True)
        cmds.joint(n=f'{joints_names[i]}',p=tr_Loc)
        if not IfBindNeck and  i == (len(locator_names)-1):
            cmds.select(clear=True)
            cmds.joint(n=f'Bind_neck_end',p=tr_Loc)
    cmds.select(clear=True)
    Eyes.append(cmds.duplicate(joints_names[2],returnRootsOnly=True)[0])
    Eyes[0]=cmds.rename(Eyes[0],"Bind_Eyelid_Down_L")
    cmds.select(clear=True)
    Eyes.append(cmds.duplicate(joints_names[2],returnRootsOnly=True)[0])
    Eyes[1]=cmds.rename(Eyes[1],"Bind_Eyelid_Up_L")
               
    ##Organisation##
    #In Eye Joint
    cmds.parent(joints_names[11],joints_names[2])
    #In Eyelid Up and Down Joint
    cmds.parent(joints_names[0],Eyes[0])
    cmds.parent(joints_names[1],Eyes[1])
    #In Jaw Up Joint
    cmds.parent(joints_names[2],joints_names[5])
    cmds.parent(joints_names[3],joints_names[5])
    cmds.parent(joints_names[4],joints_names[5])
    cmds.parent(Eyes[0],joints_names[5])
    cmds.parent(Eyes[1],joints_names[5])
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
    jnt_eyelid_Up_R = cmds.mirrorJoint(Eyes[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=["_L", "_R"])
    jnt_eyelid_dwn_R = cmds.mirrorJoint(Eyes[1], mirrorYZ=True, mirrorBehavior=True, searchReplace=["_L", "_R"])

    ##Orientation##
    #joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;
    jntsHierarchy = cmds.listRelatives(joints_names[10], allDescendents=True)
    cmds.joint(joints_names[10], e=True, oj='xyz', sao='yup', ch=True, zso=True)  
    for j in  jntsHierarchy:
        ischild = cmds.listRelatives(j, children=True)
        if ischild == None:
            cmds.joint(j, e=True, oj='none', ch=True, zso=True)


    ##Move##
    offset_jnt_hdpiv01=smallUsefulFct.move2(joints_names[10])
    offset_EyelidDwn=smallUsefulFct.hook2(Eyes[0])
    offset_EyelidUp=smallUsefulFct.hook2(Eyes[1])
    offset_EyelidUp=smallUsefulFct.hook2(jnt_eyelid_Up_R[0])
    offset_EyelidUp=smallUsefulFct.hook2(jnt_eyelid_dwn_R[0])

    if cmds.objExists('JNT'):
        cmds.parent(offset_jnt_hdpiv01,'JNT')
        cmds.parent(f'Bind_neck_end','JNT')

def CtrlHeadStructure(sz):

    ##Initialisation
    CTRLS_hierarchy = ["CTRL_Head_01","Master_Head_01","CTRL_Head_02","Master_Head_02","CTRL_Skull","Master_Skull"]
    jntConstraint=["Bind_Head_Pivot_01","Bind_Head_Pivot_02","Bind_Jaw_Up_01"]
    CTRL_names_Eyes=["CTRL_Eyelid_Down_L","CTRL_Eyelid_Up_L","CTRL_Eye_L","CTRL_Eyelid_Down_R","CTRL_Eyelid_Up_R","CTRL_Eye_R"]
    jnt_Eyes_names = ["Bind_Eyelid_Down_End_L","Bind_Eyelid_Up_End_L","Bind_Eye_L","Bind_Eyelid_Down_End_R","Bind_Eyelid_Up_End_R","Bind_Eye_R"]
    jnt_Eyes_names2 = ["Bind_Eyelid_Down_L","Bind_Eyelid_Up_L","Bind_Eye_L","Bind_Eyelid_Down_R","Bind_Eyelid_Up_R","Bind_Eye_R"]

    tr_Head01=cmds.xform('Bind_Head_Pivot_01', query=True, translation=True, worldSpace=True)
    tr_Head02=cmds.xform('Bind_Head_Pivot_02', query=True, translation=True, worldSpace=True)
    size=cmds.intField(sz, query=True, value=True)
    
    ##Creation
    for obj in CTRLS_hierarchy:
        if obj.split('_')[0] == "CTRL":
            cmds.circle(name=obj,radius=size,nr=[0,1,0])
        else:
            cmds.select(clear=True)  
            cmds.group(empty=True,name=obj)
        if obj[-1]=='2':
            cmds.xform(obj, translation=tr_Head02, worldSpace=True)
        else:
            cmds.xform(obj, translation=tr_Head01, worldSpace=True)

    for obj in CTRL_names_Eyes:
        cmds.circle(name=obj,radius=size/2,nr=[0,0,0])
    
    for i in range(len(jnt_Eyes_names)):
        tr=cmds.xform(jnt_Eyes_names[i], query=True, translation=True, worldSpace=True)
        if CTRL_names_Eyes[i].split("_")[1]==f"Eye":
            pos=[tr[0],tr[1],tr[2]+(size*2)]
        else:
            pos=tr
        cmds.xform(CTRL_names_Eyes[i], translation=pos, worldSpace=True)   

    ctrl_Eyes=cmds.circle(name='CTRL_Eyes',radius=size/2,nr=[0,0,0])[0]
    cmds.xform('CTRL_Eyes', translation=smallUsefulFct.get_translate_between('CTRL_Eye_R','CTRL_Eye_L'), worldSpace=True)   
    
    ##Organisation
    for i in range(len(CTRLS_hierarchy)-1,-1,-1): 
        if i>0:
            cmds.parent(CTRLS_hierarchy[i],CTRLS_hierarchy[i-1])
    
    # Eyes
    for eye in CTRL_names_Eyes: 
        cmds.parent(eye,"Master_Skull")

    cmds.parent(ctrl_Eyes,"Master_Skull") 
    cmds.parent(CTRL_names_Eyes[2],ctrl_Eyes)
    cmds.parent(CTRL_names_Eyes[5],ctrl_Eyes)

    
    ##Offset / Erase Transform
    for eye in CTRL_names_Eyes: 
        smallUsefulFct.hook2(eye)
    
    smallUsefulFct.move2(ctrl_Eyes)
    ctrl_head_offset=smallUsefulFct.move('CTRL_Head_01')

    
    ##Constraints
    # Head
    a=1
    for i in range(len(jntConstraint)):
        cmds.orientConstraint(CTRLS_hierarchy[a],jntConstraint[i], maintainOffset=True, weight=1)
        a=a+2

    # Eyes
    for i in range(len(CTRL_names_Eyes)):

        if not CTRL_names_Eyes[i].split("_")[1]==f"Eye":
            cmds.aimConstraint(CTRL_names_Eyes[i],f'{jnt_Eyes_names2[i]}_Hook',w=1,aim=[0,0,1],u=[0,1,0],wut=2,wu=[0,1,0],wuo=CTRL_names_Eyes[i], maintainOffset=True, weight=1)
        else:
            cmds.aimConstraint(CTRL_names_Eyes[i],f'{jnt_Eyes_names2[i]}',w=1,aim=[0,0,1],u=[0,1,0],wut=2,wu=[0,1,0],wuo=CTRL_names_Eyes[i],maintainOffset=True, weight=1)

    
    cmds.parent(ctrl_head_offset,'CTRL_Torso')
    