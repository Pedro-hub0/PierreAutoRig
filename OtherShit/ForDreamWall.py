import maya.cmds as cmds

info=["LEON",'Arm','R']
#MatchIkFk in dreamwall
def find_namespaces_with_leon(name):
    # Get a list of all namespaces
    all_namespaces = cmds.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    
    # Filter namespaces that contain "Leon"
    leon_namespaces = [ns for ns in all_namespaces if name in ns]
    if len(leon_namespaces)!=0:
        leon_namespaces=f'{leon_namespaces[0]}:'
    else:
        leon_namespaces=f''
    
    return leon_namespaces

def copy_rotation_to_list(source,destination):
    for i in range(0,len(source)):
        destination.append(cmds.xform(source[i], query=True, rotation=True, worldSpace=True))

def copy_translation_to_list(source,destination):
    for i in range(0,len(source)):
        destination.append(cmds.xform(source[i], q=True, t=True, ws=True))

def matchIkFk(value,txt_n):


    # Get the text entered in the field
    txt_namespace=txt_n
    #INITIALISATIONS VARIABLES
        #Object
    objName=info[1]
        #Names
    side=info[2]

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
    rotatectrlFk=[]
    translate_Ik=[]
    translate_Fk=[] 
    pv_Ctrl=f'{txt_namespace}Pv_{objName}_{side}'
    if objName == "Arm":
        ik_Ctrl=f'{txt_namespace}CTRL_Hand_{side}'
    if objName == "Leg":
        ik_Ctrl=f'{txt_namespace}CTRL_Foot_{side}'

    cmds.setAttr(f'{txt_namespace}CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk',1)
    #Copy transform
    copy_rotation_to_list(Ik_jnt_Names,rotate_Ik)
    copy_translation_to_list(Ik_jnt_Names,translate_Ik)
    cmds.setAttr(f'{txt_namespace}CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk',0)
    copy_rotation_to_list(Fk_jnt_Names,rotate_Fk)
    copy_translation_to_list(Fk_jnt_Names,translate_Fk)
    if cmds.objExists(f'Dummy_Loc_{objName}_{side}'):
        Dummy_Translate=cmds.xform(f'Dummy_Loc_{objName}_{side}', q=True, t=True, ws=True)

    if isIk ==1:
        if objName == "Leg":
            cmds.xform(ik_Ctrl, translation=translate_Fk[2], rotation=rotatectrlFk[2], worldSpace=True)
        else:
            cmds.xform(ik_Ctrl, translation=translate_Fk[2], rotation=rotate_Fk[2], worldSpace=True)
        rotatectrlFk
        if cmds.objExists(f'Dummy_Loc_{objName}_{side}'):
            cmds.xform(pv_Ctrl, translation=Dummy_Translate, worldSpace=True)
        else:
            cmds.xform(pv_Ctrl, translation=translate_Fk[1], worldSpace=True)    
        cmds.setAttr(f'{txt_namespace}CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk',1)
        
    elif isIk == 0:
        #Rotate Fk Ctrl to Jnt drvjnt Shoulder/Elbow/Wrist
        test=cmds.getAttr(f'{txt_namespace}CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk')

        for i in range(0,len(Fk_ctrl_Names)):
            cmds.xform(Fk_ctrl_Names[i],rotation=rotate_Ik[i], worldSpace=True)

        cmds.setAttr(f'{txt_namespace}CTRL_IkFk_{objName}_{side}.Switch_Ik_Fk',0)


    else:
        raise ValueError("Switch ik/Fk need to be 0 or 1")

txt_mamespace=find_namespaces_with_leon(info[0])
matchIkFk(2,txt_mamespace)