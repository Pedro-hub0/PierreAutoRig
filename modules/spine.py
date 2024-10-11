import maya.cmds as cmds
import smallUsefulFct
import math


###################################
###        Create Spine        ####
###################################    
def creatLocsSpine():
    loc=cmds.spaceLocator(n=f'Loc_Shoulder')
    loc=cmds.spaceLocator(n=f'Loc_Root')

def createSpine(spineIk,spineFk,sz) :
    nbIkJnt=cmds.intField(spineIk, query=True, value=True)
    nbFkJnt=cmds.intField(spineFk, query=True, value=True)
    sz=cmds.intField(sz, query=True, value=True)
    LocName=['Loc_Root','Loc_Shoulder']
    JntName=['Jnt_Root','Jnt_Shoulder']
    IkJnts=[]
    FkJnts=[]
    Ctrl_Fk_Spine=[]
    Ctrl_Ik_Spine=[]
    grp_Extranode=""
    #Organiser
    smallUsefulFct.organiser()
    grp_Ctrl="CTRL"
    grp_Jnt="JNT"
    grp_Global='GlobalMove'
    grp_Iks='IKs'
    grp_Extranode="ExtraNodes"
    if not cmds.objExists('Loc_Shoulder') or not cmds.objExists('Loc_Root'):
        raise ValueError("Create Locators")

    TranslateJnts = [cmds.xform(LocName[0], q=True, t=True, ws=True),cmds.xform(LocName[1], q=True, t=True, ws=True)]
   
    #CREATE JOINT IN A LINE BETWEEN THE 2 JOINTS
    i=0
    while i<=nbIkJnt :
        if i==0:
            name=f'Bind_Root'
        else:
            name=f'Bind_Spine_0{i}'
        JntTranslate=[((TranslateJnts[1][0]-TranslateJnts[0][0])/nbIkJnt)*i +TranslateJnts[0][0],((TranslateJnts[1][1]-TranslateJnts[0][1])/nbIkJnt)*i +TranslateJnts[0][1],((TranslateJnts[1][2]-TranslateJnts[0][2])/nbIkJnt)*i +TranslateJnts[0][2]]
        IkJnts.append(cmds.joint(position=JntTranslate, name=f'{name}'))
        i+=1

    i=0
    while i<=nbFkJnt :
        if i==0:
            name=f'Fk_Root'
        else:
            name=f'Fk_Spine_0{i}'
        JntTranslate=[((TranslateJnts[1][0]-TranslateJnts[0][0])/nbFkJnt)*i +TranslateJnts[0][0],((TranslateJnts[1][1]-TranslateJnts[0][1])/nbFkJnt)*i +TranslateJnts[0][1],((TranslateJnts[1][2]-TranslateJnts[0][2])/nbFkJnt)*i +TranslateJnts[0][2]]
        FkJnts.append(cmds.joint(position=JntTranslate, name=f'{name}'))

        if i==0 :
            p=cmds.parent(f'Fk_Root', world=True)
            if p==True:
                cmds.parent(f'Fk_Root', world=True)
        i+=1


    #Orient 
        #Ik
    cmds.joint(FkJnts[0],e=True, oj='xyz', sao='yup', ch=True, zso=True)
    cmds.joint(FkJnts[len(FkJnts)-1], e=True, oj='none', ch=True, zso=True)
        #Fk
    cmds.joint(IkJnts[0],e=True, oj='xyz', sao='yup', ch=True, zso=True)
    cmds.joint(IkJnts[len(IkJnts)-1], e=True, oj='none', ch=True, zso=True)
    
    #Create Ik 02
    temp=cmds.duplicate(IkJnts[0],parentOnly=True)[0]
    cmds.rename(temp,JntName[0])
    temp=cmds.duplicate(IkJnts[len(IkJnts)-1],parentOnly=True)[0]
    cmds.rename(temp,JntName[1])

    smallUsefulFct.move(FkJnts[0])
    smallUsefulFct.move(IkJnts[0])
    smallUsefulFct.move(JntName[0])
    smallUsefulFct.move(JntName[1])


    #Create Ik Spline
    ik_objs = cmds.ikHandle(sj=IkJnts[0], ee=IkJnts[len(IkJnts)-1], sol='ikSplineSolver', ccv=True, scv=True,pcv=True,name="Ik_Spine")
    ik_Handle=ik_objs[0]
    CurveIk=ik_objs[len(ik_objs)-1]
    cmds.rename(CurveIk,"Crv_Spine")
    CurveIk="Crv_Spine"
    cmds.parent(CurveIk,grp_Extranode)

    ##Corriger Bas curve ne rotate pas, Twist
    SkinClusterSpine = cmds.skinCluster(JntName, CurveIk, n='spine_skinCluster', tsb=True, bm=0, sm=0, nw=1,mi=3)[0]
    cmds.setAttr(f'{ik_Handle}.rootTwistMode', 1)
    cmds.setAttr(f'{ik_Handle}.dTwistControlEnable', 1)
    cmds.setAttr(f'{ik_Handle}.dWorldUpType', 4)

    cmds.connectAttr(f'{JntName[0]}.worldMatrix',f'{ik_Handle}.dWorldUpMatrix')
    cmds.connectAttr(f'{JntName[1]}.worldMatrix',f'{ik_Handle}.dWorldUpMatrixEnd') 
    cmds.setAttr(f'{ik_Handle}.dWorldUpVectorEndX',0)
    cmds.setAttr(f'{ik_Handle}.dWorldUpVectorEndY',1)
    cmds.setAttr(f'{ik_Handle}.dWorldUpVectorEndZ', 0)
    cmds.setAttr(f'{ik_Handle}.dWorldUpVectorX', 0)
    cmds.setAttr(f'{ik_Handle}.dWorldUpVectorY', 1)
    cmds.setAttr(f'{ik_Handle}.dWorldUpVectorZ', 0)
   
    #Create Controllers
        #Ik
    colorIk=17
    Ctrl_Ik_Spine.append(smallUsefulFct.controller(1,JntName[0],"CTRL_Root",sz))
    Ctrl_Ik_Spine.append(smallUsefulFct.controller(1,JntName[1],"CTRL_Torso",sz))
    smallUsefulFct.set_curve_color(Ctrl_Ik_Spine[0],colorIk)
    smallUsefulFct.set_curve_color(Ctrl_Ik_Spine[1],colorIk)
    smallUsefulFct.move(Ctrl_Ik_Spine[0]) 
    smallUsefulFct.move(Ctrl_Ik_Spine[1])        
        #Fk
    for i in range(1,nbFkJnt+1):
        TranslateCtrl=cmds.xform(FkJnts[i], query=True, translation=True, worldSpace=True)
        RotationCtrl=cmds.xform(FkJnts[i], query=True, translation=True, worldSpace=True)

        Ctrl_Fk_Spine.append(cmds.circle(name=f'Ctrl_{FkJnts[i]}',nr=[0,0,1],radius=sz)[0])                 
        #Transform Ik Ctrl_Fk_Spine to Jnt Fk Wrist
        cmds.xform(Ctrl_Fk_Spine[i-1], translation=TranslateCtrl, worldSpace=True)  
        rot=cmds.getAttr(f'{Ctrl_Fk_Spine[i-1]}.rotateX')
        cmds.setAttr(f'{Ctrl_Fk_Spine[i-1]}.rotateX',rot+90)
        smallUsefulFct.set_curve_color(Ctrl_Fk_Spine[i-1],15)
        smallUsefulFct.move(Ctrl_Fk_Spine[i-1])
        if i>1:
            cmds.parent(f'{Ctrl_Fk_Spine[i-1]}_Offset',Ctrl_Fk_Spine[i-2])
   

    #Constraints 
        #Root to Fk root/Ik/ Shoulder to Ik/ 
    cmds.parentConstraint(f'{Ctrl_Ik_Spine[0]}',f'{JntName[0]}_Move', maintainOffset=True, weight=1)
    cmds.parentConstraint(f'{Ctrl_Ik_Spine[0]}',f'{FkJnts[0]}_Move', maintainOffset=True, weight=1)
    cmds.parentConstraint(f'{Ctrl_Ik_Spine[0]}',f'{Ctrl_Fk_Spine[0]}_Move', maintainOffset=True, weight=1)
    cmds.parentConstraint(f'{Ctrl_Ik_Spine[1]}',f'{JntName[1]}_Move', maintainOffset=True, weight=1)
    cmds.parentConstraint(f'{Ctrl_Fk_Spine[len(Ctrl_Fk_Spine)-1]}',f'{Ctrl_Ik_Spine[1]}_Move', maintainOffset=True, weight=1)
        #Fk
    i=1
    while i<nbFkJnt :
        cmds.parentConstraint(f'{Ctrl_Fk_Spine[i-1]}',f'{FkJnts[i]}', maintainOffset=True, weight=1)
        i+=1

    #Organiser

    grp_Ctrl_Spine=cmds.group(empty=True, name="Grp_CTRL_Spine")
    cmds.parent(f'{Ctrl_Ik_Spine[0]}_Offset',grp_Ctrl_Spine)
    cmds.parent(f'{Ctrl_Ik_Spine[1]}_Offset',grp_Ctrl_Spine)
    cmds.parent(f'{Ctrl_Fk_Spine[0]}_Offset',grp_Ctrl_Spine)
    cmds.parent(grp_Ctrl_Spine,grp_Ctrl)

    grp_Jnt_Spine=cmds.group(empty=True, name="Grp_Jnt_Spine")
    cmds.parent(f'{FkJnts[0]}_Offset',grp_Jnt_Spine)
    cmds.parent(f'{IkJnts[0]}_Offset',grp_Jnt_Spine)
    cmds.parent(f'{JntName[0]}_Offset',grp_Jnt_Spine)
    cmds.parent(f'{JntName[1]}_Offset',grp_Jnt_Spine)
    cmds.parent(grp_Jnt_Spine,grp_Jnt)   
    cmds.parent(f'{ik_Handle}',grp_Iks)
    if not cmds.objExists("Grp_temp_Locs") :
        cmds.group(empty=True, name="Grp_temp_Locs")
    cmds.parent(LocName,"Grp_temp_Locs")


