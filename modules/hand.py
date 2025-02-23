import maya.cmds as cmds
import smallUsefulFct
import math
import importlib
importlib.reload(smallUsefulFct)


####################
###     HAND   ####
####################
def locHand(sz):
    selObj = cmds.ls(selection=True)
    size=smallUsefulFct.GetDistLocScale(sz)/2
    if len(selObj) <1:
        raise ValueError("You need to select something which finish by L or R ")
    side=selObj[0][-1]
    Fingers=["thumb","index","middle","ring","pinky"]
    posHand= (0,0,0)
    ##Find the last joint in the arm (Xhere the Hand is)
    obj=f"Arm_{side}"     
    lastJoint=lastObj(obj)
    if cmds.objExists(lastJoint):
        posHand= cmds.xform(lastJoint, query=True, translation=True, worldSpace=True)

    locHand=cmds.spaceLocator(n=f'Loc_Hand_{side}')
    cmds.xform(locHand, translation=posHand, worldSpace=True) 

 
    y=0
    z=0
    for f in Fingers:
        for i in range(1,5):
            loc=cmds.spaceLocator(n=f'{f}_0{i}_{side}')
            cmds.xform(loc, translation=posHand, worldSpace=True)  
            if i==1:      
                cmds.parent(loc,locHand)
                #The thumb is slightly smaller
                y = -(size/1.5) if f == "thumb" else 0
                sizei= size*0.5
            else:
                cmds.parent(loc,f'{f}_0{i-1}_{side}')   
                sizei=size
            moveNumber=(i*sizei,y,-z*(size/2))
            smallUsefulFct.move_object(loc,moveNumber,False)
        z+=1

def createHand():
    selObj = cmds.ls(selection=True)
    if len(selObj) <1:
        raise ValueError("You need to select something which finish by L or R ")
    side=selObj[0][-1]
    cmds.select(clear=True)
    Fingers=["thumb","index","middle","ring","pinky"]

    #Create Joints
    for f in Fingers:
        cmds.select(clear=True)
        for i in range(1,5):
            pos= cmds.xform(f'{f}_0{i}_{side}', query=True, translation=True, worldSpace=True)
            cmds.joint(n=f'Bind_{f}_0{i}_{side}',p=pos)
    
    #Parent To Bind Hand And Orient
    for f in Fingers:
        cmds.parent(f'Bind_{f}_01_{side}',f'Bind_Hand_{side}')
        #Orient joint -e  -oj xyz -secondaryAxisOrient xup -ch -zso;
        if f == "thumb":
        #joint -e  -oj xyz -secondaryAxisOrient zup -ch -zso; 
            cmds.joint(f'Bind_{f}_01_{side}',e=True, oj='xyz', sao='zup', ch=True, zso=True)
        else:
            cmds.joint(f'Bind_{f}_01_{side}',e=True, oj='xyz', sao='yup', ch=True, zso=True)
        
        cmds.joint(f'Bind_{f}_04_{side}',e=True, oj='none', ch=True, zso=True)     
    #Parent Controllers
    #cmds.delete(f'Loc_Hand_{side}')
        # Check if the group exists
    if not cmds.objExists("Grp_temp_Locs") :
        cmds.group(empty=True, name="Grp_temp_Locs")
        
    if cmds.listRelatives(f'Loc_Hand_{side}', parent=True) == None:
        cmds.parent(f'Loc_Hand_{side}',"Grp_temp_Locs")


def ctrlHand(sz):
    #Create Controllers + Move
    sz=smallUsefulFct.GetDistLocScale(sz)/2
    selObj = cmds.ls(selection=True)
    if len(selObj) <1:
        raise ValueError("You need to select something which finish by L or R ")
    side=selObj[0][-1]
    Fingers=["thumb","index","middle","ring","pinky"]
    CTRL_Hand=[]
    grp_Hand=f'grp_Hand_{side}'
    
    if not cmds.objExists(f'grp_Hand_{side}'):
        grp_Hand = cmds.group(empty=True, name=f'grp_Hand_{side}')

    y=0
    for f in Fingers:
        cmds.select(clear=True)
        for i in range(1,5):
            translateJnt= cmds.xform(f'Bind_{f}_0{i}_{side}', query=True, translation=True, worldSpace=True)
            rotateJnt= cmds.xform(f'Bind_{f}_0{i}_{side}', query=True, rotation=True, worldSpace=True)
            tempCtrl=cmds.circle(name=f'CTRL_{f}_0{i}_{side}',nr=[1,0,0],radius=sz*0.5)[0]
            smallUsefulFct.set_curve_color(tempCtrl,30)
            CTRL_Hand.append(tempCtrl)    
            
            cmds.xform(CTRL_Hand[y], translation=translateJnt, ro=rotateJnt, worldSpace=True)
            smallUsefulFct.move2(CTRL_Hand[y])
            cmds.orientConstraint(CTRL_Hand[y],f'Bind_{f}_0{i}_{side}', maintainOffset=True, weight=1)
            if i>1:
                cmds.parent(f'CTRL_{f}_0{i}_{side}_Offset',f'CTRL_{f}_0{i-1}_{side}') 
            y+=1
        cmds.parent(f'CTRL_{f}_01_{side}_Offset',grp_Hand)
    cmds.parent(grp_Hand,f'CTRL')
    cmds.parentConstraint(f'Bind_Hand_{side}',grp_Hand, maintainOffset=True, weight=1)


