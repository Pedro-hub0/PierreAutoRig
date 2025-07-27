import maya.cmds as cmds
import math
import os
import sys
import importlib


# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)

import head
import smallUsefulFct

importlib.reload(smallUsefulFct)
importlib.reload(head)


###################################
###         MATCH IK FK        ####
###################################

def matchIkFk(value,txt_n):

    # Get the text entered in the field
    txt_namespace = cmds.textField(txt_n, query=True, text=True)
    selObj = cmds.ls(selection=True)
    obj=selObj[0]

    if txt_namespace:
        txt_namespace=f"{txt_namespace}:"
    else:
        if ":" in obj:
            parts = obj.split(":") 
            txt_namespace = f'{parts[0]}:'
        else:
            txt_namespace=""
    #INITIALISATIONS VARIABLES
        #Object

    ##Find namespace     ##
    ##if ":" in obj:
    # parts = obj.split(":") ##
    # namespace = f'{parts}:'
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
    #if cmds.objExists(f'Dummy_Loc_{objName}_{side}'):
    #    Dummy_Translate=cmds.xform(f'Dummy_Loc_{objName}_{side}', q=True, t=True, ws=True)

    if isIk ==1:
        #Transform Ik Ctrl to Jnt Fk Wrist
        cmds.xform(ik_Ctrl, translation=translate_Fk[2], rotation=rotate_Fk[2], worldSpace=True)
        #Translate Ik Pv to Jnt Fk Elbow
        #if cmds.objExists(f'Dummy_Loc_{objName}_{side}'):
        #    cmds.xform(pv_Ctrl, translation=Dummy_Translate, worldSpace=True)
        #else:
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



