import maya.cmds as cmds
import smallUsefulFct
import math
import os
import importlib
importlib.reload(smallUsefulFct)


#############################
#     FONCTIONS FOOT        #
#############################

def createLocs(cb_toeNumber,cb_Toe):
    selObj = cmds.ls(selection=True)
    isToe=cmds.checkBox(cb_Toe, query=True, value=True)
    toeNumber=cmds.intField(cb_toeNumber, query=True, value=True)
    if len(selObj) <1:
        raise ValueError("You need to select something which finish by L or R ")
    side=selObj[0][-1]
    locator_names = ["Loc_Heel_"+side, "Loc_Ball_"+side,"Loc_Bank_Int_"+side,"Loc_Bank_Ext_"+side]

    #initialise names (can be optimised because it's created in 2 def)
   
    locator_names.append(f"Loc_Toe_{side}")
    if isToe:
        for i in range(0,toeNumber):
            locator_names.append(f"Loc_Toe_{i}_Start_{side}")
            locator_names.append(f"Loc_Toe_{i}_Mid_{side}")
            locator_names.append(f"Loc_Toe_{i}_End_{side}")
    
    
    folder_names = ["Pivot_Ball_"+side, "Pivot_Toe_"+side, "Pivot_Toe_"+side+"_Offset"]
    for name in locator_names:
        cmds.spaceLocator(name=name)[0]
    for name in folder_names:
        cmds.group(empty=True, name=name)

    #Organiser
    if not cmds.objExists(f"Grp_temp_Locs_Foot_{side}") :
        cmds.group(empty=True, name=f"Grp_temp_Locs_Foot_{side}")
        cmds.parent(locator_names,f"Grp_temp_Locs_Foot_{side}")
        cmds.parent(folder_names,f"Grp_temp_Locs_Foot_{side}")

    if isToe:
        limit=(len(locator_names))-(toeNumber*3)
        i=len(locator_names)-1
        y=1
        while limit<i:
            cmds.parent(locator_names[i],locator_names[i-1])
            if y%2==0:
                i=i-1
            i-=1
            y+=1


