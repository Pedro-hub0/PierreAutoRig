import maya.cmds as cmds
import smallUsefulFct
import math
import importlib
importlib.reload(smallUsefulFct)


###################################
###         MATCH IK FK        ####
###################################

def matchIkFk(value,txt_n):

    # Get the text entered in the field
    txt_namespace = cmds.textField(txt_n, query=True, text=True)
    if txt_namespace:
        txt_namespace=f"{txt_namespace}:"
    else:
        txt_namespace=""
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
        isIk=cmds.getAttr(f'{txt_namespace}CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk')
    else:
        isIk=value


    if objName == "Arm" :
        Fk_ctrl_Names=[f'{txt_namespace}CTRL_Fk_Shoulder_{side}',f'{txt_namespace}CTRL_Fk_Elbow_{side}',f'{txt_namespace}CTRL_Fk_Wrist_{side}']
        Fk_jnt_Names = [f'{txt_namespace}Fk_Shoulder_{side}',f'{txt_namespace}Fk_Elbow_{side}',f'{txt_namespace}Fk_Wrist_{side}']
        Ik_jnt_Names = [f'{txt_namespace}DrvJnt_Shoulder_{side}',f'{txt_namespace}DrvJnt_Elbow_{side}',f'{txt_namespace}DrvJnt_Wrist_{side}']
    elif objName == "Leg" :
        Fk_ctrl_Names=[f'{txt_namespace}CTRL_Fk_Leg_{side}',f'{txt_namespace}CTRL_Fk_Knee_{side}',f'{txt_namespace}CTRL_Fk_Foot_{side}']
        Fk_jnt_Names = [f'{txt_namespace}Fk_Leg_{side}',f'{txt_namespace}Fk_Knee_{side}',f'{txt_namespace}Fk_Ankle_{side}']
        Ik_jnt_Names = [f'{txt_namespace}DrvJnt_Leg_{side}',f'{txt_namespace}DrvJnt_Knee_{side}',f'{txt_namespace}DrvJnt_Ankle_{side}']
    else :
        raise ValueError("You need to select somethind that's end up by Arm_L or Leg_R for example ")
    
    #Transform
    rotate_Ik=[]
    rotate_Fk=[]
    translate_Ik=[]
    translate_Fk=[] 
    pv_Ctrl=f'{txt_namespace}Pv_{objName}_{side}'
    if objName == "Arm":
        ik_Ctrl=f'{txt_namespace}CTRL_Hand_{side}'
    if objName == "Leg":
        ik_Ctrl=f'{txt_namespace}CTRL_Foot_{side}'

    cmds.setAttr(f'{txt_namespace}CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk',1)
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
        test=cmds.getAttr(f'{txt_namespace}CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk')


        for i in range(0,len(Fk_ctrl_Names)):
            cmds.xform(Fk_ctrl_Names[i],rotation=rotate_Ik[i], worldSpace=True)

        cmds.setAttr(f'{txt_namespace}CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk',0)


    else:
        raise ValueError("Switch ik/Fk need to be 0 or 1")
        