def selectJnt(name,isOk,cb_notTheFirst):
    selObj = cmds.ls(selection=True)
    notfirst=cmds.checkBox(cb_notTheFirst, query=True, value=True)
    if notfirst:del selObj[0] 
    if name !="bind":
        name=cmds.textField(name, query=True, text=True)
    if len(selObj)<1:

        pattern= name+"*"
        if isOk:
            # Get all joints that match the pattern
            joints = cmds.ls(pattern, type="joint")
        else:
            joints = cmds.ls(pattern) 

        # Select the found joints
        cmds.select(joints, r=True)
    else:
        for sel in selObj:
            if cmds.objectType(sel)!= "joint":
                cmds.select(sel, deselect=True)
            all_joints = cmds.listRelatives(sel, allDescendents=True, type="joint")
            bind_joints = [joint for joint in all_joints if name in joint.lower()]
            current_selection = cmds.ls(selection=True)
            cmds.select(current_selection+bind_joints, r=True)

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
    CTRL_Element=['Hand','Foot']
    CTRL_Element_PV=['Arm','Leg']
    LastCtrlNeck=head.lastCTRLneck()
    flws=[]
    flws.append(FollowElement('Ctrl_Bind_Neck_01','CTRL_Torso'))
    flws.append(FollowElement('CTRL_Head_01',f'{LastCtrlNeck}'))

        ### FOLLOW ###

    for side in sides:
        for Ctrls in CTRL_Element:
            # Create Attribute
            # Generate enum names dynamically using a loop
            enum_names=':Global'
            for i in range(0, len(followElement)):
                enum_names =f"{enum_names}:{followElement[i].split('_')[-1]}" # Creates "Option1:Option2:Option3"

            if cmds.objExists(f'CTRL_{Ctrls}_{side}'):
                if not cmds.attributeQuery(f'______', node=f'CTRL_{Ctrls}_{side}', exists=True):
                    cmds.addAttr(f'CTRL_{Ctrls}_{side}', longName='______', attributeType='enum', enumName='_____', defaultValue=0,keyable=True,niceName="___")
                
                if not cmds.attributeQuery(f'Follow', node=f'CTRL_{Ctrls}_{side}', exists=True):
                    cmds.addAttr(f'CTRL_{Ctrls}_{side}', longName='Follow', attributeType='enum',enumName=f"{enum_names}", defaultValue=0,keyable=True)
            else:
                print(f'You don t have a CTRL_{Ctrls}_{side} \n ')
            
            # Create a Constraints
            for element in followElement:
                if not cmds.objExists(f"CTRL_{Ctrls}_{side}_Move_parentConstraint1.{element}W0"):
                    tempCstr=cmds.parentConstraint(f"{element}",f'CTRL_{Ctrls}_{side}_Move',maintainOffset=True)[0]
                else:
                    tempCstr=f"CTRL_{Ctrls}_{side}_Move_parentConstraint1"

            #Create Remaps
            # Global // Neutral Remap 
            if not cmds.objExists(f'remapV_follow_Global_{Ctrls}_{side}'):
                remapFollow0 = cmds.createNode('remapValue', name=f'remapV_follow_Global_{Ctrls}_{side}')
                smallUsefulFct.initialiseRemap(remapFollow0,0,2,0,1)
                for j in range(0,len(followElement)):
                    cmds.setAttr(f"{remapFollow0}.value[{j}].value_Position", 0)
                    cmds.setAttr(f"{remapFollow0}.value[{j}].value_FloatValue",0)
                    cmds.setAttr(f"{remapFollow0}.value[{j}].value_Interp", 1)

            # Others Remaps      
            for i in range(0,len(followElement)):
                if cmds.objExists(followElement[i]):
                    if not cmds.objExists(f'remapV_follow_{followElement[i]}_{Ctrls}_{side}'):
                        remapFollow = cmds.createNode('remapValue', name=f'remapV_follow_{followElement[i]}_{Ctrls}_{side}')
                        smallUsefulFct.initialiseRemap(remapFollow,0,2,0,1)
                        for j in range(0,len(followElement)+1):
                            cmds.setAttr(f"{remapFollow}.value[{j}].value_Position", j*(1/(len(followElement))))
                            if j == i+1:x = 1 
                            else: x = 0
                            cmds.setAttr(f"{remapFollow}.value[{j}].value_FloatValue",x)
                            cmds.setAttr(f"{remapFollow}.value[{j}].value_Interp", 1)
                    else:
                        remapFollow=f'remapV_follow_{followElement[i]}_{Ctrls}_{side}'
                    if not cmds.listConnections(f'{remapFollow}.inputValue', source=True, destination=False):
                        cmds.connectAttr(f'CTRL_{Ctrls}_{side}.Follow',f'{remapFollow}.inputValue')
                        cmds.connectAttr(f'{remapFollow}.outValue',f'{tempCstr}.{followElement[i]}W{i}')

                else:
                    print(f'You don t have a {followElement[i]} \n ')

        ### Pole Vectors ####
            
        # Create Attribute
                # Create Attribute
        for i in range(0,len(CTRL_Element_PV)):
            if cmds.objExists(f'Pv_{CTRL_Element_PV[i]}_{side}'):
                if not cmds.attributeQuery(f'______', node=f'Pv_{CTRL_Element_PV[i]}_{side}', exists=True):
                    cmds.addAttr(f'Pv_{CTRL_Element_PV[i]}_{side}', longName='______', attributeType='enum', enumName='_____', defaultValue=0,keyable=True,niceName="___")
                if not cmds.attributeQuery(f'Global', node=f'Pv_{CTRL_Element_PV[i]}_{side}', exists=True):
                    cmds.addAttr(f'Pv_{CTRL_Element_PV[i]}_{side}', longName='Global', attributeType='float',min=0,max=1, defaultValue=1,keyable=True)
            
            else:
                print(f'You don t have a Pv_{CTRL_Element_PV[i]}_{side} \n ')
            # Create a Constraint 
            if not cmds.objExists(f"Pv_{CTRL_Element_PV[i]}_{side}_Move_parentConstraint1.CTRL_{CTRL_Element[i]}_{side}W0"):
                tempCstr2=cmds.parentConstraint(f"CTRL_{CTRL_Element[i]}_{side}",f'Pv_{CTRL_Element_PV[i]}_{side}_Move',maintainOffset=True)[0]
            else:
                tempCstr2=f"Pv_{CTRL_Element_PV[i]}_{side}_Move_parentConstraint1"
            # Put Value Constraint
            if cmds.objExists(tempCstr):
                if not cmds.listConnections(f"Pv_{CTRL_Element_PV[i]}_{side}_Move_parentConstraint1.CTRL_{CTRL_Element[i]}_{side}W0", source=True, destination=False):
                    cmds.connectAttr(f'Pv_{CTRL_Element_PV[i]}_{side}.Global',f"Pv_{CTRL_Element_PV[i]}_{side}_Move_parentConstraint1.CTRL_{CTRL_Element[i]}_{side}W0")
                





        # Fk Epaule
        # Create Attribute
                # Create Attribute
        if cmds.objExists(f'CTRL_Fk_Shoulder_{side}'):
            if not cmds.attributeQuery(f'______', node=f'CTRL_Fk_Shoulder_{side}', exists=True):
                cmds.addAttr(f'CTRL_Fk_Shoulder_{side}', longName='______', attributeType='enum', enumName='_____', defaultValue=0,keyable=True,niceName="___")
            if not cmds.attributeQuery(f'Global', node=f'CTRL_Fk_Shoulder_{side}', exists=True):
                cmds.addAttr(f'CTRL_Fk_Shoulder_{side}', longName='Global', attributeType='float',min=0,max=1, defaultValue=1,keyable=True)
        
        else:
            print(f'You don t have a CTRL_Fk_Shoulder_{side} \n ')
        # Create a Constraint 
        tempCstr= f"CTRL_Fk_Shoulder_{side}_Move_orientConstraint1"
        # Put Value Constraint
        if cmds.objExists(tempCstr):
            if not cmds.listConnections(f'{tempCstr}.CTRL_TorsoW0', source=True, destination=False):
                cmds.connectAttr(f'CTRL_Fk_Shoulder_{side}.Global',f'{tempCstr}.CTRL_TorsoW0')
            

    # Fk Neck / Head (followGlobalElements)
    for i in range(0,len(flws)-1):
        # Create Attribute
                # Create Attribute
        if cmds.objExists(f'{flws[i].follower}'):
            if not cmds.attributeQuery(f'______', node=f'{flws[i].follower}', exists=True):
                cmds.addAttr(f'{flws[i].follower}', longName='______', attributeType='enum', enumName='_____', defaultValue=0,keyable=True,niceName="___")
            if not cmds.attributeQuery(f'Global', node=f'{flws[i].follower}', exists=True):
                cmds.addAttr(f'{flws[i].follower}', longName='Global', attributeType='float',min=0,max=1, defaultValue=1,keyable=True)
        
        else:
            print(f'You don t have a {flws[i].follower} \n ')
        # Create a Constraint 
        tempCstr= f"{flws[i].follower}_Move_orientConstraint1"
        # Put Value Constraint
        if cmds.objExists(tempCstr):
            cmds.connectAttr(f'{flws[i].follower}.Global',f'{tempCstr}.{flws[i].follow}W0')
            