def OrganiseLocs(sz,cb_ToeNumber,cb_Toe):

    selObj = cmds.ls(selection=True)
    isToe=cmds.checkBox(cb_Toe, query=True, value=True)
    toeNumber=cmds.intField(cb_ToeNumber, query=True, value=True)
    if len(selObj) <1:
        raise ValueError("You need to select something which finish by L or R ")
    side=selObj[0][-1]
    if not cmds.objExists(f'CTRL_Foot_{side}'):
        raise ValueError("You need to create the leg before")
    #initialise names (can be optimised because it's created in 2 def)
    loc_names = ["Loc_Heel_"+side,"Loc_Toe_"+side,"Loc_Ball_"+side,"Loc_Bank_Ext_"+side, "Loc_Bank_Int_"+side,"CTRL_Foot_"+side]
    folder_names = ["Pivot_Ball_"+side, "Pivot_Toe_"+side, "Pivot_Toe_"+side+"_Offset"]
    ik_names=["Ik_Toe_"+side,"Ik_Leg_"+side,"Ik_Ball_"+side]
    fk_names=["Fk_Foot_"+side,"Fk_Ball_"+side,"Fk_Toe_"+side]
    jnt_names=["Bind_Foot_"+side,"Bind_Ball_"+side,"Bind_Toe_"+side]
    jnts=[]
    FkCtrl=[]
    LocsToe=[]
    iks=[]
    count=0
    size=smallUsefulFct.GetDistLocScale(sz)

    ##INITIALISE TOES
    if isToe:
        for i in range(0,toeNumber):
            LocsToe.append(f"Loc_Toe_{i}_Start_{side}")
            LocsToe.append(f"Loc_Toe_{i}_Mid_{side}")
            LocsToe.append(f"Loc_Toe_{i}_End_{side}")



    #Create Joints IKs Foot
    tr_Ankle = cmds.xform(f'DrvJnt_Ankle_{side}', query=True, translation=True, worldSpace=True)
    tr_Ball = cmds.xform(f'{loc_names[2]}', query=True, translation=True, worldSpace=True)
    cmds.select(clear=True)
    jnts.append(cmds.joint(n=f'{jnt_names[0]}',p=tr_Ankle))
    jnts.append(cmds.joint(n=f'{jnt_names[1]}',p=tr_Ball))

    
    if not isToe:
        tr_Toe = cmds.xform(f'{loc_names[1]}', query=True, translation=True, worldSpace=True)
        jnts.append(cmds.joint(n=f'{jnt_names[2]}',p=tr_Toe))
    else:
        tr_Toe=[]
        y=1
        for i in range(0,toeNumber*3):
            tempTrToe=cmds.xform(f'{LocsToe[i]}', query=True, translation=True, worldSpace=True)
            tr_Toe.append(tempTrToe)
            tempJnt=cmds.joint(n=f'Bind_{"_".join(LocsToe[i].split("_")[1:])}',p=tempTrToe)
            jnts.append(tempJnt)
            if y%3==0:
                cmds.select(jnt_names[1])
            y+=1
        
    
    cmds.select(clear=True)
    smallUsefulFct.move(jnts[0])
    DistanceRepere=smallUsefulFct.getDistBetweenJnts(jnts[len(jnts)-1],jnts[len(jnts)-2])
    #Orient    joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;
    cmds.joint(jnts[0],e=True, oj='xyz', sao='yup', ch=True, zso=True)
    if not isToe:
        cmds.joint(f'{jnts[len(jnts)-1]}',e=True, oj='none', ch=True, zso=True) 
    else:
        for obj in jnts:
            if  obj.split("_")[-1]=="End":
                cmds.joint(f'{obj}',e=True, oj='none', ch=True, zso=True) 

    #Create Joints FKs Foot
    FkJnts=cmds.duplicate(jnt_names[0], rc=True)
    i=0
    while i<len(FkJnts):
        cmds.rename(FkJnts[i], f'Fk_{"_".join(jnts[i].split("_")[1:])}')
        FkJnts[i]=  f'Fk_{"_".join(jnts[i].split("_")[1:])}'
        i+=1
    smallUsefulFct.move(FkJnts[0])



    #Iks
    iks.append(cmds.ikHandle(startJoint=jnts[0], endEffector=jnts[1], solver='ikRPsolver', name=f'{ik_names[2]}')[0])
    if not isToe:
        iks.append(cmds.ikHandle(startJoint=jnts[1], endEffector=jnts[2], solver='ikRPsolver', name=f'{ik_names[0]}')[0])
    else:

        grpBallsIks=cmds.group(empty=True, name=f'grp_Balls_Iks')
        grpToesIks=cmds.group(empty=True, name=f'grp_Toes_Iks')
        y=0
        for i in range(0,len(jnts)):
            if jnts[i].split("_")[-2] in ["Start"]: 
                tempik1=cmds.ikHandle(startJoint=jnt_names[1], endEffector=jnts[i], solver='ikRPsolver', name=f'ikHandle_{jnt_names[1]}_Toe{i}')[0]
                tempik2=cmds.ikHandle(startJoint=jnts[i], endEffector=jnts[i+2], solver='ikRPsolver', name=f'ikHandle_{jnts[i]}')[0]
                iks.append(tempik1)
                cmds.parent(tempik1,grpBallsIks)
                iks.append(tempik2)
                cmds.parent(tempik2,grpToesIks)


            """  if jnts[i].split("_")[-2] in ["Mid"]:   
                TranslatePV = cmds.xform(jnts[i], q=True, t=True, ws=True)
                CTRLPv=cmds.circle(name=f'CTRL_PV_Toe_{y}_{side}',radius=DistanceRepere,nr=[1,0,0])[0]
                smallUsefulFct.set_curve_color(CTRLPv,9)
                cmds.xform(CTRLPv, t=TranslatePV, ws=True)
                cmds.poleVectorConstraint(CTRLPv,tempik1)
                cmds.pointConstraint(tempik1,f'CTRL_Foot_{side}')
                smallUsefulFct.move2(CTRLPv)

                y+=1"""

    #CTRL FKs
    if not isToe:
        FkCtrl.append(cmds.circle(name=f'CTRL_Fk_Ball_{side}',radius=size,nr=[1,0,0])[0])
        FkCtrl.append(cmds.circle(name=f'CTRL_Fk_Toe_{side}',radius=size,nr=[1,0,0])[0])
    else:
        for fk in FkJnts:
            if fk != f"Fk_Foot_{side}":
                FkCtrl.append(cmds.circle(name=f'CTRL_{fk}',radius=size,nr=[1,0,0])[0])


    i=0

    #Fk Controller -- Move and do the hierarchy --
    while i<len(FkCtrl):
        TranslateJnt = cmds.xform(FkJnts[i+1], q=True, t=True, ws=True)
        RotationJnt = cmds.xform(FkJnts[i+1], query=True, rotation=True, worldSpace=True)
        smallUsefulFct.set_curve_color(FkCtrl[i],28)
        cmds.xform(FkCtrl[i], t=TranslateJnt, ro=RotationJnt, ws=True)
        smallUsefulFct.offset(FkCtrl[i])
        if i>0:
            cmds.parent(f'{FkCtrl[i]}_Offset',FkCtrl[i-1])
        if isToe:
            if jnts[i].split("_")[-2] in ["Start"]:
                cmds.parent(f'{FkCtrl[i]}_Offset',FkJnts[0])

        i+=1

    #Parents Chains
    i=0
    #Fk --Constraint Controller --
    while i<len(FkCtrl):
        cmds.parentConstraint(FkCtrl[i],FkJnts[i+1], maintainOffset=True, weight=1)
        i+=1
    #Parents Chaines
    cmds.parentConstraint(f'DrvJnt_Ankle_{side}',f'{jnt_names[0]}_Move', maintainOffset=True, weight=1)
    cmds.parentConstraint(f'Fk_Ankle_{side}',f'{FkJnts[0]}_Move', maintainOffset=True, weight=1)

    
    #PairBlend
    MyPbFct("Foot",side,f'CTRL_IkFk_Leg_{side}',jnts,FkJnts,iks)
    #Parents Locs
    while count<len(loc_names)-1:
        if cmds.objExists(loc_names[count]) and cmds.objExists(loc_names[count+1]):
            cmds.parent(loc_names[count], loc_names[count+1])    
            count +=1
        else :
            print("marche pas ")
            break

    #CTRL Ik Toes
    if isToe:
        ikToes=cmds.listRelatives(grpToesIks, allDescendents=True)
        for ik in ikToes:
            TranslateIk = cmds.xform(ik, q=True, t=True, ws=True)
            CTRLIk=cmds.circle(name=f'CTRL_{ik}',radius=DistanceRepere,nr=[1,0,0])[0]
            smallUsefulFct.set_curve_color(CTRLIk,9)
            cmds.xform(CTRLIk, t=TranslateIk, ws=True)
            cmds.parentConstraint(CTRLIk,ik)
            smallUsefulFct.move2(CTRLIk)



   #Parents Locs empty folder
    if cmds.objExists(folder_names[1]) and cmds.objExists(folder_names[2]):
        cmds.xform(folder_names[1], translation=tr_Ball, worldSpace=True)
        cmds.parent(folder_names[1], folder_names[2])
    if cmds.objExists(folder_names[2]) and cmds.objExists(loc_names[0]):
        cmds.xform(folder_names[1], translation=tr_Ball, worldSpace=True)
        cmds.parent(folder_names[2], loc_names[0])
    if cmds.objExists(folder_names[0]) and cmds.objExists(loc_names[0]):
        cmds.xform(folder_names[0], translation=tr_Ball, worldSpace=True)
        cmds.parent(folder_names[0], loc_names[0])
    if isToe:
        cmds.parent(grpBallsIks,folder_names[1])
        cmds.parent(grpToesIks,folder_names[1])
    """
    for n in loc_names:
        if cmds.objExists(n):
            cmds.makeIdentity(n, apply=True, t=False, r=True, s=False)
    """
    smallUsefulFct.offset2(loc_names[-2])
 # #Parents Iks 
    if cmds.objExists(ik_names[2]) and cmds.objExists(loc_names[0]):
        cmds.parent(ik_names[2], loc_names[0])
    if cmds.objExists(ik_names[0]) and cmds.objExists(folder_names[1]):
        cmds.parent(ik_names[0], folder_names[1])

    if cmds.objExists(ik_names[1]) and cmds.objExists(folder_names[0]):
        cmds.parent(ik_names[1], folder_names[0])



   ##ORGANISE    
    cmds.parent(f'{jnt_names[0]}_Offset',"JNT")
    cmds.parent(f'{FkJnts[0]}_Offset',"JNT")
    cmds.parent(f'{FkCtrl[0]}_Offset',f'CTRL_Fk_Foot_{side}')
    if not cmds.objExists(f'CTRL_Foot_{side}_Offset'):
        smallUsefulFct.move(f'CTRL_Foot_{side}')
        
    cmds.parent(f'CTRL_Foot_{side}_Offset',"CTRL")
    

