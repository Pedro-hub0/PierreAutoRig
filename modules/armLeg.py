import maya.cmds as cmds
import sys
import os
# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)
import smallUsefulFct
import foot
import math
import importlib
importlib.reload(smallUsefulFct)
importlib.reload(foot)
###################################
###         CREATE IK FK       ####
###################################
def createJnts(sz):
    cmds.select(clear=True)
    jntLeg=[]
    jntArm=[]
    size=smallUsefulFct.GetDistLocScale(sz)*3
    for i in range(0,3): 
        moveNumber=(i*size,0,0)
        moveNumber2=(0,(-i)*size,0)
        jntArm.append(cmds.joint(n=f'Arm_L',p=moveNumber))
        cmds.select(clear=True)
        jntLeg.append(cmds.joint(n=f'Leg_L',p=moveNumber2))
        cmds.select(clear=True)

    for i in range(2,0,-1): 
        cmds.parent(jntArm[i],jntArm[i-1])
        cmds.parent(jntLeg[i],jntLeg[i-1])
        cmds.select(clear=True)

    if not cmds.objExists("Grp_temp_Jnt_Leg_Arm") :
        cmds.group(empty=True, name="Grp_temp_Jnt_Leg_Arm")
        cmds.parent(jntLeg[0],"Grp_temp_Jnt_Leg_Arm")
        cmds.parent(jntArm[0],"Grp_temp_Jnt_Leg_Arm")

        

def FreezeOrient():
#joint -e  -oj xyz -secondaryAxisOrient xup -ch -zso;
    #Prendre Selections
    selObj = cmds.ls(selection=True)    
    TempIkChain = cmds.listRelatives(selObj, allDescendents=True, type='joint') or []

    #Freeze et Orient :
    cmds.makeIdentity(selObj[0],apply=True, rotate=True, translate=False, scale=False, normal=False)
    cmds.joint(selObj[0], e=True, oj='xyz', sao='xup', ch=True, zso=True)   
    cmds.joint(TempIkChain[0], e=True, oj='none', ch=True, zso=True)
    return