def lockUnlock(cbMove,cbaxes,cbhide):
    # Assuming 'pCube1' is the name of your object
    cb_loc_Move=[]
    cb_loc_Axes=[]
    move=['translate','rotate','scale']
    selected =cmds.ls(selection=True)
    cbhide=cmds.checkBox(cbhide, query=True, value=True)
    for cb in cbMove:
        cb_loc_Move.append(cmds.checkBox(cb, query=True, value=True))

    for cb2 in cbaxes:
        cb_loc_Axes.append(cmds.checkBox(cb2, query=True, value=True))


    # Lock the translation attributes (X, Y, Z)
    for obj in selected:
        for ilock in range(0,len(cb_loc_Move)):
            if cb_loc_Move[ilock]:
                j=ilock*3
                cmds.setAttr(f'{obj}.{move[ilock]}X', lock=cb_loc_Axes[j])
                cmds.setAttr(f'{obj}.{move[ilock]}Y', lock=cb_loc_Axes[j+1])
                cmds.setAttr(f'{obj}.{move[ilock]}Z', lock=cb_loc_Axes[j+2])

                if cbhide:
                    cmds.setAttr(f'{obj}.{move[ilock]}X', keyable=False, channelBox=False)
                    cmds.setAttr(f'{obj}.{move[ilock]}Y', keyable=False, channelBox=False)
                    cmds.setAttr(f'{obj}.{move[ilock]}Z', keyable=False, channelBox=False)
                else:
                    cmds.setAttr(f'{obj}.{move[ilock]}X', keyable=True, channelBox=True)
                    cmds.setAttr(f'{obj}.{move[ilock]}Y', keyable=True, channelBox=True)
                    cmds.setAttr(f'{obj}.{move[ilock]}Z', keyable=True, channelBox=True)


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

def parentshapeScript(child_transform,parent_transform):

    # Get the shape of the child
    child_shape = cmds.listRelatives(child_transform, shapes=True, fullPath=True)[0]
    # Re-parent the shape to the new parent transform
    cmds.parent(child_shape, parent_transform, shape=True, relative=True)

    # Optionally, delete the old transform node (if it becomes empty after re-parenting)
    if not cmds.listRelatives(child_transform, children=True):
        cmds.delete(child_transform)



def selectJnt(name):
    pattern= name+"*"
    # Get all joints that match the pattern
    joints = cmds.ls(pattern, type="joint")

    # Select the found joints
    cmds.select(joints, r=True)

def LocScale():
    if not cmds.objExists("Loc_Echelle_01"):
        cmds.spaceLocator(name="Loc_Echelle_01")[0]
    if not cmds.objExists("Loc_Echelle_02"):
        cmds.spaceLocator(name="Loc_Echelle_02")[0]


def toggleRotateVisibilityFct(onOff):
    # Get a list of all joints in the scene
    all_joints = cmds.ls(type='joint')

    # Iterate through each joint
    for joint in all_joints:
        # Check if ToggleLocalRotationAxes is true for the current joint
        toggle_rotation_axes = cmds.getAttr(joint + ".displayLocalAxis")
        if cmds.objExists(joint):
            cmds.setAttr(joint + ".displayLocalAxis", onOff)