def CtrlParentCreate(cbcstr,sz):
    sz=smallUsefulFct.GetDistLocScale(sz)
    selObj = cmds.ls(selection=True)
    checkboxs=[]
    for cb in cbcstr:
        checkboxs.append(cmds.checkBox(cb, query=True, value=True))
    
    for sel in selObj:
        Ctrl=cmds.circle(name=f'Ctrl_{sel}',nr=[1,0,0],radius=sz)[0]     
        tr_Sel=cmds.xform(sel,translation=True, query=True, worldSpace=True)
        ro_Sel=cmds.xform(sel,rotation=True, query=True, worldSpace=True)
        if checkboxs[5]:
            cmds.matchTransform(Ctrl,sel)  
        cmds.matchTransform(Ctrl,sel,rotation=False)         
        if checkboxs[0]:
            cmds.parentConstraint(Ctrl,sel, maintainOffset=True, weight=1)
        if checkboxs[1]:
            cmds.pointConstraint(Ctrl,sel, maintainOffset=True, weight=1)
        if checkboxs[2]:
            cmds.orientConstraint(Ctrl,sel, maintainOffset=True, weight=1)
        if checkboxs[3]:
            smallUsefulFct.move2(Ctrl)
        if checkboxs[4]:
            smallUsefulFct.offset2(Ctrl)

