import maya.cmds as cmds
import sys
import os



"""Script created by Pierre LIPPENS """

def create_window():
    """
    Create a window with a button.
    """
    # Check if the window already exists, and delete it if it does
    if cmds.window("myWindow", exists=True):
        cmds.deleteUI("myWindow", window=True)

    # Create the window
    window_name = cmds.window("myWindow", title="MatchIkFk_PierreAuto", widthHeight=(310, 100), sizeable=False)
    # Create a layout for the window
    column_layout= cmds.columnLayout(adjustableColumn=True)


    cmds.separator(h=8)
    cmds.text(label="TOOLS", font = "boldLabelFont" , w = 300, align = "center")
    cmds.separator(h=8)


    cmds.text(label=" Match Ik/Fk ", font = "boldLabelFont" , w = 300, align = "left")
    cmds.separator(h=5)
    # Create a text field
    txt_mamespace = cmds.textField(placeholderText="Namespace")
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[150, 75,75])
    cmds.button(label='Match Auto', command=lambda x:matchIkFk(2,txt_mamespace),width=150)
    cmds.button(label='Fk/Ik', command=lambda x:matchIkFk(0,txt_mamespace),width=75)
    cmds.button(label='Ik/Fk', command=lambda x:matchIkFk(1,txt_mamespace),width=75)
    # Show the window
    cmds.showWindow(window_name)



###################################
###         MATCH IK FK        ####
###################################

######################## A CHANGER ################################
## Avoir le variable_side ou Nom_R
ControllersArm=['CTRL_Fk_Shoulder','CTRL_Fk_Elbow','CTRL_Fk_Wrist']
FkJointsArm=['Fk_Shoulder','Fk_Elbow','Fk_Wrist']
IkJointsArm=['DrvJnt_Shoulder','DrvJnt_Elbow','DrvJnt_Wrist']

ControllersLeg=['CTRL_Fk_Leg','CTRL_Fk_Knee','CTRL_Fk_Foot']
FkJointsLeg=['Fk_Leg','Fk_Knee','Fk_Ankle']
IkJointsLeg=['DrvJnt_Leg','DrvJnt_Knee','DrvJnt_Ankle']

#        Nom _   Arm Leg _ L/R . switch attribute 
#{ControllersArm[0]}_{objName}_{side}.{switchNameAttribute}'
CTRL_Ik=['CTRL_Hand','CTRL_Foot']
switchNameAttribute='Switch_Ik_Fk'

#{PoleVector}_{objName}_{side}
PoleVector='Pv'
##################################################################


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
        isIk=cmds.getAttr(f'{txt_namespace}{obj}.{switchNameAttribute}')
    else:
        isIk=value


    if objName == "Arm" :
        Fk_ctrl_Names=[f'{txt_namespace}{ControllersArm[0]}_{side}',f'{txt_namespace}{ControllersArm[1]}_{side}',f'{txt_namespace}{ControllersArm[2]}_{side}']
        Ik_jnt_Names = [f'{txt_namespace}{IkJointsArm[0]}_{side}',f'{txt_namespace}{IkJointsArm[1]}_{side}',f'{IkJointsArm[2]}_{side}']
    elif objName == "Leg" :
        Fk_ctrl_Names=[f'{txt_namespace}{ControllersLeg[0]}_{side}',f'{txt_namespace}{ControllersLeg[1]}_{side}',f'{txt_namespace}{ControllersLeg[2]}_{side}']
        Ik_jnt_Names = [f'{txt_namespace}{IkJointsLeg[0]}_{side}',f'{txt_namespace}{IkJointsLeg[1]}_{side}',f'{txt_namespace}{IkJointsLeg[2]}_{side}']
    else :
        raise ValueError("You need to select somethind that's end up by Arm_L or Leg_R for example ")
    
    #Transform
    rotate_Ik=[]
    rotate_Fk=[]
    translate_Ik=[]
    translate_Fk=[] 
    pv_Ctrl=f'{txt_namespace}{PoleVector}_{objName}_{side}'
    if objName == "Arm":
        ik_Ctrl=f'{txt_namespace}{CTRL_Ik[0]}_{side}'
    if objName == "Leg":
        ik_Ctrl=f'{txt_namespace}{CTRL_Ik[1]}_{side}'

    cmds.setAttr(f'{txt_namespace}{obj}.{switchNameAttribute}',1)

    #Copy transform
    copy_rotation_to_list(Ik_jnt_Names,rotate_Ik)
    copy_rotation_to_list(Fk_ctrl_Names,rotate_Fk)
    copy_translation_to_list(Ik_jnt_Names,translate_Ik)
    copy_translation_to_list(Fk_ctrl_Names,translate_Fk)

    if isIk ==1:
        #Transform Ik Ctrl to Jnt Fk Wrist
        cmds.xform(ik_Ctrl, translation=translate_Fk[2], rotation=rotate_Fk[2], worldSpace=True)
        #Translate Ik Pv to Jnt Fk Elbow
        cmds.xform(pv_Ctrl, translation=translate_Fk[1], worldSpace=True)
    elif isIk == 0:
        #Rotate Fk Ctrl to Jnt drvjnt Shoulder/Elbow/Wrist
        test=cmds.getAttr(f'{txt_namespace}{obj}.{switchNameAttribute}')


        for i in range(0,len(Fk_ctrl_Names)):
            cmds.xform(Fk_ctrl_Names[i],rotation=rotate_Ik[i], worldSpace=True)

        cmds.setAttr(f'{txt_namespace}{obj}.{switchNameAttribute}',0)


    else:
        raise ValueError("Switch ik/Fk need to be 0 or 1")
     
        

def copy_rotation_to_list(source,destination):
    for i in range(0,len(source)):
        destination.append(cmds.xform(source[i], query=True, rotation=True, worldSpace=True))

def copy_translation_to_list(source,destination):
    for i in range(0,len(source)):
        destination.append(cmds.xform(source[i], q=True, t=True, ws=True))

create_window()