def createIkFk(sz):
    #NEED A GOOD NAME FOR THE FIRST JOINT
    #####INITIALISATION#####
    selObj = cmds.ls(selection=True)
    obj=selObj[0]
    side=selObj[0][-1]
    objName=selObj[0][:-2]
    FkCtrl=[]
    ConstrBindHand=[]
    size=smallUsefulFct.GetDistLocScale(sz)


    # Find the index of the letter after which you want to grab the name
    #index_of_letter = selObj[0].find('_')  # Assuming you want to grab the name after the underscore
    
   
    if objName == "Arm" :
        Fk_jnt_Names = [f'Fk_Shoulder_{side}',f'Fk_Elbow_{side}',f'Fk_Wrist_{side}']
        Ik_jnt_Names = [f'DrvJnt_Shoulder_{side}',f'DrvJnt_Elbow_{side}',f'DrvJnt_Wrist_{side}']
    elif objName == "Leg" :
        Fk_jnt_Names = [f'Fk_Leg_{side}',f'Fk_Knee_{side}',f'Fk_Ankle_{side}']
        Ik_jnt_Names = [f'DrvJnt_Leg_{side}',f'DrvJnt_Knee_{side}',f'DrvJnt_Ankle_{side}']
  
    else :
        raise ValueError("You need to name your joint like Arm_L or Leg_R for example ")
    
        ##Create Organisation##
    smallUsefulFct.organiser()
    grp_Ctrl="CTRL"
    grp_Jnt="JNT"
    grp_preserve="Preserve_Jnts"
    grp_Iks='IKs'

    #Get children 
    TempIkChain = cmds.listRelatives(obj, allDescendents=True, type='joint') or []
    IkChain =[]
    
    ### More Optimisation ###
    #Create Locs
    #Create joints
    ######
    #Rename

    if (len(TempIkChain) == 2):
        i=0
        #SORT Names
        IkChain.append(selObj[0])
        IkChain.append(TempIkChain[1])
        IkChain.append(TempIkChain[0])
        
        while i<len(IkChain):
            cmds.rename(IkChain[i], Ik_jnt_Names[i])
            IkChain[i]= Ik_jnt_Names[i]

            i+=1
    else:
        raise ValueError("You need to have only 2 child (in your hierarchy, do whatever you want in your life)")
    
    #Freeze and Orient ?

    #Duplicate
    if objName == "Arm":
        #create BindHand
        BindHand=cmds.duplicate(IkChain[2], rc=True)[0]
        cmds.parent(BindHand, world=True)

        #Rename BindHand  
        cmds.rename(BindHand,f'Bind_Hand_{side}')     
        BindHand=f'Bind_Hand_{side}'
        smallUsefulFct.move(BindHand)

    FkChain =cmds.duplicate(IkChain[0], rc=True)
    
    i=0
    while i<len(FkChain):
        cmds.rename(FkChain[i], Fk_jnt_Names[i])
        FkChain[i]= Fk_jnt_Names[i]
        i+=1
    
    #Create Move//Offset 
    smallUsefulFct.move(FkChain[0])
    smallUsefulFct.move(IkChain[0])
    
    #Ik
    ik_handle_Arm =cmds.ikHandle(startJoint=IkChain[0], endEffector=IkChain[2], solver='ikRPsolver', name=f'Ik_{objName}_{side}')[0]
    cmds.parent(ik_handle_Arm,grp_Iks)
    #Pole vector

    Pv_Ik_Arm= cmds.circle(name=f'Pv_{objName}_{side}',radius=size/2,nr=[1,0,0])[0]
    smallUsefulFct.set_curve_color(Pv_Ik_Arm,28)
    TranslateShoulder = cmds.xform(FkChain[1], q=True, t=True, ws=True)
    move=1

    if objName=="Arm":
        move=-size*3

    if objName=="Leg":
        move=size*3
    TranslateShoulderMove=(TranslateShoulder[0],TranslateShoulder[1],TranslateShoulder[2]+move)
    cmds.xform(Pv_Ik_Arm, t=TranslateShoulderMove, ws=True)
    cmds.poleVectorConstraint(Pv_Ik_Arm, ik_handle_Arm)
    smallUsefulFct.offset(Pv_Ik_Arm)

    #Fk Controller 
    if objName == "Arm" :
        FkCtrl.append(cmds.circle(name=f'CTRL_Fk_Shoulder_{side}',radius=size,nr=[1,0,0])[0])
        FkCtrl.append(cmds.circle(name=f'CTRL_Fk_Elbow_{side}',radius=size,nr=[1,0,0])[0])
        FkCtrl.append(cmds.circle(name=f'CTRL_Fk_Wrist_{side}',radius=size,nr=[1,0,0])[0])

    if objName == "Leg" :
        FkCtrl.append(cmds.circle(name=f'CTRL_Fk_Leg_{side}',radius=size,nr=[1,0,0])[0])
        FkCtrl.append(cmds.circle(name=f'CTRL_Fk_Knee_{side}',radius=size,nr=[1,0,0])[0])
        FkCtrl.append(cmds.circle(name=f'CTRL_Fk_Foot_{side}',radius=size,nr=[1,0,0])[0])
    

    i=0
    #Fk Controller -- Move and do the hierarchy --
    while i<len(FkCtrl):
        TranslateJnt = cmds.xform(FkChain[i], q=True, t=True, ws=True)
        RotationJnt = cmds.xform(FkChain[i], query=True, rotation=True, worldSpace=True)
        smallUsefulFct.set_curve_color(FkCtrl[i],28)
        cmds.xform(FkCtrl[i], t=TranslateJnt, ro=RotationJnt, ws=True)
        if i>0:
            smallUsefulFct.offset(FkCtrl[i])
            cmds.parent(f'{FkCtrl[i]}_Offset',FkCtrl[i-1])
        elif i==0:
            smallUsefulFct.move(FkCtrl[i])
        i+=1
    i=0
    #Fk --Constraint Controller --
    while i<len(FkCtrl):
        cmds.parentConstraint(FkCtrl[i],Fk_jnt_Names[i], maintainOffset=True, weight=1)
        i+=1
        
    i=0
    #Ik Controller 
    TranslateJnt = cmds.xform(FkChain[2], q=True, t=True, ws=True)
    RotationJnt = cmds.xform(FkChain[2], query=True, rotation=True, worldSpace=True)
    if objName == "Arm" :
        Ctrl_Hand=smallUsefulFct.controller(1,FkChain[2],f'CTRL_Hand_{side}',size)
        smallUsefulFct.set_curve_color(Ctrl_Hand,16)
        cmds.xform(Ctrl_Hand, t=TranslateJnt, ro=RotationJnt, ws=True)
        smallUsefulFct.move(Ctrl_Hand)
    if objName == "Leg" :
        if cmds.objExists(f'CTRL_Foot_{side}'):
            cmds.delete(f'CTRL_Foot_{side}')
        Ctrl_Hand=cmds.circle(name=f'CTRL_Foot_{side}',nr=[1,0,0],radius=size)[0]
        smallUsefulFct.set_curve_color(Ctrl_Hand,16)
        cmds.xform(Ctrl_Hand, t=TranslateJnt, ro=RotationJnt, ws=True)
        smallUsefulFct.move(Ctrl_Hand)
        foot.createAttributFoot(Ctrl_Hand,side)
        #else:
        #    Ctrl_Hand=f'CTRL_Foot_{side}'
            
        BindHand="null"


    
    #Ik Fk
    # --> Create switch CTRL with attributes
    Ctrl_SwitchIkFk = cmds.circle(name=f'CTRL_IkFk_{objName}_{side}',radius=size)[0]
    # Get the translation values of the source object
    TranslateFk = cmds.xform(IkChain[0], q=True, t=True, ws=True)
    ofCtrl=smallUsefulFct.offset2(Ctrl_SwitchIkFk)
    # Apply the translation values to the destination object
    cmds.xform(ofCtrl, t=TranslateFk, ws=True)
    
    # Move the destination object up and right
    if side == "L" :
        ikFkSide=0.5*size
    if side == "R" :
        ikFkSide=(-0.5)*size
    cmds.move(ikFkSide,2*size, 0, ofCtrl, r=True, os=True)  
    
    #Add An attribute 
    cmds.addAttr(Ctrl_SwitchIkFk, longName="Switch_Ik_Fk", attributeType="float", defaultValue=0, minValue=0.0, maxValue=1.0,keyable=True)
    smallUsefulFct.lock_and_hide_attributes(f'CTRL_IkFk_{objName}_{side}')
    MyPbFct(objName,side,Ctrl_SwitchIkFk,IkChain,FkChain)

    if objName == "Arm" :
        #Contraintes Bind Arm
        #CTRL
        cmds.parentConstraint(Ctrl_Hand, ik_handle_Arm, maintainOffset=True, weight=1, skipRotate=['x', 'y', 'z'])
        cmds.parentConstraint(Ctrl_Hand, Ik_jnt_Names[2], maintainOffset=True, weight=1, skipTranslate=['x', 'y', 'z'])
        #Jnts
        ConstrBindHand.append(cmds.parentConstraint(Fk_jnt_Names[2], f'{BindHand}_Move', maintainOffset=True, weight=1)[0])
        ConstrBindHand.append(cmds.parentConstraint(Ik_jnt_Names[2], f'{BindHand}_Move', maintainOffset=True, weight=1)[0])
        cmds.connectAttr(f'Rev_{objName}_{side}_IkFk.outputX',f'{ConstrBindHand[0]}.{Fk_jnt_Names[2]}W0')
        cmds.connectAttr(Ctrl_SwitchIkFk+".Switch_Ik_Fk",f'{ConstrBindHand[1]}.{Ik_jnt_Names[2]}W1')



    #Preserve Joint 

    PreserveJnt =cmds.duplicate(IkChain[1], po=True)[0]
            #Rename Preserve Joint  
    cmds.rename(PreserveJnt,f'Preserve_{objName}_{side}')     
    PreserveJnt=f'Preserve_{objName}_{side}'
        #Change pivot etc.
    smallUsefulFct.hook(PreserveJnt)
    smallUsefulFct.match_pivot(f'{PreserveJnt}_Hook',IkChain[0])
    cmds.parentConstraint(IkChain[0],f'{PreserveJnt}_Hook', maintainOffset=True, weight=1)
    cmds.parentConstraint(IkChain[1],f'{PreserveJnt}_Move', maintainOffset=True, weight=1, skipRotate=['x', 'y', 'z'])
        #Nodes
    """    multiply_divide_preserve = cmds.createNode("multiplyDivide", name=f'Preserve_{objName}_{side}_Mult')
    cmds.connectAttr(f"{IkChain[0]}.rotateZ",f'{multiply_divide_preserve}.input1X')
    cmds.setAttr(f'{multiply_divide_preserve}.input2X',0.5)
    cmds.connectAttr(f'{multiply_divide_preserve}.outputX',f"{PreserveJnt}.rotateZ")"""
    cmds.orientConstraint(IkChain[0],IkChain[1],PreserveJnt, weight=0.5)    

    #Visibility
    cmds.connectAttr(Ctrl_SwitchIkFk+".Switch_Ik_Fk",f"{Ctrl_Hand}.visibility")
    cmds.connectAttr(f"Rev_{objName}_{side}_IkFk.outputX",f'{FkCtrl[0]}.visibility')


    #Organiser
    grp_Jnt_Spine=cmds.group(empty=True, name=f"Grp_Jnt_{objName}_{side}")
    grp_Ctrl_Spine=cmds.group(empty=True, name=f"Grp_Ctrl_{objName}_{side}")
    cmds.parent(f'{PreserveJnt}_Offset',grp_preserve)
    cmds.parent(f'{Fk_jnt_Names[0]}_Offset',grp_Jnt_Spine)
    cmds.parent(f'{Ik_jnt_Names[0]}_Offset',grp_Jnt_Spine)
    cmds.parent(grp_Jnt_Spine,grp_Jnt)
    if objName == "Arm" :
        cmds.parent(f'{BindHand}_Offset',grp_Jnt_Spine)
    cmds.parent(f'{FkCtrl[0]}_Offset',grp_Ctrl_Spine)
    if objName == "Arm" :
        cmds.parent(f'{Ctrl_Hand}_Offset',grp_Ctrl_Spine)
    cmds.parent(f'{Pv_Ik_Arm}_Offset',grp_Ctrl_Spine)
    cmds.parent(f'{ofCtrl}',grp_Ctrl_Spine)
    cmds.parentConstraint(Ik_jnt_Names[0] ,ofCtrl,maintainOffset=True, weight=1)
    cmds.parent(grp_Ctrl_Spine,grp_Ctrl)



    return