class FollowElement:
    def __init__(self, follower, follow):
        self.follower = follower
        self.follow = follow
def findType(var):
    EnmuName=["Scene Up","Object Up","Object Rotation Up","Vector","Normal"]
    FinalName=["scene","object","objectrotation","vector","normal"]
    
    for i in range(0,len(EnmuName)):
        if var==EnmuName[i]:
            return FinalName[i]



def PathJointContraint(cbnbjoint,cbName,cbType,cbobjUp,cbFollow):
    typeBrute=cmds.optionMenu(cbType, query=True, value=True)
    vartype=findType(typeBrute)
    objUp= cmds.textField(cbobjUp, query=True, text=True)
    selObj = cmds.ls(selection=True)
    nbrJnt=cmds.intField(cbnbjoint, query=True, value=True)

    name=cmds.textField(cbName, query=True, text=True)
    grp = cmds.group(empty=True, name=f'Grp_{name}')
    follow=cmds.checkBox(cbFollow, query=True, value=True)
    if follow:
        nbfollow=1
    else:nbfollow=0
    # Attach the joint to the motion path
    for i in range(0,nbrJnt):
        # Create a joint
        cmds.select(clear=True)
        joint = cmds.joint(name=f"{name}")
        if objUp == "":
            motion_path_node = cmds.pathAnimation(joint, c=selObj[0], name=f"{name}_motionPath",                
            fractionMode=True,
            follow=True,
            followAxis="x",
            upAxis="y",
            worldUpType=vartype,
            worldUpVector=(0, 1, 0),
            inverseUp=False,
            inverseFront=False,
            bank=False)

        else:
            motion_path_node = cmds.pathAnimation(joint, c=selObj[0], name=f"{name}_motionPath",                
                    fractionMode=True,
                    follow=True,
                    followAxis="x",
                    upAxis="y",
                    worldUpType=vartype,
                    worldUpVector=(0, 1, 0),
                    worldUpObject=objUp,
                    inverseUp=False,
                    inverseFront=False,
                    bank=False)
        cmds.setAttr(f"{motion_path_node}.follow", nbfollow)  # Enable follow
        # Delete the keyframes on the uValue
        cmds.cutKey(motion_path_node, attribute="uValue", clear=True)

        # Set the joint at a specific position along the curve
        # uValue ranges from 0 (start of curve) to 1 (end of curve)
        position_on_curve = i*(1/(nbrJnt-1))  # Change this value to move the joint
        cmds.setAttr(f"{motion_path_node}.uValue", position_on_curve)


        # Optional: Configure front axis and up axis if needed
        cmds.setAttr(f"{motion_path_node}.frontAxis", 0)  # X-axis
        cmds.setAttr(f"{motion_path_node}.upAxis", 1)     # Y-axis
        cmds.parent(joint,grp)