####################
###   STRETCH   ####
####################

def Stretchfct():
    selObj = cmds.ls(selection=True)
    obj=selObj[0]
        #Names
    parts = obj.split("_")
    lenName=len(parts)
    side=parts[lenName-1]
    objName=parts[lenName-2]
    if objName == "Arm" :
        Ik_jnt_Names = [f'DrvJnt_Shoulder_{side}',f'DrvJnt_Elbow_{side}',f'DrvJnt_Wrist_{side}']
    elif objName == "Leg" :
        Ik_jnt_Names = [f'DrvJnt_Leg_{side}',f'DrvJnt_Knee_{side}',f'DrvJnt_Ankle_{side}']
    elif side == "Root" :
        Ik_jnt_Names = cmds.listRelatives("Bind_Root_Move", ad=True, fullPath=False, type="joint") or []
    
    else :
        raise ValueError("You need to select somethind that's end up by Arm_L or Leg_R for example ")
    


    if not side == "Root" :
        if cmds.objExists('Locs'):
            grp_Locs='Locs'
        else:
            grp_Locs = cmds.group(empty=True, name="Locs")

        cmds.parent(grp_Locs,'GlobalMove')
        name3="Foot"
        if objName =="Arm":
            name3="Hand"
        name1=f"Loc_Dist_{objName}_{side}"
        name2=f"Loc_Dist_{name3}_{side}"

        if objName =="Arm":
            name3="Hand"
        loc1=cmds.spaceLocator(name=name1)[0]
        loc2=cmds.spaceLocator(name=name2)[0]

        ## Mettre les Locs dans un dossier
        cmds.parent(loc1,grp_Locs)
        cmds.parent(loc2,grp_Locs)


        cmds.matchTransform(name1,Ik_jnt_Names[0], pos=True, rot=False, scale=False)
        cmds.matchTransform(name2,Ik_jnt_Names[2], pos=True, rot=False, scale=False)


    # Create a distanceBetween node
    if side == "Root" :
        distance_node = cmds.createNode('curveInfo', name=f'curveInfo_Spine')

    else:
        distance_node = cmds.createNode('distanceBetween', name=f'Distance_{objName}_{side}')


    mD_LegPourcDiv=cmds.createNode('multiplyDivide', name=f'MD_{objName}_{side}_Pourcent_Div')
    cmds.setAttr(f'{mD_LegPourcDiv}.operation',2)

    mD_LegPourcPow=cmds.createNode('multiplyDivide', name=f'MD_{objName}_{side}_Pourcent_Pow')
    cmds.setAttr(mD_LegPourcPow+ '.input2X',0.5 )
    cmds.setAttr(f'{mD_LegPourcPow}.operation',3)

    mD_LegStretchDiv=cmds.createNode('multiplyDivide', name=f'MD_{objName}_{side}_Stretch_Div')
    cmds.setAttr(mD_LegStretchDiv+'.input1X',1)
    cmds.setAttr(f'{mD_LegStretchDiv}.operation',2)

    cond_EvDist=cmds.createNode('condition', name=f'Cond_Evaluate_Dist_{objName}_{side}')
    cmds.setAttr(f'{cond_EvDist}.operation',3)

    cond_Stretch=cmds.createNode('condition', name=f'Cond_Stretch_{objName}_{side}')
    cmds.setAttr(f'{cond_Stretch}.operation', 0)
    cmds.setAttr(f'{cond_Stretch}.colorIfTrueR', 1)
    cmds.setAttr(f'{cond_Stretch}.colorIfTrueG', 1)
    cmds.setAttr(f'{cond_Stretch}.colorIfTrueB', 1)

    GlobalMult=cmds.createNode('multiplyDivide', name=f'Global_Relative_Scale_{objName}_Mult_{side}')

    # Connect the nodes
    if not side == "Root" :
        cmds.connectAttr(f'{name1}Shape.worldPosition[0]', f'{distance_node}.point1')
        cmds.connectAttr(f'{name2}Shape.worldPosition[0]', f'{distance_node}.point2')
        cmds.connectAttr(f'{distance_node}.distance', f'{mD_LegPourcDiv}.input1X')
    else:
        cmds.connectAttr(f'Crv_SpineShape.worldSpace', f'{distance_node}.inputCurve')
        cmds.connectAttr(f'{distance_node}.arcLength',f'{mD_LegPourcDiv}.input1X')

    cmds.connectAttr(f'{mD_LegPourcDiv}.outputX', f'{mD_LegPourcPow}.input1X')
    cmds.connectAttr(f'{mD_LegPourcPow}.outputX', f'{mD_LegStretchDiv}.input2X')
    cmds.connectAttr(f'{mD_LegStretchDiv}.outputX', f'{cond_EvDist}.colorIfTrueG')

    cmds.connectAttr(f'{mD_LegPourcDiv}.outputX', f'{cond_EvDist}.colorIfTrueR')

    cmds.connectAttr(f'{cond_EvDist}.outColor', f'{cond_Stretch}.colorIfFalse')

    cmds.connectAttr(f'{GlobalMult}.outputX', f'{mD_LegPourcDiv}.input2X')
    cmds.connectAttr(f'{GlobalMult}.outputX', f'{cond_EvDist}.secondTerm')
    cmds.connectAttr('GlobalMove.scale', f'{GlobalMult}.input1')

    if not side == "Root" :
        cmds.connectAttr(f'{distance_node}.distance', f'{cond_EvDist}.firstTerm')
        dist=smallUsefulFct.getDistBetweenJnts(Ik_jnt_Names[0],Ik_jnt_Names[1])+smallUsefulFct.getDistBetweenJnts(Ik_jnt_Names[1],Ik_jnt_Names[2])
        print (f'DIST     ::   {dist}')
    else:
        cmds.connectAttr(f'{distance_node}.arcLength',f'{cond_EvDist}.firstTerm')
        dist=cmds.getAttr(f'{distance_node}.arcLength')

    cmds.setAttr(f'{GlobalMult}.input2X',dist)


    if objName =="Arm":
        name3="Hand"

    ## Connecter Locator
    if not side == "Root" :
        cmds.pointConstraint(Ik_jnt_Names[0],name1,weight=1)
        cmds.pointConstraint(f'CTRL_{name3}_{side}',name2,weight=1)

        ##SI STRETCH N EXISTE PAS --> Le CREER
        if not cmds.objExists(f'CTRL_{name3}_{side}.Stretch_{objName}'):
            cmds.addAttr(f'CTRL_{name3}_{side}', longName=f'Stretch_{objName}', attributeType='bool', defaultValue=0,keyable=True)
        cmds.connectAttr(f'CTRL_{name3}_{side}.Stretch_{objName}', f'{cond_Stretch}.firstTerm')
    else:
        if not cmds.objExists(f'CTRL_Root.Stretch_Spine'): 
            cmds.addAttr(f'CTRL_Root', longName=f'Stretch_Spine', attributeType='bool', defaultValue=0,keyable=True)
        cmds.connectAttr(f'CTRL_Root.Stretch_Spine', f'{cond_Stretch}.firstTerm')

    ##Tout CONNECTER AUX JOINTS 
    for ik in Ik_jnt_Names:
        cmds.connectAttr(f'{cond_Stretch}.outColorR',f'{ik}.scaleX')
        cmds.connectAttr(f'{cond_Stretch}.outColorG',f'{ik}.scaleY')
        cmds.connectAttr(f'{cond_Stretch}.outColorG',f'{ik}.scaleZ')