def mirorHand2(cb_ctrl,sz):
    cb_ctrl_val=True
    if cb_ctrl!= True:
        cb_ctrl_val = cmds.checkBox(cb_ctrl, query=True, value=True)
    selObj = cmds.ls(selection=True)
    side=selObj[0][-1]
    otherside = "R" if side == "L" else "L"


    #Create mirror
    #Duplicate Hand
    tempJnt=cmds.duplicate(f'Bind_Hand_{side}', rc=True)
    #Parent to Bind_root
    cmds.parent(tempJnt[0],"Bind_Root")
    #Erase non joint things
    smallUsefulFct.delete_non_joints_in_hierarchy(tempJnt)

    #Mirror mirrorJoint -mirrorYZ -mirrorBehavior -searchReplace "_L" "_R";
    newJnts=cmds.mirrorJoint(tempJnt[0],mirrorYZ=True,mirrorBehavior=True,searchReplace=(f'_{side}', f'_{otherside}'))
    #Delete temp Fk
    cmds.delete(tempJnt[0])
    #if there isn't a Bind Hand, parent and offset the hand to sort it well
    if not cmds.objExists(f'Bind_Hand_{otherside}'):
        newHand=cmds.rename(newJnts[0],f'Bind_Hand_{otherside}')
        of_newhand=smallUsefulFct.move2(newHand)
        if cmds.objExists(f'Grp_Jnt_Arm_{otherside}'):
            cmds.parent(of_newhand,f'Grp_Jnt_Arm_{otherside}')
    
    #if Bin Hand already exist, sort everything and correct the name 
    else:
        
        children = cmds.listRelatives(newJnts[0],children=True)
        for c in children:
            cmds.parent(c,f'Bind_Hand_{otherside}')
        cmds.delete(newJnts[0])
        all_children_BH = cmds.listRelatives(f'Bind_Hand_{otherside}', allDescendents=True)
        #Erase if ther is a number at the end 
        for child in all_children_BH:
            end=child[-1]
            if cmds.objExists(child):
                if cmds.objectType(child) == "joint":
                    if end != otherside: 
                        cmds.rename(child,child[:-1])
            
    if cb_ctrl_val:
        cmds.select(f"CTRL_IkFk_Arm_{otherside}")
        ctrlHand(sz)
        cmds.select(f"CTRL_IkFk_Arm_{otherside}")
        CtrlPoses(sz)