def Cstr(type,choix):
    selObj = cmds.ls(selection=True)
    checkboxs=[]
    for cb in type:
        checkboxs.append(cmds.checkBox(cb, query=True, value=True))
    if choix==0:
        for i in range(1,len(selObj)):
            if cmds.objExists(f'{selObj[i]}'):
                if checkboxs[3]:
                    cmds.scaleConstraint(selObj[0],f'{selObj[i]}', maintainOffset=True, weight=1)
                if checkboxs[0]:
                    cmds.parentConstraint(selObj[0],f'{selObj[i]}', maintainOffset=True, weight=1)
                if checkboxs[1]:
                    cmds.pointConstraint(selObj[0],f'{selObj[i]}', maintainOffset=True, weight=1)
                if checkboxs[2]:
                    cmds.orientConstraint(selObj[0],f'{selObj[i]}', maintainOffset=True, weight=1)
                if checkboxs[4]:
                    cmds.aimConstraint(selObj[0],f'{selObj[i]}', maintainOffset=True, weight=1)   
                if checkboxs[5]:
                    cmds.parentConstraint(selObj[0],f'{selObj[i]}', maintainOffset=True,skipTranslate=["x", "y", "z"], weight=1)
                if checkboxs[6]:
                    cmds.parent(selObj[i],f'{selObj[i+1]}')
                    
    if choix==1:
        if len(selObj)%2 == 0:
            i=0
            while i < len(selObj):
                if cmds.objExists(f'{selObj[i+1]}'):
                    if checkboxs[0]:
                        cmds.parentConstraint(selObj[i],f'{selObj[i+1]}', maintainOffset=True, weight=1)
                    if checkboxs[1]:
                        cmds.pointConstraint(selObj[i],f'{selObj[i+1]}', maintainOffset=True, weight=1)
                    if checkboxs[2]:
                        cmds.orientConstraint(selObj[i],f'{selObj[i+1]}', maintainOffset=True, weight=1)
                    if checkboxs[3]:
                        cmds.scaleConstraint(selObj[i],f'{selObj[i+1]}', maintainOffset=True, weight=1)
                    if checkboxs[4]:
                        cmds.aimConstraint(selObj[i],f'{selObj[i+1]}', maintainOffset=True, weight=1)
                    if checkboxs[5]:
                        cmds.parentConstraint(selObj[i],f'{selObj[i+1]}', maintainOffset=True,skipTranslate=["x", "y", "z"], weight=1)
                    if checkboxs[6]:
                        cmds.parent(selObj[i],f'{selObj[i+1]}')
                i=i+2
    
def JntOnCurve_Poc(l,nbPath,v_obj_On_Curve):

   
    selection=cmds.ls(selection=True)
    CurveUp=selection[0]

    if not isinstance(l, int):
        length=cmds.intField(l, query=True, value=True)
    else:
        length=l
    if not isinstance(nbPath, int):
        nbPathv=cmds.intField(nbPath, query=True, value=True)   
    else:
        nbPathv=nbPath  
    if "|" in v_obj_On_Curve:
        v_obj_On_Curve=cmds.optionMenu(v_obj_On_Curve, query=True, value=True)



    pocUp=[]
    JntUp=[]
 
    for y in range(0,len(selection)):
        CurveUp=selection[y]
        size=y*length
        ##Organise
        grp_JntsUp = cmds.group(empty=True, name=f"grp_{v_obj_On_Curve}_{CurveUp}")

        ### Init of the first Object at 0
        #if v_obj_On_Curve=="Joints":
        #    JntUp.append(cmds.joint(n=f'Bind_{CurveUp}_00'))
        #if v_obj_On_Curve=="Locator":
        #    JntUp.append(cmds.spaceLocator(name=f'Loc_{CurveUp}_00')[0])
        #pocUp.append(cmds.createNode('pointOnCurveInfo', name=f'{CurveUp}_PocUp_00'))
        #cmds.connectAttr(f'{CurveUp}.worldSpace[0]',f'{pocUp[size]}.inputCurve')
        #cmds.setAttr(f"{pocUp[size]}.parameter",0)


        for i in range(1,length+1):
            pocUp.append(cmds.createNode('pointOnCurveInfo', name=f'{CurveUp}_PocUp_0{i}'))
            cmds.select(clear=True)
            if v_obj_On_Curve=="Joints":
                JntUp.append(cmds.joint(n=f'Bind_{CurveUp}_0{i}'))
            if v_obj_On_Curve=="Locator":
                JntUp.append(cmds.spaceLocator(name=f'Loc_{CurveUp}_0{i}')[0])
            
            cmds.parent(JntUp[size+i-1],grp_JntsUp)
            smallUsefulFct.move2(JntUp[size+i-1])

            val3=(i-1)*(1/(length-1))*(nbPathv)         

            cmds.connectAttr(f'{CurveUp}.worldSpace[0]',f'{pocUp[size+i-1]}.inputCurve')
            cmds.setAttr(f"{pocUp[size+i-1]}.parameter",val3)

            #Connect to joints

            cmds.connectAttr(f'{pocUp[size+i-1]}.position',f'{JntUp[size+i-1]}_Move.translate')

    return JntUp
    