def CreateFollows():

    sides=['L','R']
    followElement=['CTRL_Root','CTRL_Torso']
        ### FOLLOW ###

    for side in sides:
    # Hand
        # Create Attribute
        # Generate enum names dynamically using a loop
        enum_names=':Global'
        for i in range(0, len(followElement)):
            enum_names =f"{enum_names}:{followElement[i].split('_')[-1]}" # Creates "Option1:Option2:Option3"

        if cmds.objExists(f'CTRL_Hand_{side}'):
            if not cmds.attributeQuery(f'______', node=f'CTRL_Hand_{side}', exists=True):
                cmds.addAttr(f'CTRL_Hand_{side}', longName='______', attributeType='enum', enumName='_____', defaultValue=0,keyable=True,niceName="___")
            
            if not cmds.attributeQuery(f'Follow', node=f'CTRL_Hand_{side}', exists=True):
                cmds.addAttr(f'CTRL_Hand_{side}', longName='Follow', attributeType='enum',enumName=f"{enum_names}", defaultValue=0,keyable=True)
        else:
            print(f'You don t have a CTRL_Hand_{side} \n ')
        
        
        # Create a Constraints
        for element in followElement:
            if not cmds.objExists(f"CTRL_Hand_{side}_Move_parentConstraint1.{element}W0"):
                tempCstr=cmds.parentConstraint(f"{element}",f'CTRL_Hand_{side}_Move',maintainOffset=True)[0]
            else:
                tempCstr=f"CTRL_Hand_{side}_Move_parentConstraint1"


        #Create Remaps
        # Global // Neutral Remap 
        remapFollow0 = cmds.createNode('remapValue', name=f'remapV_follow_Global_Hand_{side}')
        smallUsefulFct.initialiseRemap(remapFollow0,0,2,0,1)
        for j in range(0,len(followElement)):
            cmds.setAttr(f"{remapFollow0}.value[{j}].value_Position", 0)
            cmds.setAttr(f"{remapFollow0}.value[{j}].value_FloatValue",0)
            cmds.setAttr(f"{remapFollow0}.value[{j}].value_Interp", 1)

        # Others Remaps      
        for i in range(0,len(followElement)):
            if cmds.objExists(followElement[i]):
                remapFollow = cmds.createNode('remapValue', name=f'remapV_follow_{followElement[i]}_Hand_{side}')
                smallUsefulFct.initialiseRemap(remapFollow,0,2,0,1)

                for j in range(0,len(followElement)+1):
                    cmds.setAttr(f"{remapFollow}.value[{j}].value_Position", j*(1/(len(followElement))))
                    if j == i+1:x = 1 
                    else: x = 0
                    cmds.setAttr(f"{remapFollow}.value[{j}].value_FloatValue",x)
                    cmds.setAttr(f"{remapFollow}.value[{j}].value_Interp", 1)
                    
                cmds.connectAttr(f'CTRL_Hand_{side}.Follow',f'{remapFollow}.inputValue')
                cmds.connectAttr(f'{remapFollow}.outValue',f'{tempCstr}.{followElement[i]}W{i}')

            else:
                print(f'You don t have a {followElement[i]} \n ')

            # Put Value Constraint





        # Fk Epaule
        # Create Attribute
                # Create Attribute
        if cmds.objExists(f'CTRL_Fk_Shoulder_{side}'):
            if not cmds.attributeQuery(f'______', node=f'CTRL_Fk_Shoulder_{side}', exists=True):
                cmds.addAttr(f'CTRL_Fk_Shoulder_{side}', longName='______', attributeType='enum', enumName='_____', defaultValue=0,keyable=True,niceName="___")
            if not cmds.attributeQuery(f'Global', node=f'CTRL_Fk_Shoulder_{side}', exists=True):
                cmds.addAttr(f'CTRL_Fk_Shoulder_{side}', longName='Global', attributeType='float',min=0,max=1, defaultValue=0,keyable=True)
        
        else:
            print(f'You don t have a CTRL_Fk_Shoulder_{side} \n ')
        # Create a Constraint 
        tempCstr= f"CTRL_Fk_Shoulder_{side}_Move_orientConstraint1"
        # Put Value Constraint
        if cmds.objExists(tempCstr):
            cmds.connectAttr(f'CTRL_Fk_Shoulder_{side}.Global',f'{tempCstr}.CTRL_TorsoW0')
            
"""
    # Fk Neck
    # Create Attribute
            # Create Attribute
    if cmds.objExists(f'Ctrl_Bind_Neck_01'):
        if not cmds.attributeQuery(f'______', node=f'Ctrl_Bind_Neck_01', exists=True):
            cmds.addAttr(f'CTRL_Fk_Shoulder_{side}', longName='______', attributeType='enum', enumName='_____', defaultValue=0,keyable=True,niceName="___")
        if not cmds.attributeQuery(f'Global', node=f'Ctrl_Bind_Neck_01', exists=True):
            cmds.addAttr(f'CTRL_Fk_Shoulder_{side}', longName='Global', attributeType='float',min=0,max=1, defaultValue=0,keyable=True)
    
    else:
        print(f'You don t have a Ctrl_Bind_Neck_01 \n ')
    # Create a Constraint 
    tempCstr= f"CTRL_Fk_Shoulder_{side}_Move_orientConstraint1"
    # Put Value Constraint
    if cmds.objExists(tempCstr):
        cmds.connectAttr(f'CTRL_Fk_Shoulder_{side}.Global',f'{tempCstr}.CTRL_TorsoW0')
        

"""