import maya.cmds as cmds
import sys
import os
# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)
import smallUsefulFct
import math


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


    for r in rib_check:
        ######REUSSIR A FAKE LES SELECT OBJ#######
        obj=r.split("_")[0]
        side=r.split("_")[1]
        ##Check##
        if obj == "Shoulder":
            selObj=[f"DrvJnt_{r}",f"DrvJnt_Elbow_{side}"]
        if obj == "Elbow":
            selObj=[f"DrvJnt_{r}",f"DrvJnt_Wrist_{side}"]
        
        if obj == "Leg":
            selObj=[f"DrvJnt_{r}",f"DrvJnt_Knee_{side}"]
        if obj == "Knee":
            selObj=[f"DrvJnt_{r}",f"DrvJnt_Ankle_{side}"]

        ##IMPORTE RIBBON
        createRibbon()
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

       
  
        if cmds.objExists(ARib) and cmds.objExists(BRib):
            if not smallUsefulFct.getDistBetweenJnts(selObj[0],ARib)<smallUsefulFct.getDistBetweenJnts(selObj[1],ARib):
                temp=selObj[0]
                selObj[0]=selObj[1]
                selObj[1]=temp
            cmds.pointConstraint(selObj[0],ARib,maintainOffset=False)
            cmds.pointConstraint(selObj[1],BRib,maintainOffset=False)
        else : 
            print(f'{ARib} AND {BRib}')
            




        

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