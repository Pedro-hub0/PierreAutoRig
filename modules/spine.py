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
    sz=smallUsefulFct.GetDistLocScale(sz)
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
    for i in range(1,nbFkJnt):
        TranslateCtrl=cmds.xform(FkJnts[i], query=True, translation=True, worldSpace=True)
        Ctrl_Fk_Spine.append(cmds.circle(name=f'Ctrl_{FkJnts[i]}',nr=[0,1,0],radius=sz)[0])                 
        #Transform Ik Ctrl_Fk_Spine to Jnt Fk Wrist
        cmds.xform(Ctrl_Fk_Spine[i-1], translation=TranslateCtrl, worldSpace=True)  
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


