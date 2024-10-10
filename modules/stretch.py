import maya.cmds as cmds
import smallUsefulFct
import math



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

        if cmds.listRelatives(grp_Locs,parent=True) == None:
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
    blacklist=['Bind_Hip','Bind_Leg_R','Bind_Leg_L']
    for ik in Ik_jnt_Names:
        if ik not in blacklist:
            cmds.connectAttr(f'{cond_Stretch}.outColorR',f'{ik}.scaleX')
            cmds.connectAttr(f'{cond_Stretch}.outColorG',f'{ik}.scaleY')
            cmds.connectAttr(f'{cond_Stretch}.outColorG',f'{ik}.scaleZ')