def mirror(sz):
    selObj = cmds.ls(selection=True)
    obj=selObj[0]
        #Names
    parts = obj.split("_")
    lenName=len(parts)
    side=parts[lenName-1]
    objName=parts[lenName-2]
    mirorJnt=""
    if side=="L":
        otherSide='R'
    else: otherSide='L'

    if objName == "Arm" :
        mirorJnt=f'Fk_Shoulder_{side}'
    elif objName == "Leg" :
        mirorJnt = f'Fk_Leg_{side}' 
    else :
        raise ValueError("You need to name your joint like Arm_L or Leg_R for example ")
    
    if not cmds.objExists("Bind_Root"):
        raise ValueError("You need to have a Bind_Root to mirror")

    if not selObj==f'{obj}_{side}':
        #Create mirror
        #Duplicate Fk
        tempJnt=cmds.duplicate(mirorJnt, rc=True)
        #Parent to Bind_root
        cmds.parent(tempJnt[0],"Bind_Root")
        #Erase non joint things
        smallUsefulFct.delete_non_joints_in_hierarchy(tempJnt)
    
        #Mirror mirrorJoint -mirrorYZ -mirrorBehavior -searchReplace "_L" "_R";
        newJnt=cmds.mirrorJoint(tempJnt[0],mirrorYZ=True,mirrorBehavior=True,searchReplace=(f'_{side}', f'_{otherSide}'))
        #Delete temp Fk
        cmds.delete(tempJnt[0])
        #rename to match with Create
        cmds.rename(newJnt[0],f'{objName}_{otherSide}')

    finalObj=f'{objName}_{otherSide}'
    #Create Ik/Fk
    cmds.select(finalObj)
    print(f"FINALLL {finalObj}")
    createIkFk(sz)


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
        Fk_ctrl_Names=[f'CTRL_Shoulder_{side}',f'CTRL_Elbow_{side}',f'CTRL_Wrist_{side}']
        Fk_jnt_Names = [f'Fk_Shoulder_{side}',f'Fk_Elbow_{side}',f'Fk_Wrist_{side}']
        Ik_jnt_Names = [f'DrvJnt_Shoulder_{side}',f'DrvJnt_Elbow_{side}',f'DrvJnt_Wrist_{side}']
    elif objName == "Leg" :
        Fk_ctrl_Names=[f'CTRL_Leg_{side}',f'CTRL_Knee_{side}',f'CTRL_Ankle_{side}']
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
        

