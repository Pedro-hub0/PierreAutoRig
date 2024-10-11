import maya.cmds as cmds
import sys
import importlib
import os
# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)
import smallUsefulFct

importlib.reload(smallUsefulFct)


def createRibbon():
    smallUsefulFct.importFileFromScene('Ribbon_MatX')

def AttachRib(attach):
    selObj = []
    name="Shoulder_L"
    obj="none"
    side="none"
    cb_Rib=["Shoulder_L","Shoulder_R","Elbow_L","Elbow_R","Leg_L","Leg_R","Knee_L","Knee_R"]
    rib_check=[]
    for i in range(len(attach)):
        is_checked = cmds.checkBox(attach[i], query=True, value=True)
        if is_checked:
            rib_check.append(cb_Rib[i])
    objextremity=''
    isA=True
    for r in rib_check:
        ######REUSSIR A FAKE LES SELECT OBJ#######
        obj=r.split("_")[0]
        side=r.split("_")[1]
        ##Check##
        if obj == "Shoulder":
            selObj=[f"DrvJnt_{r}",f"DrvJnt_Elbow_{side}"]
            objSwitch="Arm"
        if obj == "Elbow":
            selObj=[f"DrvJnt_{r}",f"DrvJnt_Wrist_{side}"]
            objSwitch="Arm"
            objextremity="Wrist"
        if obj == "Leg":
            selObj=[f"DrvJnt_{r}",f"DrvJnt_Knee_{side}"]
            objSwitch="Leg"
        if obj == "Knee":
            selObj=[f"DrvJnt_{r}",f"DrvJnt_Ankle_{side}"]
            objSwitch="Leg"
            objextremity="Ankle"


        ##IMPORTE RIBBON
        createRibbon()
        if cmds.objExists(f'Ribbon_01_{obj}_{side}'):
            cmds.delete(f'Ribbon_01_{obj}_{side}')
        if cmds.objExists("Ribbon_01"):
            smallUsefulFct.addSuffix("Ribbon_01",f'_{obj}_{side}')
        else:        
            raise ValueError("There is no Ribbon with the name Ribbon_01  Met Ribbon_matX fait par Kelly dans ton dossier scene")

        GlobalRib=f"Ctrl_Global_Ribbon_01_{obj}_{side}"
        ARib= f'CTRL_Ribbon_A01_{obj}_{side}'
        BRib=f'CTRL_Ribbon_B01_{obj}_{side}'

        ##Parent le Ribbon a la jambe
        cmds.parentConstraint(selObj[0], selObj[1], GlobalRib, sr=["x","y","z"],maintainOffset=False)
        cmds.parentConstraint(selObj[0], GlobalRib, st=["x", "y","z"],maintainOffset=False)
        print(f'           :{selObj[0]}        {selObj[1]}')

  
        if cmds.objExists(ARib) and cmds.objExists(BRib):
            print(smallUsefulFct.getDistBetweenJnts(selObj[0],f'Bind_Ribbon_A01_{obj}_{side}'))
            print(smallUsefulFct.getDistBetweenJnts(selObj[1],f'Bind_Ribbon_A01_{obj}_{side}'))
            
            if not smallUsefulFct.getDistBetweenJnts(selObj[0],f'Bind_Ribbon_A01_{obj}_{side}')<smallUsefulFct.getDistBetweenJnts(selObj[1],f'Bind_Ribbon_A01_{obj}_{side}'):
                
                isA=False
                temp=selObj[0]
                selObj[0]=selObj[1]
                selObj[1]=temp
            else:
                isA=True
            cmds.pointConstraint(selObj[0],ARib,maintainOffset=False)
            cmds.pointConstraint(selObj[1],BRib,maintainOffset=False)
        else : 
            print(f'{ARib} AND {BRib}') 

        ##NON ROLL##
        ##Wrist --> Connect Arm fk and ik with condition at the Ribbon
        if obj in ("Elbow","Knee") :
            condition_node_elbow = cmds.createNode('condition', name=f'condition_{objextremity}_{side}')
            if obj=="Knee":
                cmds.connectAttr(f'CTRL_Foot_{side}.rotate',f'{condition_node_elbow}.colorIfTrue')                
            else:
                cmds.connectAttr(f'DrvJnt_{objextremity}_{side}.rotate',f'{condition_node_elbow}.colorIfTrue')
            cmds.connectAttr(f'Fk_{objextremity}_{side}.rotate',f'{condition_node_elbow}.colorIfFalse')
            cmds.connectAttr(f'CTRL_IkFk_{objSwitch}_{side}.Switch_Ik_Fk',f'{condition_node_elbow}.firstTerm') 
            cmds.setAttr(f'{condition_node_elbow}.operation',0)
            cmds.setAttr(f'{condition_node_elbow}.secondTerm',1)
            if not isA:
                cmds.connectAttr(f'{condition_node_elbow}.outColorR',f'{ARib}.rotateX')
                cmds.connectAttr(f'{condition_node_elbow}.outColorG',f'{ARib}.rotateY') 
            else:
                cmds.connectAttr(f'{condition_node_elbow}.outColorR',f'{BRib}.rotateX') 
                cmds.connectAttr(f'{condition_node_elbow}.outColorG',f'{BRib}.rotateY') 


        ##SHOULDER 
        if obj in ("Shoulder","Leg"):
            locs_NonRoll=[f'Loc_Twist_{obj}_01_{side}',f'Loc_Twist_{obj}_02_{side}']
            for l in range(len(locs_NonRoll)):
                if cmds.objExists(f'{locs_NonRoll[l]}_Move'):
                    cmds.delete(f'{locs_NonRoll[l]}_Move')
                if cmds.objExists(f'{locs_NonRoll[l]}'):
                    cmds.delete(f'{locs_NonRoll[l]}')

                cmds.spaceLocator(name=locs_NonRoll[l])[0]
            
            #Loc 01
            cmds.parent(locs_NonRoll[0],f'DrvJnt_{obj}_{side}')
            smallUsefulFct.cleanTransform(locs_NonRoll[0])
            
            #Loc 02
            rotateDrvJnt=cmds.xform(f'DrvJnt_{obj}_{side}', query=True, worldSpace=True, rotation=True)
            translateDrvJnt=cmds.xform(f'DrvJnt_{obj}_{side}', query=True, worldSpace=True, translation=True)
            if obj=="Leg":
                cmds.parent(locs_NonRoll[1],f'Bind_Hip')
            else:
                cmds.parent(locs_NonRoll[1],f'Bind_Clavicule_01_{side}')
            #Put the same translate and rotate than the DrvJnt
            cmds.xform(locs_NonRoll[1], rotation=rotateDrvJnt, worldSpace=True, translation=translateDrvJnt)
            smallUsefulFct.offset2(locs_NonRoll[1])
        
            ##Create the nodale Behind

            mult_matrix_node = cmds.createNode('multMatrix', name=f'myMultMatrix_Nonroll_{obj}_{side}')
            decompose_node = cmds.createNode('decomposeMatrix', name=f'myDecomposeMatrix_Nonroll_{obj}_{side}')

            axes=["X","Y","Z"]
            cmds.connectAttr(locs_NonRoll[0] + ".worldMatrix[0]", mult_matrix_node + ".matrixIn[0]")
            cmds.connectAttr(locs_NonRoll[1] + ".worldInverseMatrix[0]", mult_matrix_node + ".matrixIn[1]")
            cmds.connectAttr(mult_matrix_node + ".matrixSum", decompose_node + ".inputMatrix")
            
            for a in axes:
                quat_to_euler_node = cmds.createNode('quatToEuler', name=f'myQuatToEuler_Nonroll_{a}_{obj}_{side}')
                cmds.connectAttr(f'{decompose_node}.outputQuatW', f'{quat_to_euler_node}.inputQuatW')   
                cmds.connectAttr(f'{decompose_node}.outputQuat{a}',f'{quat_to_euler_node}.inputQuat{a}')
                if a=='X':
                    if isA:
                        cmds.connectAttr(f'{quat_to_euler_node}.outputRotateX',f'{ARib}.rotateX')
                    else:
                        cmds.connectAttr(f'{quat_to_euler_node}.outputRotateX',f'{BRib}.rotateX')

    

        if not cmds.attributeQuery(f'Bend_{objSwitch}_{side}', node=f'CTRL_IkFk_{objSwitch}_{side}', exists=True):
            cmds.addAttr(f'CTRL_IkFk_{objSwitch}_{side}', longName=f'Bend_{objSwitch}_{side}', attributeType='bool', defaultValue=0,keyable=True)
        cmds.connectAttr(f'CTRL_IkFk_{objSwitch}_{side}.Bend_{objSwitch}_{side}',f"CTRL_Ribbon_Mid_01_{obj}_{side}.visibility")
        parent=cmds.listRelatives(f"CTRL_Ribbon_Mid_01_{obj}_{side}",parent=True)[0]
        translateMidCtrl=cmds.getAttr(f'{parent}.translateX')
        smallUsefulFct.offset2(f"CTRL_Ribbon_Mid_01_{obj}_{side}")
        #cmds.parent(f"CTRL_Ribbon_Mid_01_{obj}_{side}_Offset",f'CTRL_Ribbon_Mid_01_Move_{obj}_{side}')
        cmds.setAttr(f"CTRL_Ribbon_Mid_01_{obj}_{side}_Offset.translateX",(-1)*translateMidCtrl)
        
        ##  Organiser
        if cmds.objExists('GlobalMove'):
            if not cmds.objExists('grp_Ribbon'):
                grp_Ribbon = cmds.group(empty=True, name="grp_Ribbon")
            else:
                grp_Ribbon="grp_Ribbon"       
            cmds.parent(f'Ribbon_01_{obj}_{side}',grp_Ribbon)
            if not cmds.objExists('ExtraNodes'):
                grp_Extranode = cmds.group(empty=True, name="ExtraNodes")
            else:
                grp_Extranode="ExtraNodes"

            if cmds.objExists('Perso01'):
                if cmds.listRelatives(grp_Extranode,parent=True) == None:
                    cmds.parent(grp_Extranode,'Perso01')
            
            if cmds.listRelatives(grp_Ribbon,parent=True) == None:                
                cmds.parent(grp_Ribbon,grp_Extranode)







        """
        if(obj=="Leg" or obj=="Shoulder" ):
            if(obj=="Leg"):
                name="Knee"
            if(obj=="Shoulder"):
                name="Arm"

        if cmds.objExists(f'Preserve_{name}_{side}'):
    ## Node Legs
                print("I'm Here")
                RibLeg_Mult=cmds.createNode('multiplyDivide', name=f'Preserve_{name}_{side}_Mult')
                cmds.setAttr(RibLeg_Mult+'.input2X',-0.5)
                Rev_Leg=cmds.createNode('reverse', name=f'{name}_{side}_Rev_Rotate_X')

                cmds.connectAttr(f'{selObj[0]}.rotateX', f'{Rev_Leg}.inputX')
                cmds.connectAttr(f'{selObj[0]}.rotateZ', f'{RibLeg_Mult}.input1X')

                #cmds.connectAttr(f'{RibLeg_Mult}.outputX',f'Preserve_{name}_{side}.rotateX')
                if cmds.objExists(ARib):
                    cmds.connectAttr(f'{Rev_Leg}.outputX',f'{ARib}.rotateX' )
                else :
                    print(f'{ARib} NOT FOUND ')
            
        else :
            print(f'Preserve_{name}_{side} NOT FOUND ')

       #if(obj=="Knee"):
       #    name="Foot"

       #    if cmds.objExists(f'Bind_{name}_{side}') and cmds.objExists(BRib) :
       #        cmds.connectAttr(f'Bind_{name}_{side}.rotateX',f'{BRib}.rotateX')
       #    else :
       #        print(f'Bind_{name}_{side} AND {BRib}.rotateX NOT FOUND ')


        ##A RAJOUTER --> Contrainte point Drv_Arm --> Loc Arm// CTRL Hand --> Loc Hand
        """

####################################
#         FONCTION NON ROLL        #
####################################
    
def NonrollFct(taille) :
    temp=[]