def CtrlPoses(size):
    #Initialise
    selObj = cmds.ls(selection=True)
    side=selObj[0][-1]
    if side not in ["L","R"]: 
        raise ValueError("You need to select something which finish by L or R ")
    sz=smallUsefulFct.GetDistLocScale(size)
    Att=["Spread","Relax","Scrunch","Bend","Curl"]
    Fingers=["thumb","index","middle","ring","pinky"]
    AttCurl=['CurlThumb', 'CurlIndex','CurlMiddle','CurlRing','CurlPinky']
    axe=['x','y','z']
    valueAttribute = [
    [[0, 0, 0], [-(3/2), 0, 0], [-(1/2), 0, 0], [(1/2), 0, 0], [(3/2), 0, 0]],
    [[-(1/8), -(1/8), -(1/8)], [-(1/4), -(1/4), -(1/4)], [-(2/4), -(2/4), -(2/4)], [-(3/4), -(3/4), -(3/4)], [-1, -1, -1]],
    [[0, 0, 0], [1, (-1), (-2)], [1, (-1), (-2)], [1,( -1), (-2)], [1, (-1), (-2)]],
    [[0, 0, 0], [-1, 0, 0], [-1, 0, 0], [-1, 0, 0], [-1, 0, 0]],
    [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
    ]
    #valueAttribute=[[[0,0,0],[-(3/2),0,0],[-(1/2),0,0],[(1/2),0,0],[(3/2),0,0]]  ,  [[-1/2,-1/2,-1/2],[-(1/4),-(1/4),-(1/4)],[-(2/4),-(2/4),-(2/4)],[-(1/2),-(1/2),-(1/2)][-1,-1,-1]]    ,    [[0,0,0],[1,(-1),(-2)],[1,(-1),(-2)],[1,(-1),(-2)],[1,(-1),(-2)]]       ,     [[0,0,0],[-1,0,0],[-1,0,0],[-1,0,0],[-1,0,0]]      ,     [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]     ]
    plusMinusNode=[]

    #Create Ctrl
    CtrlPose=cmds.circle(name=f'CTRL_Poses_Finger_{side}',nr=[1,0,0],radius=sz/1.5)[0]
    smallUsefulFct.set_curve_color(CtrlPose,30)
    #Move
    tr=cmds.xform(f"Bind_Hand_{side}",translation=True,worldSpace=True ,query=True)
    cmds.xform(CtrlPose,translation=tr,worldSpace=True )
    #Put some attribute
    createAttributHand(CtrlPose)
    #Create the attributes 

    ##NODALES##
    #Link Ctrl to plus minus average
    for f in Fingers:
        # Create the plusMinusAverage node
        tempnode=cmds.createNode('plusMinusAverage', name=f'pma_{f}_{side}')
        plusMinusNode.append(tempnode)
        # Set the operation --> 1 = sum
        cmds.setAttr(f'{tempnode}.operation', 1)

    ##Connect nodes
    for iAtt in range(0,len(Att)):
        for iFing in range(0,len(Fingers)):
            for j in range(0,3):
                if valueAttribute[iAtt][iFing][j] !=0:
                    if Att[iAtt]== "Spread":
                        connections = cmds.listConnections(f'CTRL_{Fingers[iFing]}_0{j+2}_{side}_Move.rotateY' , source=True, destination=True)
                        if not connections:
                            cmds.expression(s=f'CTRL_{Fingers[iFing]}_0{j+2}_{side}_Move.rotateY = {CtrlPose}.{Att[iAtt]} * {valueAttribute[iAtt][iFing][j]}',n=f'EXPR_{CtrlPose}_{Fingers[iFing]}_{Att[iAtt]}_{side}')                    
                    else:
                        cmds.expression(s=f"{plusMinusNode[iFing]}.input3D[{iAtt}].input3D{axe[j]} = {CtrlPose}.{Att[iAtt]} * {valueAttribute[iAtt][iFing][j]}",n=f'EXPR_{CtrlPose}_{Fingers[iFing]}_{Att[iAtt]}_{side}')
                        connections = cmds.listConnections(f'CTRL_{Fingers[iFing]}_0{j+2}_{side}_Move.rotateZ', source=True, destination=True)
                        if not connections:
                            #cmds.expression(s=f"{plusMinusNode[iFing]}.input3D[{iAtt}].input3D{axe[j]} = {CtrlPose}.{Att[iAtt]} * {valueAttribute[iAtt][iFing][j]}")
                            cmds.connectAttr(f'{plusMinusNode[iFing]}.output3D.output3D{axe[j]}',f'CTRL_{Fingers[iFing]}_0{j+2}_{side}_Move.rotateZ')

    for ifing in range(0,len(Fingers)):
        for j in range(0,3):
            nbr=iAtt+ifing+1
            cmds.expression(s=f"{plusMinusNode[ifing]}.input3D[{nbr}].input3D{axe[j]} = {CtrlPose}.{AttCurl[ifing]} * (-1)",n=f'EXPR_{CtrlPose}_{Fingers[ifing]}_{AttCurl[iAtt]}_{side}')

    cmds.parent(CtrlPose,f'CTRL')
    smallUsefulFct.move2(CtrlPose)
    cmds.parentConstraint(f'Bind_Hand_{side}',f'{CtrlPose}_Move', maintainOffset=True, weight=1)



def createAttributHand(ctrlName):
    #Create attribute in the controller
    cmds.addAttr(ctrlName, longName='___', attributeType='enum', enumName='____', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Spread', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Relax', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Scrunch', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Bend', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='Curl', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='____', attributeType='enum', enumName='_____', defaultValue=0,keyable=True)    
    cmds.addAttr(ctrlName, longName='CurlThumb', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='CurlIndex', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='CurlMiddle', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='CurlRing', attributeType='float', defaultValue=0,keyable=True)
    cmds.addAttr(ctrlName, longName='CurlPinky', attributeType='float', defaultValue=0,keyable=True)

    #cmds.addAttr(ctrlName, longName='_', attributeType='enum', enumName='____', defaultValue=0,keyable=True,niceName="___")    
    #cmds.addAttr(ctrlName, longName='Stretch_Leg', attributeType='bool', defaultValue=0,keyable=True)
    #cmds.addAttr(ctrlName, longName='_____', attributeType='enum', enumName='____', defaultValue=0,keyable=True,niceName="___")


def lastObj(obj):
        if cmds.objExists(obj):
            transfChain = cmds.listRelatives(obj, allDescendents=True, type='transform') or []
            LastTransform=transfChain[0]
        return LastTransform
