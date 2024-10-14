import maya.cmds as cmds
import smallUsefulFct
import math


###################################
###         MATCH IK FK        ####
###################################

def matchIkFk(value):

    #INITIALISATIONS VARIABLES
        #Object
    selObj = cmds.ls(selection=True)
    obj=selObj[0]
        #Names
    parts = obj.split("_")
    lenName=len(parts)
    side=parts[lenName-1]
    objName=parts[lenName-2]



    isIk=value
    if value == 2:
        isIk=cmds.getAttr(f'CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk')
    else:
        isIk=value


    if objName == "Arm" :
        Fk_ctrl_Names=[f'CTRL_Fk_Shoulder_{side}',f'CTRL_Fk_Elbow_{side}',f'CTRL_Fk_Wrist_{side}']
        Fk_jnt_Names = [f'Fk_Shoulder_{side}',f'Fk_Elbow_{side}',f'Fk_Wrist_{side}']
        Ik_jnt_Names = [f'DrvJnt_Shoulder_{side}',f'DrvJnt_Elbow_{side}',f'DrvJnt_Wrist_{side}']
    elif objName == "Leg" :
        Fk_ctrl_Names=[f'CTRL_Fk_Leg_{side}',f'CTRL_Fk_Knee_{side}',f'CTRL_Fk_Foot_{side}']
        Fk_jnt_Names = [f'Fk_Leg_{side}',f'Fk_Knee_{side}',f'Fk_Ankle_{side}']
        Ik_jnt_Names = [f'DrvJnt_Leg_{side}',f'DrvJnt_Knee_{side}',f'DrvJnt_Ankle_{side}']
    else :
        raise ValueError("You need to select somethind that's end up by Arm_L or Leg_R for example ")
    
    #Transform
    rotate_Ik=[]
    rotate_Fk=[]
    translate_Ik=[]
    translate_Fk=[] 
    pv_Ctrl=f'Pv_{objName}_{side}'
    if objName == "Arm":
        ik_Ctrl=f'CTRL_Hand_{side}'
    if objName == "Leg":
        ik_Ctrl=f'CTRL_Foot_{side}'

    cmds.setAttr(f'CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk',1)
    #Copy transform
    smallUsefulFct.copy_rotation_to_list(Ik_jnt_Names,rotate_Ik)
    smallUsefulFct.copy_rotation_to_list(Fk_jnt_Names,rotate_Fk)
    smallUsefulFct.copy_translation_to_list(Ik_jnt_Names,translate_Ik)
    smallUsefulFct.copy_translation_to_list(Fk_jnt_Names,translate_Fk)

    if isIk ==1:
        #Transform Ik Ctrl to Jnt Fk Wrist
        cmds.xform(ik_Ctrl, translation=translate_Fk[2], rotation=rotate_Fk[2], worldSpace=True)
        #Translate Ik Pv to Jnt Fk Elbow
        cmds.xform(pv_Ctrl, translation=translate_Fk[1], worldSpace=True)
    elif isIk == 0:
        #Rotate Fk Ctrl to Jnt drvjnt Shoulder/Elbow/Wrist
        test=cmds.getAttr(f'CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk')


        for i in range(0,len(Fk_ctrl_Names)):
            cmds.xform(Fk_ctrl_Names[i],rotation=rotate_Ik[i], worldSpace=True)

        cmds.setAttr(f'CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk',0)


    else:
        raise ValueError("Switch ik/Fk need to be 0 or 1")
        


def lockUnlock(cb_loc_Translate,cb_loc_tx,cb_loc_ty,cb_loc_tz,cb_loc_Rotate,cb_loc_rx,cb_loc_ry,cb_loc_rz):
    # Assuming 'pCube1' is the name of your object
    selected =cmds.ls(selection=True)

    cb_loc_Translate=cmds.checkBox(cb_loc_Translate, query=True, value=True)
    cb_loc_tx       =cmds.checkBox(cb_loc_tx, query=True, value=True)  
    cb_loc_ty=cmds.checkBox(cb_loc_ty, query=True, value=True)
    cb_loc_tz=cmds.checkBox(cb_loc_tz, query=True, value=True)
    cb_loc_Rotate=cmds.checkBox(cb_loc_Rotate, query=True, value=True)
    cb_loc_rx=cmds.checkBox(cb_loc_rx, query=True, value=True)
    cb_loc_ry=cmds.checkBox(cb_loc_ry, query=True, value=True)
    cb_loc_rz=cmds.checkBox(cb_loc_rz, query=True, value=True)

    # Lock the translation attributes (X, Y, Z)
    for obj in selected:
        if cb_loc_Translate:
            
            cmds.setAttr(obj + ".translateX", lock=cb_loc_tx)
            cmds.setAttr(obj + ".translateY", lock=cb_loc_ty)
            cmds.setAttr(obj + ".translateZ", lock=cb_loc_tz)
        if cb_loc_Rotate :
            cmds.setAttr(obj + ".rotateX", lock=cb_loc_rx)
            cmds.setAttr(obj + ".rotateY", lock=cb_loc_ry)
            cmds.setAttr(obj + ".rotateZ", lock=cb_loc_rz)


def parentshape():
    selObj = cmds.ls(selection=True)
    if len(selObj)!=2:
        raise ValueError ("Select only 2 things")
    # Select the child and parent objects
    child_transform = selObj[0]  # The object with the shape you want to re-parent
    parent_transform =selObj[1]  # The transform you want to parent the shape to

    # Get the shape of the child
    child_shape = cmds.listRelatives(child_transform, shapes=True, fullPath=True)[0]
    parent_shape =cmds.listRelatives(parent_transform, shapes=True, fullPath=True)[0]
    # Re-parent the shape to the new parent transform
    cmds.parent(child_shape, parent_transform, shape=True, relative=True)

    # Optionally, delete the old transform node (if it becomes empty after re-parenting)
    if not cmds.listRelatives(child_transform, children=True):
        cmds.delete(child_transform)
    cmds.delete(parent_shape)
   
def selectJnt(name):
    pattern= name+"*"
    # Get all joints that match the pattern
    joints = cmds.ls(pattern, type="joint")

    # Select the found joints
    cmds.select(joints, r=True)