def initialiseRemap(n,a,b,c,d,axe):
        cmds.setAttr(f'{n}.min{axe}', a)
        cmds.setAttr(f'{n}.max{axe}', b)
        cmds.setAttr(f'{n}.oldMin{axe}', c)
        cmds.setAttr(f'{n}.oldMax{axe}', d)

def renameRiv(n):
    selObj = cmds.ls(selection=True)
    for i in range(0,len(selObj)):
        cmds.rename(selObj[i],f'{n}_0{i+1}')


def aimOnCurveAdapt(txt,cbPath,cbType,cbobjUp):
    ## Initialise and Check the variable
    nbPathv=cmds.intField(cbPath, query=True, value=True)   
    selObj = cmds.ls(selection=True)
    txt=cmds.textField(txt,query=True, text=True)
    LocCenter=[]
    typeBrute=cmds.optionMenu(cbType, query=True, value=True)
    vartype=findType(typeBrute)
    objUp= cmds.textField(cbobjUp, query=True, text=True)
    print(f' OBJ Up {objUp}    TYPE {vartype}')
    ##Orga
    grp_LocCenter = cmds.group(empty=True, name=f"grp_Loc_Center_{selObj[0]}")
    grp_LocEyelash = cmds.group(empty=True, name=f"grp_Loc_onJnt_{selObj[0]}")
    grp_sysCrvAim = cmds.group(empty=True, name=f"grp_LSysCrvAim_{selObj[0]}")
    cmds.parent([grp_LocCenter,grp_LocEyelash],grp_sysCrvAim)

    #Is it a Curve
    shapeNode = cmds.listRelatives(selObj[0], shapes=True)
    if cmds.objectType(shapeNode[0]) not in ["nurbsCurve","bezierCurve"]:
        raise ValueError("The first selection need to be a curve")
    else:
        curve=selObj[0]
    if not cmds.objExists(txt):
        raise ValueError(f"{txt} Not Exist")
    else:
        objCentre=txt

    ##Create Loc on Curve
    cmds.select(selObj[0])

    locs=JntOnCurve_Poc(len(selObj)-1,nbPathv,'Locator')

    print(f'DIST JNT LOC {smallUsefulFct.getDistBetweenJnts(locs[0],selObj[1])}    {smallUsefulFct.getDistBetweenJnts(locs[0],selObj[len(selObj)-1])}')
    ##Loc on Jnt 
    if smallUsefulFct.getDistBetweenJnts(locs[0],selObj[1])<smallUsefulFct.getDistBetweenJnts(locs[0],selObj[len(selObj)-1]):
        for i in range(0,len(locs)):

            cmds.matchTransform(locs[i],selObj[i+1], position=True)
            tr=cmds.xform(txt,t=True,q=True,ws=True)
            #Creation of loc in the center of the obj selected
            LocCenter.append(cmds.spaceLocator(name=f'Loc_{selObj[i+1]}')[0])
            cmds.xform(LocCenter[i], t=tr,ws=True)
            #Creation of the constraints which link the center to the others element
            cmds.orientConstraint(LocCenter[i],selObj[i+1])
            if objUp == "":
                print("KesKe Je Fou la")
                cmds.aimConstraint(
                    locs[i],LocCenter[i],
                    aimVector=(1, 0, 0), 
                    upVector=(0, 1, 0), 
                    worldUpType=vartype, 
                    worldUpVector=(0, 1, 0),
                    maintainOffset=True)
            else:
                print("Ah BAh Chui Au bon endroit")
                cmds.aimConstraint(
                    locs[i],LocCenter[i],
                    aimVector=(1, 0, 0), 
                    upVector=(0, 1, 0), 
                    worldUpType=vartype, 
                    worldUpVector=(0, 1, 0),
                    maintainOffset=True,
                    worldUpObject=objUp)
                    

            cmds.parent(f'{locs[i]}_Offset',grp_LocEyelash)


    else:
        y=len(locs)
        for i in range(0,len(locs)):
            cmds.matchTransform( locs[y-1],selObj[i+1], position=True)
            tr=cmds.xform(txt,t=True,q=True,ws=True)
            #Creation of loc in the center of the obj selected
            LocCenter.append(cmds.spaceLocator(name=f'Loc_{selObj[i+1]}')[0])
            cmds.xform(LocCenter[i], t=tr,ws=True)
            #Creation of the constraints which link the center to the others element
            cmds.orientConstraint(LocCenter[i],selObj[i+1])
            if objUp == "":
                print("KesKe Je Fou la")
                cmds.aimConstraint(
                    locs[i],LocCenter[i],
                    aimVector=(1, 0, 0), 
                    upVector=(0, 1, 0), 
                    worldUpType=vartype, 
                    worldUpVector=(0, 1, 0),
                    maintainOffset=True)
            else:
                print("Ah BAh Chui Au bon endroit")
                cmds.aimConstraint(
                    locs[i],LocCenter[i],
                    aimVector=(1, 0, 0), 
                    upVector=(0, 1, 0), 
                    worldUpType=vartype, 
                    worldUpVector=(0, 1, 0),
                    maintainOffset=True,
                    worldUpObject=objUp)
            cmds.parent(f'{locs[i]}_Offset',grp_LocEyelash)
            y=y-1

    cmds.parent(LocCenter,grp_LocCenter)