###################################
###PAIR BLEND (Fil Rouge Code)####
###################################

def MyPbFct(ob,side,Ctrl,ik,fk):
    i=0
    #CONNECTIONS PAIR BLEND
    while i < 3:
        # Select the object
        PBname = "pairBlend_" + ik[i] + "_" + fk[i]
        pair_blend_node = cmds.createNode("pairBlend", name=PBname)
        # Get the current rotation values
        rotation_values = cmds.getAttr(ik[i] + ".rotate")
        # Set the rotate values of the object as inRotate1 of the pairBlend node and The Out Rotate to the rotate of every 2nd Joints
        cmds.connectAttr(fk[i] + ".rotate",pair_blend_node + ".inRotate1")
        cmds.connectAttr(f'{pair_blend_node}.outRotate',ik[i]+ ".rotate")
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",pair_blend_node +".weight")
        i=i+1
    if ob == "Arm":
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"Ik_{ob}_{side}.ikBlend")
        reverse_node = cmds.createNode('reverse', name=f'Rev_{ob}_{side}_IkFk')
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"{reverse_node}.inputX")
        cmds.connectAttr(f"{Ctrl}.Switch_Ik_Fk",f"Pv_{ob}_{side}.visibility")
        cmds.connectAttr(f"{Ctrl}.Switch_Ik_Fk",f"DrvJnt_Shoulder_{side}.visibility")
        cmds.setAttr(f"Ik_{ob}_{side}.visibility",0)
        cmds.connectAttr(f"{reverse_node}.outputX",f"Fk_Shoulder_{side}.visibility")
  
    if ob == "Leg":
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"Ik_{ob}_{side}.ikBlend")
        reverse_node = cmds.createNode('reverse', name=f'Rev_{ob}_{side}_IkFk')
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"{reverse_node}.inputX")
        cmds.connectAttr(f"{Ctrl}.Switch_Ik_Fk",f"Pv_{ob}_{side}.visibility")
        cmds.connectAttr(f"{Ctrl}.Switch_Ik_Fk",f"DrvJnt_{ob}_{side}.visibility")
        cmds.setAttr(f"Ik_{ob}_{side}.visibility",0)
        cmds.connectAttr(f"{reverse_node}.outputX",f"Fk_{ob}_{side}.visibility")
    
    if ob == "Foot":
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"Ik_Toe_{side}.ikBlend")
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"Ik_Ball_{side}.ikBlend")
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"Bind_{ob}_{side}.visibility")
        reverse_node = f'Rev_Leg_{side}_IkFk'
        conn=cmds.listConnections(f"CTRL_{ob}_{side}.visibility")
        if cmds.objExists(reverse_node):
            cmds.connectAttr(f"{reverse_node}.outputX",f"Fk_{ob}_{side}.visibility")
        if not conn:
            cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"CTRL_{ob}_{side}.visibility")
   #Pair Blend BindHand
    if ob == "Arm":
        if f'Bind_Hand_{side}':
            pB_Bind = cmds.createNode("pairBlend", name=f'PB_Hand_{side}')
            cmds.connectAttr(fk[2] + ".rotate",pB_Bind + ".inRotate1")
            cmds.connectAttr(pB_Bind +".outRotate",f'Bind_Hand_{side}.rotate')
            cmds.connectAttr(Ctrl+".Switch_Ik_Fk",pB_Bind + ".weight")