def ConnectFoot():
    selObj = cmds.ls(selection=True)
    if len(selObj) <1:
        raise ValueError("You need to select something which finish by L or R ")
    side=selObj[0][-1]
    # variables Bank
    exp_L = """ if(CTRL_Foot_L.Bank_L<=0){
    Loc_Bank_Ext_L.rotateZ=CTRL_Foot_L.Bank_L;
    }else{Loc_Bank_Ext_L.rotateZ=0;}

    if(CTRL_Foot_L.Bank_L>=0){
    Loc_Bank_Int_L.rotateZ=CTRL_Foot_L.Bank_L;
    }else{Loc_Bank_Int_L.rotateZ=0;}"""
           
    
    exp_name_L = "Exp_Bank_Legs_L"
    
    exp_R =  """ if(CTRL_Foot_R.Bank_R<=0){
    Loc_Bank_Ext_R.rotateZ=CTRL_Foot_R.Bank_R;
    }else{Loc_Bank_Ext_R.rotateZ=0;}

    if(CTRL_Foot_R.Bank_R>=0){
    Loc_Bank_Int_R.rotateZ=CTRL_Foot_R.Bank_R;
    }else{Loc_Bank_Int_R.rotateZ=0;}"""
    
    exp_name_R = "Exp_Bank_Legs_R"



    # Create the expression
    if side == "L" :
        Ctrl="CTRL_Foot_L"
        # Expression Bank
        cmds.expression(name=exp_name_L, string=exp_L)

        #VARIABLES
        #Toe
        remapFlexToe = cmds.createNode('remapValue', name='remapV_FlexToe_'+side)
        remapToeRotY = cmds.createNode('remapValue', name='remapV_Toe_Rot_Y_'+side)
        #FootRoll
        remapFRPivotRotX = cmds.createNode('remapValue', name='remapV_FootRoll_PivotBall_RotX_'+side)
        remapFRToeRotX = cmds.createNode('remapValue', name='remapV_FootRoll_Toe_RotX_'+side)
        remapFRHeelRotX = cmds.createNode('remapValue', name='remapV_FootRoll_Heel_RotX_'+side)
        #Heel
        remapHeelRotY = cmds.createNode('remapValue', name='remapV_Heel_RotY_'+side)

        # INITIALISE
        smallUsefulFct.initialiseRemap(remapFlexToe,-1,1,-20,20)
        smallUsefulFct.initialiseRemap(remapToeRotY,-1,1,-70,70)

        smallUsefulFct.initialiseRemap(remapFRPivotRotX,0,1,0,45)
        smallUsefulFct.initialiseRemap(remapFRToeRotX,0,1,0,45)
        smallUsefulFct.initialiseRemap(remapFRHeelRotX,-1,0,-40,0)

        smallUsefulFct.initialiseRemap(remapHeelRotY,-1,1,-40,70)

        cmds.setAttr(f"{remapFRPivotRotX}.value[3].value_Position", 0.5)
        cmds.setAttr(f"{remapFRPivotRotX}.value[3].value_FloatValue",1)
        cmds.setAttr(f"{remapFRPivotRotX}.value[3].value_Interp", 1)

        cmds.setAttr(f"{remapFRPivotRotX}.value[1].value_Position", 1)
        cmds.setAttr(f"{remapFRPivotRotX}.value[1].value_FloatValue",0)
        cmds.setAttr(f"{remapFRPivotRotX}.value[1].value_Interp", 1)
 
        cmds.setAttr(f"{remapHeelRotY}.value[3].value_Position", 0.5)
        cmds.setAttr(f"{remapHeelRotY}.value[3].value_FloatValue",0.364)
        cmds.setAttr(f"{remapHeelRotY}.value[3].value_Interp", 1)



        #CONNECT
        #Toe
        cmds.connectAttr(Ctrl + ".Flex_Toe_L", remapFlexToe+".inputValue")
        cmds.connectAttr(remapFlexToe+".outValue","Pivot_Toe_L.rotateX")

        cmds.connectAttr(Ctrl + ".Twist_Toe_L", remapToeRotY+".inputValue")
        cmds.connectAttr(remapToeRotY+".outValue","Loc_Toe_L.rotateY")

        #FootRoll
        Rotate=cmds.getAttr(f'Pivot_Ball_L.rotateX')
        if Rotate!= 0:
            smallUsefulFct.offset2(f'Pivot_Ball_L')
        cmds.connectAttr(Ctrl + ".Foot_Roll_L", remapFRPivotRotX+".inputValue")
        cmds.connectAttr(remapFRPivotRotX+".outValue","Pivot_Ball_L.rotateX")

        cmds.connectAttr(Ctrl + ".Foot_Roll_L", remapFRToeRotX+".inputValue")
        cmds.connectAttr(remapFRToeRotX+".outValue","Loc_Toe_L.rotateX")

        cmds.connectAttr(Ctrl + ".Foot_Roll_L", remapFRHeelRotX+".inputValue")
        cmds.connectAttr(remapFRHeelRotX+".outValue","Loc_Heel_L.rotateX")

        #Heel
        cmds.connectAttr(Ctrl + ".Twist_Heel_L", remapHeelRotY+".inputValue")
        cmds.connectAttr(remapHeelRotY+".outValue","Loc_Heel_L.rotateY")


    if side == "R" :
        Ctrl="CTRL_Foot_R"
        # Expression Bank
        cmds.expression(name=exp_name_R, string=exp_R)

        #VARIABLES
        #Toe
        remapFlexToe = cmds.createNode('remapValue', name='remapV_FlexToe_'+side)
        remapToeRotY = cmds.createNode('remapValue', name='remapV_Toe_Rot_Y_'+side)
        #FootRoll
        remapFRPivotRotX = cmds.createNode('remapValue', name='remapV_FootRoll_PivotBall_RotX_'+side)
        remapFRToeRotX = cmds.createNode('remapValue', name='remapV_FootRoll_Toe_RotX_'+side)
        remapFRHeelRotX = cmds.createNode('remapValue', name='remapV_FootRoll_Heel_RotX_'+side)
        #Heel
        remapHeelRotY = cmds.createNode('remapValue', name='remapV_Heel_RotY_'+side)

        # INITIALISE
        smallUsefulFct.initialiseRemap(remapFlexToe,-1,1,-20,20)
        smallUsefulFct.initialiseRemap(remapToeRotY,-1,1,-70,70)

        smallUsefulFct.initialiseRemap(remapFRPivotRotX,0,1,0,-45)


 
        smallUsefulFct.initialiseRemap(remapFRToeRotX,0,1,0,45)
        smallUsefulFct.initialiseRemap(remapFRHeelRotX,-1,0,-40,0)

        smallUsefulFct.initialiseRemap(remapHeelRotY,-1,1,-70,40)
        cmds.setAttr(f"{remapFRPivotRotX}.value[3].value_Position", 0.5)
        cmds.setAttr(f"{remapFRPivotRotX}.value[3].value_FloatValue",1)
        cmds.setAttr(f"{remapFRPivotRotX}.value[3].value_Interp", 1)

        cmds.setAttr(f"{remapFRPivotRotX}.value[1].value_Position", 1)
        cmds.setAttr(f"{remapFRPivotRotX}.value[1].value_FloatValue",0)
        cmds.setAttr(f"{remapFRPivotRotX}.value[1].value_Interp", 1)

        cmds.setAttr(f"{remapHeelRotY}.value[3].value_Position", 0.5)
        cmds.setAttr(f"{remapHeelRotY}.value[3].value_FloatValue",0.636)
        cmds.setAttr(f"{remapHeelRotY}.value[3].value_Interp", 1)


        
        #CONNECT
        #Toe
        cmds.connectAttr(Ctrl + ".Flex_Toe_R", remapFlexToe+".inputValue")
        cmds.connectAttr(remapFlexToe+".outValue","Pivot_Toe_R.rotateX")

        cmds.connectAttr(Ctrl + ".Twist_Toe_R", remapToeRotY+".inputValue")
        cmds.connectAttr(remapToeRotY+".outValue","Loc_Toe_R.rotateY")
        
        #FootRoll
        Rotate=cmds.getAttr(f'Pivot_Ball_R.rotateX')
        if Rotate!= 0:
            smallUsefulFct.offset2(f'Pivot_Ball_R')
        cmds.connectAttr(Ctrl + ".Foot_Roll_R", remapFRPivotRotX+".inputValue")
        cmds.connectAttr(remapFRPivotRotX+".outValue","Pivot_Ball_R.rotateX")
        

        cmds.connectAttr(Ctrl + ".Foot_Roll_R", remapFRToeRotX+".inputValue")
        cmds.connectAttr(remapFRToeRotX+".outValue","Loc_Toe_R.rotateX")
    
        cmds.connectAttr(Ctrl + ".Foot_Roll_R", remapFRHeelRotX+".inputValue")
        cmds.connectAttr(remapFRHeelRotX+".outValue","Loc_Heel_R.rotateX")
        
        #Heel
        cmds.connectAttr(Ctrl + ".Twist_Heel_R", remapHeelRotY+".inputValue")
        cmds.connectAttr(remapHeelRotY+".outValue","Loc_Heel_R.rotateY")


    if cmds.objExists(f'Ik_Leg_{side}'):
        cmds.connectAttr(Ctrl + ".Twist_Leg", f'Ik_Leg_{side}.twist')


