import maya.cmds as cmds
import smallUsefulFct
import math
 
 ###################################
###       CREATE Clavicule     ####
###################################

def locClavicule():
    selObj = cmds.ls(selection=True)
    if len(selObj) <1:
        raise ValueError("You need to select just 1 thing which finish by L or R")
    side=selObj[0][-1]
    cmds.spaceLocator(name=f'Temp_Loc_Clav_{side}')[0]



    return


def createClavicule():
    selObj = cmds.ls(selection=True)
    side=selObj[0][-1]
    if len(selObj) <1:
        raise ValueError("You need to select just 1 thing which finish by L or R")
    ## Get the translation of the 2 futures Clavicules joints
    tr_Shoulder = cmds.xform(f'DrvJnt_Shoulder_{side}', query=True, translation=True, worldSpace=True)
    tr_Clav = cmds.xform(f'Temp_Loc_Clav_{side}', query=True, translation=True, worldSpace=True)
    grp_Ctrl_Clav='Grp_Ctrl_Clav'
    if not cmds.objExists(f"Grp_Ctrl_Clav"):
        grp_Ctrl_Clav=cmds.group(empty=True, name="Grp_Ctrl_Clav")
    grp_Ctrl="CTRL"
    cmds.select(clear=True)
    ## Create joints ##
    cmds.joint(n=f'Bind_Clavicule_01_{side}',p=tr_Clav)
    cmds.joint(n=f'Bind_Clavicule_End_{side}',p=tr_Shoulder)
    ## Color joints ##
    cmds.setAttr(f"Bind_Clavicule_End_{side}.overrideColor", 16)
    # Enable display override for the joint
    cmds.setAttr(f"Bind_Clavicule_01_{side}.overrideEnabled", 1)
    # Set the color to white (color index 16)
    cmds.setAttr(f"Bind_Clavicule_01_{side}.overrideColor", 16)
    # Enable display override for the joint
    cmds.setAttr(f"Bind_Clavicule_End_{side}.overrideEnabled", 1)
    # Set the color to white (color index 16)
    cmds.select(clear=True)

    #Freeze et Orient :
    cmds.makeIdentity(f'Bind_Clavicule_01_{side}',apply=True, rotate=True, translate=False, scale=False, normal=False)
    cmds.joint(f'Bind_Clavicule_01_{side}', e=True, oj='xyz', sao='xup', ch=True, zso=True)   
    cmds.joint(f'Bind_Clavicule_End_{side}', e=True, oj='none', ch=True, zso=True)

    ##Create Clavicule
    CtrlClav=cmds.circle(name=f'CTRL_Clavicle_{side}',nr=[0,0,1])[0]
    TranslateJnt = cmds.xform(f'Bind_Clavicule_01_{side}', q=True, t=True, ws=True)
    smallUsefulFct.set_curve_color(CtrlClav,28)
    cmds.xform(CtrlClav, t=TranslateJnt)

    ## Organise with move
    smallUsefulFct.move(f'Bind_Clavicule_01_{side}')
    smallUsefulFct.move(CtrlClav)

    ##Permit to have like a mirror effect
    if side=="R":
        cmds.xform(f'{CtrlClav}_Offset', scale=[-1, 1, 1], worldSpace=True)
    ##Put in folder

    ##Constraints CTRL
    cmds.orientConstraint(CtrlClav,f'Bind_Clavicule_01_{side}', maintainOffset=True, weight=1)    
    ##Constraints Attache Body
    or_Clav_Ik=cmds.orientConstraint(f'Bind_Clavicule_End_{side}',f'DrvJnt_Shoulder_{side}_Move' ,maintainOffset=True, weight=1)[0]    
    cmds.pointConstraint(f'Bind_Clavicule_End_{side}',f'DrvJnt_Shoulder_{side}_Move' ,maintainOffset=True, weight=1)    
    cmds.pointConstraint(f'Bind_Clavicule_End_{side}',f'CTRL_Fk_Shoulder_{side}_Move', maintainOffset=True, weight=1)    
    if cmds.objExists('CTRL_Torso'):
        cmds.orientConstraint(f'CTRL_Torso',f'CTRL_Fk_Shoulder_{side}_Move', maintainOffset=True, weight=1)    
    
    condition_node = cmds.createNode("condition", name=f'condition_Clav_{side}')
    cmds.setAttr(f'{condition_node}.colorIfTrueR',0)
    cmds.setAttr(f'{condition_node}.colorIfTrueG',0)
    cmds.setAttr(f'{condition_node}.colorIfTrueB',0)
    cmds.setAttr(f'{condition_node}.colorIfFalseR',1)
    cmds.setAttr(f'{condition_node}.colorIfFalseG',1)
    cmds.setAttr(f'{condition_node}.colorIfFalseB',1)
    cmds.connectAttr(f"CTRL_IkFk_Arm_{side}.Switch_Ik_Fk",f'{condition_node}.firstTerm')
    cmds.connectAttr(f'{condition_node}.outColorR',f'{or_Clav_Ik}.Bind_Clavicule_End_{side}W0')
    
    TempIkChain = cmds.listRelatives(selObj, allDescendents=True, type='joint') or []
    
    if cmds.objExists('Bind_Root'):
        SpineChain = cmds.listRelatives('Bind_Root', allDescendents=True, type='joint') or []
        LastSpine='Bind_Spine_01'
        for n in SpineChain:
            if 'Spine' in n:
                LastSpine=n
                break
        cmds.parent(f'Bind_Clavicule_01_{side}_Offset',LastSpine)

    ##Organiser 
    cmds.parent(f'{CtrlClav}_Offset',grp_Ctrl_Clav)

    if cmds.listRelatives(grp_Ctrl_Clav,parent=True) ==  None:  
        cmds.parent(grp_Ctrl_Clav,grp_Ctrl)

    return


def mirorClav(cb_jnt):
    cb_jnt_val = cmds.checkBox(cb_jnt, query=True, value=True)
    selObj = cmds.ls(selection=True)
    side=selObj[0][-1]
    otherside = "R" if side == "L" else "L"
    nameClav=f'Temp_Loc_Clav_{side}'
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

    cmds.parent(nameClav,temp_grp01)
    temp_grp02=cmds.duplicate(temp_grp01,f=True)

 
    current_parent = "Grp_temp_Locs"
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
    cmds.parent(nameClav,current_parent)
    cmds.parent(f"{nameClav[:-1]}{otherside}",current_parent)
  
    #Delete Parent groupe
    cmds.delete(temp_grp01)
    cmds.delete(temp_grp02[0].split("|")[-1])
    #Use the last codes

    if cb_jnt_val:
        cmds.select(f"CTRL_IkFk_Arm_{otherside}")
        createClavicule()