###### POSITIONS Automatique ######
def bboxsize(sel):
    bbox = cmds.exactWorldBoundingBox(sel[0])

    width = bbox[3] - bbox[0]   # X size
    height = bbox[4] - bbox[1]  # Y size
    depth = bbox[5] - bbox[2]   # Z size
    size=[width,height,depth]
    return size

def multTab(tab,valeur):
    newTab=[]
    for t in tab:
        newTab.append(t*valeur)
    return newTab

def getTranslatePosition(nom,sel):
    h=bboxsize(sel)[1]/AdultePos.get_position('ratio')
    t=AdultePos.get_position(nom)
    result=multTab(t,h)
    return result




class Positions:
    def __init__(self,ratio, root, shoulder, arm, elbow, hand, hip, knee, foot, ball, toe, heel, bank_int, bank_ext, clavicle,head01,head02,JawUp,JawDwn,Eye,EyelidUp,EyelidDwn):
        """Initialize positions with fully custom values."""
        self.positions = {
            "ratio":ratio,

            "root": root,
            "shoulder": shoulder,

            "arm": arm,
            "elbow": elbow,
            "hand": hand,

            "hip": hip,
            "knee": knee,
            "foot": foot,

            "ball": ball,
            "toe": toe,
            "heel": heel,
            "bank_int": bank_int,
            "bank_ext": bank_ext,
            "clavicle": clavicle,

            "head01": head01,
            "head02": head02,
            "JawUp": JawUp,
            "JawDwn": JawDwn,
            "Eye": Eye,
            "EyelidUp":EyelidUp,
            "EyelidDwn":EyelidDwn

        }
    
    def get_position(self, name):
        """Returns the position of the requested joint."""
        return self.positions.get(name, None)




AdultePos=Positions(    
    ratio=8.0,

    root= [0.0,4.35,0.0],
    shoulder= [0.0,6.7,0.0],

    arm=    [1.0,6.5,-0.2],
    elbow=  [2.5,6.5,-0.2],
    hand=   [3.5,6.5,-0.2],

    hip=[0.4,4.2,0.0],
    knee= [0.4,2.0,0.0],
    foot= [0.4,0.3,0.0],

    ball= [0.4,0.1,0.65],
    toe= [0.4,0.1,1],
    heel=[0.4,0,0],
    bank_int=[0.2,0,0.5],
    bank_ext=[0.7,0,0.5],

    
    clavicle=[0.5,6.5,0.2],


    head01=   [0.0,7.2,-0.26],
    head02=   [0.0,7.15,-0.20],
    JawUp=    [0.0,7.15,0.5],
    JawDwn=   [0.0,6.9,0.42],
    Eye=      [0.15,7.38,0.4],
    EyelidUp= [0.15,7.40,0.45],
    EyelidDwn=[0.15,7.36,0.45]
)