def mirorFeet():
    selObj = cmds.ls(selection=True)
    side=selObj[0][-1]
    otherside = "R" if side == "L" else "L"
    if len(selObj) <=1:
        if side not in ["L","R"]: 
            raise ValueError("You need to select something which finish by L or R ")
    else:
            raise ValueError("You need to select just 1 thing which finish by L or R ")


###################################
###PAIR BLEND (Fil Rouge Code)####
###################################

def MyPbFct(ob,side,Ctrl,ik,fk,iks):
    i=0
    #CONNECTIONS PAIR BLEND
    while i < len(fk):
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


    for ikhandle in iks:
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"{ikhandle}.ikBlend")


    cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"Bind_{ob}_{side}.visibility")
    reverse_node = f'Rev_Leg_{side}_IkFk'

    conn=cmds.listConnections(f"CTRL_{ob}_{side}.visibility")
    if cmds.objExists(reverse_node):
        cmds.connectAttr(f"{reverse_node}.outputX",f"Fk_{ob}_{side}.visibility")
    if not conn:
        cmds.connectAttr(Ctrl+".Switch_Ik_Fk",f"CTRL_{ob}_{side}.visibility")



def mirorFoot(cb_jnt,cb_ctrl,sizeCtrlArm):
    cb_ctrl_val =True
    cb_jnt_val = True
    #Initialisation
    if cb_jnt!=True:
        cb_ctrl_val = cmds.checkBox(cb_ctrl, query=True, value=True)
        cb_jnt_val = cmds.checkBox(cb_jnt, query=True, value=True)
    locs_Sort=[]
    selObj = cmds.ls(selection=True)
    newName=[]
    side=selObj[0][-1]
    locator_names = ["Loc_Heel_"+side, "Loc_Ball_"+side, "Loc_Toe_"+side,"Loc_Bank_Int_"+side,"Loc_Bank_Ext_"+side]
    otherside = "R" if side == "L" else "L"
    folder_names = ["Pivot_Ball_"+otherside, "Pivot_Toe_"+otherside, "Pivot_Toe_"+otherside+"_Offset"]



    if len(selObj) <=1:
        if side not in ["L","R"]: 
            raise ValueError("You need to select something which finish by L or R ")
    else:
            raise ValueError("You need to select just 1 thing which finish by L or R ")

    if cmds.objExists("Bind_Root"):
        tr_BindRoot = cmds.xform("Bind_Root", query=True, worldSpace=True, translation=True)
    else:
        raise ValueError("You need to create a Bind_Root")
    
    # Create a new group (folder)
    temp_grp01 = cmds.group(empty=True, name="temp_grp01")
    # Set the translation for the group
    cmds.xform(temp_grp01, worldSpace=True, translation=tr_BindRoot)

    #Duplicate just the locs
    # Get all the children of the parent
    temp_dup_loc=cmds.duplicate(locator_names[-2], rr=True)[0]
    cmds.parent(temp_dup_loc,temp_grp01)
    children = cmds.listRelatives(temp_dup_loc, allDescendents=True, fullPath=True, type='transform', noIntermediate=True) or []


    # Iterate through the children
    if len(children)>1:

        for child in children:
            nwLoc=child.split("|")[-1]
            chObj=nwLoc.split('_')[0]
            print(f'Child   {child} {chObj}')
            if chObj=="Loc":
                nwname=f'{nwLoc[:-1]}{otherside}'
                cmds.rename(child,nwname)
                cmds.parent(nwname, temp_grp01) 
                locs_Sort.append(nwname)
            else:
                cmds.delete(child)

        nwLoc=temp_dup_loc.split("|")[-1]
        nwname=f'{nwLoc[:-2]}{otherside}'
        cmds.rename(temp_dup_loc,nwname)
        if cmds.listRelatives(nwname, parent=True)[0] != temp_grp01:
            cmds.parent(nwname, temp_grp01) 

            
    else:        
        for f in locator_names:
            newName=cmds.duplicate(f, rr=True,n=f'{f[:-1]}{otherside}')[0]
            cmds.parent(newName,temp_grp01)
        
  

    cmds.xform(temp_grp01, scale=[-1, 1, 1], worldSpace=True)

    lstNewLocs=cmds.listRelatives(temp_grp01,allDescendents=True)
    #Parent
    for f in lstNewLocs:
        if cmds.listRelatives(f,parent=True)[0] == temp_grp01:
            cmds.parent(f,world=True)

    #Delete Parent groupe
    cmds.delete(temp_grp01)

    for name in folder_names:
        cmds.group(empty=True, name=name)

    ctrlName=f'CTRL_Foot_{otherside}'
    if not cmds.objExists(ctrlName):
        cmds.circle(name=ctrlName)[0]
    #createAttributFoot(ctrlName,otherside)

    
    #Use the last codes
    if cb_jnt_val:
        cmds.select(f"CTRL_IkFk_Leg_{otherside}")
        OrganiseLocs(sizeCtrlArm)

    if cb_ctrl_val:
        cmds.select(f"CTRL_IkFk_Leg_{otherside}")
        ConnectFoot()





def createAttributFoot(ctrlName,side):
    #Create attribute in the controller
    cmds.addAttr(ctrlName, longName='___', attributeType='enum', enumName='____', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Twist_Leg', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='__', attributeType='enum', enumName='____', defaultValue=0,keyable=True,niceName="___")

    cmds.addAttr(ctrlName, longName='Foot_Roll_'+side, attributeType='float',minValue=-1.0, maxValue=1.0, defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Twist_Heel_'+side, attributeType='float',minValue=-1.0, maxValue=1.0, defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Twist_Toe_'+side, attributeType='float',minValue=-1.0, maxValue=1.0, defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Flex_Toe_'+side, attributeType='float',minValue=-1.0, maxValue=1.0, defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Bank_'+side, attributeType='float',minValue=-30.0, maxValue=30.0, defaultValue=0,keyable=True)

    #cmds.addAttr(ctrlName, longName='_', attributeType='enum', enumName='____', defaultValue=0,keyable=True,niceName="___")    
    #cmds.addAttr(ctrlName, longName='Stretch_Leg', attributeType='bool', defaultValue=0,keyable=True)
    #cmds.addAttr(ctrlName, longName='_____', attributeType='enum', enumName='____', defaultValue=0,keyable=True,niceName="___")

