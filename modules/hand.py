import maya.cmds as cmds
import smallUsefulFct
import math
import importlib
importlib.reload(smallUsefulFct)


####################
###     HAND   ####
####################
def locHand():
    selObj = cmds.ls(selection=True)
    if len(selObj) <1:
        raise ValueError("You need to select something which finish by L or R ")
    side=selObj[0][-1]
    Fingers=["thumb","index","middle","ring","pinky"]
    posHand= cmds.xform(f'Bind_Hand_{side}', query=True, translation=True, worldSpace=True)
    locHand=cmds.spaceLocator(n=f'Loc_Hand_{side}')
    cmds.xform(locHand, translation=posHand, worldSpace=True)  
    y=0
    for f in Fingers:
        for i in range(1,5):
            loc=cmds.spaceLocator(n=f'{f}_0{i}_{side}')
            cmds.xform(loc, translation=posHand, worldSpace=True)  
            if i==1:      
                cmds.parent(loc,locHand)
            else:
                cmds.parent(loc,f'{f}_0{i-1}_{side}')   
            moveNumber=(i,0,y)
            smallUsefulFct.move_object(loc,moveNumber,False)
        y+=1

def createHand():
    selObj = cmds.ls(selection=True)
    if len(selObj) <1:
        raise ValueError("You need to select something which finish by L or R ")
    side=selObj[0][-1]
    cmds.select(clear=True)
    Fingers=["thumb","index","middle","ring","pinky"]

    #Create Joints
    for f in Fingers:
        cmds.select(clear=True)
        for i in range(1,5):
            pos= cmds.xform(f'{f}_0{i}_{side}', query=True, translation=True, worldSpace=True)
            cmds.joint(n=f'Bind_{f}_0{i}_{side}',p=pos)
    
    #Parent To Bind Hand And Orient
    for f in Fingers:
        cmds.parent(f'Bind_{f}_01_{side}',f'Bind_Hand_{side}')
        #Orient joint -e  -oj xyz -secondaryAxisOrient xup -ch -zso;
        cmds.joint(f'Bind_{f}_01_{side}',e=True, oj='xyz', sao='xup', ch=True, zso=True)
        cmds.joint(f'Bind_{f}_04_{side}',e=True, oj='none', ch=True, zso=True)     
    #Parent Controllers
    #cmds.delete(f'Loc_Hand_{side}')
        # Check if the group exists
    if not cmds.objExists("Grp_temp_Locs") :
        cmds.group(empty=True, name="Grp_temp_Locs")
        
    if cmds.listRelatives(f'Loc_Hand_{side}', parent=True) == None:
        cmds.parent(f'Loc_Hand_{side}',"Grp_temp_Locs")


def ctrlHand():
    #Create Controllers + Move
    selObj = cmds.ls(selection=True)
    if len(selObj) <1:
        raise ValueError("You need to select something which finish by L or R ")
    side=selObj[0][-1]
    Fingers=["thumb","index","middle","ring","pinky"]
    CTRL_Hand=[]
    grp_Hand=f'grp_Hand_{side}'
    
    if not cmds.objExists(f'grp_Hand_{side}'):
        grp_Hand = cmds.group(empty=True, name=f'grp_Hand_{side}')

    y=0
    for f in Fingers:
        cmds.select(clear=True)
        for i in range(1,5):
            translateJnt= cmds.xform(f'Bind_{f}_0{i}_{side}', query=True, translation=True, worldSpace=True)
            rotateJnt= cmds.xform(f'Bind_{f}_0{i}_{side}', query=True, rotation=True, worldSpace=True)
            CTRL_Hand.append(cmds.circle(name=f'CTRL_{f}_0{i}_{side}',nr=[1,0,0],radius=0.5)[0])    
            cmds.xform(CTRL_Hand[y], translation=translateJnt, ro=rotateJnt, worldSpace=True)
            smallUsefulFct.offset(CTRL_Hand[y])
            cmds.orientConstraint(CTRL_Hand[y],f'Bind_{f}_0{i}_{side}', maintainOffset=True, weight=1)
            if i>1:
                cmds.parent(f'CTRL_{f}_0{i}_{side}_Offset',f'CTRL_{f}_0{i-1}_{side}') 
            y+=1
        cmds.parent(f'CTRL_{f}_01_{side}_Offset',grp_Hand)
    cmds.parent(grp_Hand,f'Bind_Hand_{side}')

def mirorHand(cb_jnt,cb_ctrl):
    cb_ctrl_val = cmds.checkBox(cb_ctrl, query=True, value=True)
    cb_jnt_val = cmds.checkBox(cb_jnt, query=True, value=True)

    selObj = cmds.ls(selection=True)
    side=selObj[0][-1]
    otherside = "R" if side == "L" else "L"
    if len(selObj) <=1:
        if side not in ["L","R"]: 
            raise ValueError("You need to select something which finish by L or R ")
    else:
            raise ValueError("You need to select just 1 thing which finish by L or R ")

    if cmds.objExists("Bind_Root"):
        tr_BindRoot = cmds.xform("Bind_Root", query=True, worldSpace=True, translation=True)
    else:
        raise ValueError("You need to create a Bind_Root")
    
    # Create a new group (folder)
    temp_grp01 = cmds.group(empty=True, name="temp_grp01")
    if not cmds.objExists("Grp_temp_Locs"):
        cmds.group(empty=True, name="Grp_temp_Locs")
    cmds.parent(temp_grp01,"Grp_temp_Locs")
    
    # Set the translation for the group
    cmds.xform(temp_grp01, worldSpace=True, translation=tr_BindRoot)

    cmds.parent(f"Loc_Hand_{side}",temp_grp01)
    temp_grp02=cmds.duplicate(temp_grp01,f=True)

 
    current_parent = cmds.listRelatives(temp_grp01, parent=True)[0]
    cmds.xform(temp_grp02[0].split("|")[-1], scale=[-1, 1, 1], worldSpace=True)
    #Change the last letter
    for n in reversed(temp_grp02):
        if n[-1] == side:
            newname=n[:-1] + otherside
            newname = newname.split("|")[-1]
            if cmds.objExists(n):
                cmds.rename(n, newname)
                n=newname

    
    #Parent
    cmds.parent(f"Loc_Hand_{side}",current_parent)
    cmds.parent(f"Loc_Hand_{otherside}",current_parent)
  
    #Delete Parent groupe
    cmds.delete(temp_grp01)
    cmds.delete(temp_grp02[0].split("|")[-1])
    #Use the last codes
    if cb_jnt_val:
        cmds.select(f"CTRL_IkFk_Arm_{otherside}")
        createHand()
    if cb_ctrl_val:
        cmds.select(f"CTRL_IkFk_Arm_{otherside}")
        ctrlHand()