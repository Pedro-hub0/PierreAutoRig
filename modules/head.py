import maya.cmds as cmds
import smallUsefulFct
import math
import os
import importlib
importlib.reload(smallUsefulFct)

locator_names = ["Loc_Eyelid_Down_L","Loc_Eyelid_Up_L","Loc_Eye_L","Loc_Jaw_Up_End","Loc_Teeth_Up","Loc_Jaw_Up_01","Loc_Jaw_down_End","Loc_Teeth_Down","Loc_Jaw_Down_01","Loc_Head_Pivot_02","Loc_Head_Pivot_01","Eye_End_L"]
joints_names = ["Bind_Eyelid_Dwn_End_L","Bind_Eyelid_Up_End_L","Bind_Eye_L","Bind_Jaw_Up_End","Bind_Teeth_Up","Bind_Jaw_Up_01","Bind_Jaw_Down_End","Bind_Teeth_Down","Bind_Jaw_Down_01","Bind_Head_Pivot_02","Bind_Head_Pivot_01","Bind_Eye_End_L"]



def CreatelocHeadStructure(cb_org):
    tr_Neck=(0,0,0)
    if cb_org!=True:
        cb_org=cmds.checkBox(cb_org, query=True, value=True)
        tr_Neck=cmds.xform('Bind_Neck_end', q=True, t=True, ws=True)

    for loc in locator_names:
        cmds.spaceLocator(name=loc)[0]
    
    if cb_org:
        #Organisation
        #In Eye Joint
        cmds.parent(locator_names[0],locator_names[2])
        cmds.parent(locator_names[1],locator_names[2])
        cmds.parent(locator_names[11],locator_names[2])
        #In Jaw Up Joint
        cmds.parent(locator_names[2],locator_names[5])
        cmds.parent(locator_names[3],locator_names[5])
        cmds.parent(locator_names[4],locator_names[5])
        #In Jaw Down Joint
        cmds.parent(locator_names[6],locator_names[8])
        cmds.parent(locator_names[7],locator_names[8])
        #In Jaw Head Pivot 02 Joint
        cmds.parent(locator_names[8],locator_names[9])
        #In Jaw Head Pivot 01 Joint
        cmds.parent(locator_names[5],locator_names[10])
        cmds.parent(locator_names[9],locator_names[10])
        if cmds.objExists('Grp_temp_Locs'):   
            tr_Neck=cmds.xform(locator_names[10], t=tr_Neck, ws=True)
            cmds.parent(locator_names[10],'Grp_temp_Locs')
    
def HeadStructure():
    ##Initialisation##
    Eyes=[]
    #Creation
    for i in range(len(joints_names)):
        tr_Loc=cmds.xform(locator_names[i], query=True, translation=True, worldSpace=True)
        cmds.select(clear=True)
        cmds.joint(n=f'{joints_names[i]}',p=tr_Loc)
    

    cmds.select(clear=True)
    Eyes.append(cmds.duplicate(joints_names[2],returnRootsOnly=True)[0])
    Eyes[0]=cmds.rename(Eyes[0],"Bind_Eyelid_Dwn_L")
    cmds.select(clear=True)
    Eyes.append(cmds.duplicate(joints_names[2],returnRootsOnly=True)[0])
    Eyes[1]=cmds.rename(Eyes[1],"Bind_Eyelid_Up_L")
               
    ##Organisation##
    #In Eye Joint
    cmds.parent(joints_names[11],joints_names[2])
    #In Eyelid Up and Down Joint
    cmds.parent(joints_names[0],Eyes[0])
    cmds.parent(joints_names[1],Eyes[1])
    #In Jaw Up Joint
    cmds.parent(joints_names[2],joints_names[5])
    cmds.parent(joints_names[3],joints_names[5])
    cmds.parent(joints_names[4],joints_names[5])
    cmds.parent(Eyes[0],joints_names[5])
    cmds.parent(Eyes[1],joints_names[5])
    #In Jaw Down Joint
    cmds.parent(joints_names[6],joints_names[8])
    cmds.parent(joints_names[7],joints_names[8])
    #In Jaw Head Pivot 02 Joint
    cmds.parent(joints_names[5],joints_names[9])
    cmds.parent(joints_names[8],joints_names[9])
    #In Jaw Head Pivot 01 Joint
    cmds.parent(joints_names[9],joints_names[10])

    # mirror Eyes
    jnt_eye_R = cmds.mirrorJoint(joints_names[2], mirrorYZ=True, mirrorBehavior=True, searchReplace=["_L", "_R"])
    jnt_eyelid_Up_R = cmds.mirrorJoint(Eyes[0], mirrorYZ=True, mirrorBehavior=True, searchReplace=["_L", "_R"])
    jnt_eyelid_dwn_R = cmds.mirrorJoint(Eyes[1], mirrorYZ=True, mirrorBehavior=True, searchReplace=["_L", "_R"])

    ##Orientation##
    #joint -e  -oj xyz -secondaryAxisOrient yup -ch -zso;
    jntsHierarchy = cmds.listRelatives(joints_names[10], allDescendents=True)
    cmds.joint(joints_names[10], e=True, oj='xyz', sao='yup', ch=True, zso=True)  
    for j in  jntsHierarchy:
        ischild = cmds.listRelatives(j, children=True)
        if ischild == None:
            cmds.joint(j, e=True, oj='none', ch=True, zso=True)



    ##Move##
    offset_jnt_hdpiv01=smallUsefulFct.move2(joints_names[10])
    offset_EyelidDwn=smallUsefulFct.hook2(Eyes[0])
    offset_EyelidUp=smallUsefulFct.hook2(Eyes[1])
    offset_EyelidUp=smallUsefulFct.hook2(jnt_eyelid_Up_R[0])
    offset_EyelidUp=smallUsefulFct.hook2(jnt_eyelid_dwn_R[0])

    lastNeckJnt=lastNeck()
    cmds.parentConstraint(f'{lastNeckJnt}',offset_jnt_hdpiv01, maintainOffset=True, weight=1)
    cmds.parent(offset_jnt_hdpiv01,'JNT')
def lastSpine():

        SpineChain = cmds.listRelatives('Bind_Root', allDescendents=True, type='joint') or []
        LastSpine='Bind_Spine_01'
        for n in SpineChain:
            if 'Spine' in n:
                LastSpine=n
                break
        return LastSpine

def lastNeck():

        NeckChain = cmds.listRelatives('Bind_Neck_00', allDescendents=True, type='joint') or []
        LastNeck='Bind_Neck_01'
        for n in NeckChain:
            if 'Neck' in n:
                LastNeck=n
                break
        return LastNeck

def CtrlHeadStructure(sz):

    ##Initialisation
    CTRLS_hierarchy = ["CTRL_Head_01","Master_Head_01","CTRL_Head_02","Master_Head_02","CTRL_Skull","Master_Skull"]
    jntConstraint=["Bind_Head_Pivot_01","Bind_Head_Pivot_02","Bind_Jaw_Up_01"]
    CTRL_names_Eyes=["CTRL_Eyelid_Down_L","CTRL_Eyelid_Up_L","CTRL_Eye_L","CTRL_Eyelid_Down_R","CTRL_Eyelid_Up_R","CTRL_Eye_R"]
    jnt_Eyes_names = ["Bind_Eyelid_Dwn_End_L","Bind_Eyelid_Up_End_L","Bind_Eye_L","Bind_Eyelid_Dwn_End_R","Bind_Eyelid_Up_End_R","Bind_Eye_R"]
    jnt_Eyes_names2 = ["Bind_Eyelid_Dwn_L","Bind_Eyelid_Up_L","Bind_Eye_L","Bind_Eyelid_Dwn_R","Bind_Eyelid_Up_R","Bind_Eye_R"]

    tr_Head01=cmds.xform('Bind_Head_Pivot_01', query=True, translation=True, worldSpace=True)
    tr_Head02=cmds.xform('Bind_Head_Pivot_02', query=True, translation=True, worldSpace=True)
    size=smallUsefulFct.GetDistLocScale(sz)
    
    ##Creation
    for obj in CTRLS_hierarchy:
        if obj.split('_')[0] == "CTRL":
            cmds.circle(name=obj,radius=size,nr=[0,1,0])
        else:
            cmds.select(clear=True)  
            cmds.group(empty=True,name=obj)
        if obj[-1]=='2':
            cmds.xform(obj, translation=tr_Head02, worldSpace=True)
        else:
            cmds.xform(obj, translation=tr_Head01, worldSpace=True)

    for obj in CTRL_names_Eyes:
        cmds.circle(name=obj,radius=size/2,nr=[0,0,0])
    
    for i in range(len(jnt_Eyes_names)):
        tr=cmds.xform(jnt_Eyes_names[i], query=True, translation=True, worldSpace=True)
        if CTRL_names_Eyes[i].split("_")[1]==f"Eye":
            pos=[tr[0],tr[1],tr[2]+(size*2)]
        else:
            pos=[tr[0],tr[1],tr[2]+(size/2)]
        cmds.xform(CTRL_names_Eyes[i], translation=pos, worldSpace=True)   

    ctrl_Eyes=cmds.circle(name='CTRL_Eyes',radius=size/2,nr=[0,0,0])[0]
    cmds.xform('CTRL_Eyes', translation=smallUsefulFct.get_translate_between('CTRL_Eye_R','CTRL_Eye_L'), worldSpace=True)   
    
    ##Organisation
    for i in range(len(CTRLS_hierarchy)-1,-1,-1): 
        if i>0:
            cmds.parent(CTRLS_hierarchy[i],CTRLS_hierarchy[i-1])
    
    # Eyes
    for eye in CTRL_names_Eyes: 
        cmds.parent(eye,"Master_Skull")

    cmds.parent(ctrl_Eyes,"Master_Skull") 
    cmds.parent(CTRL_names_Eyes[2],ctrl_Eyes)
    cmds.parent(CTRL_names_Eyes[5],ctrl_Eyes)


    # Jaw
    trJawend=cmds.xform('Bind_Jaw_Down_End', query=True, translation=True, worldSpace=True)
    trJaw=cmds.xform('Bind_Jaw_Down_01', query=True, translation=True, worldSpace=True)
    JwDwnCtrl=cmds.circle(name='CTRL_Jaw_Down',radius=size/2,nr=[0,0,0])[0]
    cmds.xform(JwDwnCtrl,translation=trJawend, worldSpace=True)
    cmds.xform(JwDwnCtrl, pivots=trJaw, worldSpace=True)
    offJwDwnCtrl=smallUsefulFct.move2(JwDwnCtrl)
    cmds.parent(offJwDwnCtrl,'Master_Head_01')
    cmds.orientConstraint(JwDwnCtrl,'Bind_Jaw_Down_01', maintainOffset=True, weight=1)

    ##Offset / Erase Transform
    for eye in CTRL_names_Eyes: 
        smallUsefulFct.hook2(eye)
    
    smallUsefulFct.move2(ctrl_Eyes)
    ctrl_head_offset=smallUsefulFct.move('CTRL_Head_01')

    
    ##Constraints
    # Head
    a=1
    for i in range(len(jntConstraint)):
        cmds.orientConstraint(CTRLS_hierarchy[a],jntConstraint[i], maintainOffset=True, weight=1)
        a=a+2

    # Eyes
    for i in range(len(CTRL_names_Eyes)):

        if not CTRL_names_Eyes[i].split("_")[1]==f"Eye":
            cmds.aimConstraint(CTRL_names_Eyes[i],f'{jnt_Eyes_names2[i]}_Hook',w=1,aim=[1,0,0],u=[0,1,0],wut=2,wu=[0,1,0],wuo=CTRL_names_Eyes[i], maintainOffset=True, weight=1)
        else:
            cmds.aimConstraint(CTRL_names_Eyes[i],f'{jnt_Eyes_names2[i]}',w=1,aim=[1,0,0],u=[0,1,0],wut=2,wu=[0,1,0],wuo=CTRL_names_Eyes[i],maintainOffset=True, weight=1)
        ## Eyelide ##
    expEyelides="""    
    //Horizontal

    Bind_Eyelid_Up_L.rotateY = Bind_Eye_L.rotateY*0.3;
    Bind_Eyelid_Dwn_L.rotateY = Bind_Eye_L.rotateY*0.3;

    Bind_Eyelid_Up_R.rotateY = Bind_Eye_R.rotateY*0.3;
    Bind_Eyelid_Dwn_R.rotateY = Bind_Eye_R.rotateY*0.3;

    //Vertical


    Bind_Eyelid_Up_L.rotateX = Bind_Eye_L.rotateX*0.6;
    Bind_Eyelid_Dwn_L.rotateX = Bind_Eye_L.rotateX*0.35;

    Bind_Eyelid_Up_R.rotateX = Bind_Eye_R.rotateX*0.6;
    Bind_Eyelid_Dwn_R.rotateX = Bind_Eye_R.rotateX*0.35;"""
    

    exp_name_Eyelides = f"Exp_Eyelid"


    cmds.expression(name=exp_name_Eyelides, string=expEyelides)

    
    cmds.parent(ctrl_head_offset,'CTRL_Torso')
    
def LocNeck():
    loc=cmds.spaceLocator(n=f'Loc_Neck_Base')[0]
    loc2=cmds.spaceLocator(n=f'Loc_Neck_End')[0]
    cmds.parent(loc2,loc)




        ##########
        ## NECK ##
        ##########



def createNeckAlt(neckIk,sz) :
    nbIkJnt=cmds.intField(neckIk, query=True, value=True)+1
    sz=smallUsefulFct.GetDistLocScale(sz)
    LocName=['Loc_Neck_Base','Loc_Neck_End']
    IkJnts=[]
    Ctrl_Fk_Neck=[]
    cmds.select(clear=True)
    if not cmds.objExists('Loc_Neck_End') or not cmds.objExists('Loc_Neck_Base'):
        raise ValueError("Create Locators")

    TranslateJnts = [cmds.xform(LocName[0], q=True, t=True, ws=True),cmds.xform(LocName[1], q=True, t=True, ws=True)]
    i=0
    while i<=nbIkJnt :
        if i==nbIkJnt:
            name=f'Bind_Neck_end'
        else:
            name=f'Bind_Neck_0{i}'

        JntTranslate=[((TranslateJnts[1][0]-TranslateJnts[0][0])/nbIkJnt)*i +TranslateJnts[0][0],((TranslateJnts[1][1]-TranslateJnts[0][1])/nbIkJnt)*i +TranslateJnts[0][1],((TranslateJnts[1][2]-TranslateJnts[0][2])/nbIkJnt)*i +TranslateJnts[0][2]]
        IkJnts.append(cmds.joint(position=JntTranslate, name=f'{name}'))
        i+=1
    
    
    #Orient 
        #Ik
    cmds.joint(IkJnts[0],e=True, oj='xyz', sao='yup', ch=True, zso=True)
    cmds.joint(IkJnts[len(IkJnts)-1], e=True, oj='none', ch=True, zso=True)
    cmds.parent(IkJnts[0],'JNT')
    offJnts=smallUsefulFct.move2(IkJnts[0])
     #Create Controllers      
        #Fk
    for i in range(1,nbIkJnt):
        TranslateCtrl=cmds.xform(IkJnts[i], query=True, translation=True, worldSpace=True)
        Ctrl_Fk_Neck.append(cmds.circle(name=f'Ctrl_{IkJnts[i]}',nr=[0,1,0],radius=sz)[0])                 
        #Transform Ik Ctrl_Fk_Neck to Jnt Fk Wrist
        cmds.xform(Ctrl_Fk_Neck[i-1], translation=TranslateCtrl, worldSpace=True)
        rot=cmds.getAttr(f'{Ctrl_Fk_Neck[i-1]}.rotateX')
        smallUsefulFct.set_curve_color(Ctrl_Fk_Neck[i-1],15)
        smallUsefulFct.move2(Ctrl_Fk_Neck[i-1])
        print(f'{Ctrl_Fk_Neck[i-1]}_Move {IkJnts[i-1]}',)
        cmds.parentConstraint(f'{Ctrl_Fk_Neck[i-1]}',f'{IkJnts[i]}', maintainOffset=True, weight=1)

        if i>1:
            cmds.parent(f'{Ctrl_Fk_Neck[i-1]}_Offset',Ctrl_Fk_Neck[i-2])
   
    lastSpineJnt=lastSpine()
    if cmds.objExists(f'{Ctrl_Fk_Neck[0]}_Offset'):
        cmds.parent(f'{Ctrl_Fk_Neck[0]}_Offset','CTRL')
    
    ##CONSTRAINTS Folder neck
    cmds.parentConstraint('CTRL_Torso',f'{Ctrl_Fk_Neck[0]}_Offset',maintainOffset=True, weight=1)
    cmds.parentConstraint(lastSpineJnt,f'Bind_Neck_00_Offset',maintainOffset=True, weight=1)

## NECK Ik Fk

###################################
###        Create Neck        ####
###################################    

def createNeck(neckIk,neckFk,sz):
    nbIkJnt=cmds.intField(neckIk, query=True, value=True)
    nbFkJnt=cmds.intField(neckFk, query=True, value=True)
    sz=smallUsefulFct.GetDistLocScale()
    LocName=['Loc_Neck_Base','Loc_Neck_End']
    JntName=['Jnt_Neck_Root','Jnt_Neck_End']
    IkJnts=[]
    FkJnts=[]
    Ctrl_Fk_Neck=[]
    Ctrl_Ik_Neck=[]
    grp_Extranode=""
    #Organiser
    smallUsefulFct.organiser()
    grp_Ctrl="CTRL"
    grp_Jnt="JNT"
    grp_Global='GlobalMove'
    grp_Iks='IKs'
    grp_Extranode="ExtraNodes"
    if not cmds.objExists('Loc_Neck_End') or not cmds.objExists('Loc_Neck_Base'):
        raise ValueError("Create Locators")

    TranslateJnts = [cmds.xform(LocName[0], q=True, t=True, ws=True),cmds.xform(LocName[1], q=True, t=True, ws=True)]
   
    #CREATE JOINT IN A LINE BETWEEN THE 2 JOINTS
    i=0
    while i<=nbIkJnt :
        if i==0:
            name=f'Bind_Root_Neck'
        else:
            name=f'Bind_Neck_0{i}'
        JntTranslate=[((TranslateJnts[1][0]-TranslateJnts[0][0])/nbIkJnt)*i +TranslateJnts[0][0],((TranslateJnts[1][1]-TranslateJnts[0][1])/nbIkJnt)*i +TranslateJnts[0][1],((TranslateJnts[1][2]-TranslateJnts[0][2])/nbIkJnt)*i +TranslateJnts[0][2]]
        IkJnts.append(cmds.joint(position=JntTranslate, name=f'{name}'))
        i+=1

    i=0
    while i<=nbFkJnt :
        if i==0:
            name=f'Fk_Root_Neck'
        else:
            name=f'Fk_Neck_0{i}'
        JntTranslate=[((TranslateJnts[1][0]-TranslateJnts[0][0])/nbFkJnt)*i +TranslateJnts[0][0],((TranslateJnts[1][1]-TranslateJnts[0][1])/nbFkJnt)*i +TranslateJnts[0][1],((TranslateJnts[1][2]-TranslateJnts[0][2])/nbFkJnt)*i +TranslateJnts[0][2]]
        FkJnts.append(cmds.joint(position=JntTranslate, name=f'{name}'))

        if i==0 :
            p=cmds.parent(f'Fk_Root_Neck', world=True)
            if p==True:
                cmds.parent(f'Fk_Root_Neck', world=True)
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
    ik_objs = cmds.ikHandle(sj=IkJnts[0], ee=IkJnts[len(IkJnts)-1], sol='ikSplineSolver', ccv=True, scv=True,pcv=True,name="Ik_Neck")
    ik_Handle=ik_objs[0]
    CurveIk=ik_objs[len(ik_objs)-1]
    cmds.rename(CurveIk,"Crv_Neck")
    CurveIk="Crv_Neck"
    cmds.parent(CurveIk,grp_Extranode)

    ##Corriger Bas curve ne rotate pas, Twist
    SkinClusterNeck = cmds.skinCluster(JntName, CurveIk, n='Neck_skinCluster', tsb=True, bm=0, sm=0, nw=1,mi=3)[0]
    cmds.setAttr(f'{ik_Handle}.Root_NeckTwistMode', 1)
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
    Ctrl_Ik_Neck.append(smallUsefulFct.controller(1,JntName[0],"CTRL_Root",sz))
    Ctrl_Ik_Neck.append(smallUsefulFct.controller(1,JntName[1],"CTRL_Torso",sz))
    smallUsefulFct.set_curve_color(Ctrl_Ik_Neck[0],colorIk)
    smallUsefulFct.set_curve_color(Ctrl_Ik_Neck[1],colorIk)
    smallUsefulFct.move(Ctrl_Ik_Neck[0]) 
    smallUsefulFct.move(Ctrl_Ik_Neck[1])        
        #Fk
    for i in range(1,nbFkJnt+1):
        TranslateCtrl=cmds.xform(FkJnts[i], query=True, translation=True, worldSpace=True)
        RotationCtrl=cmds.xform(FkJnts[i], query=True, translation=True, worldSpace=True)

        Ctrl_Fk_Neck.append(cmds.circle(name=f'Ctrl_{FkJnts[i]}',nr=[0,0,1],radius=sz)[0])                 
        #Transform Ik Ctrl_Fk_Neck to Jnt Fk Wrist
        cmds.xform(Ctrl_Fk_Neck[i-1], translation=TranslateCtrl, worldSpace=True)  
        rot=cmds.getAttr(f'{Ctrl_Fk_Neck[i-1]}.rotateX')
        cmds.setAttr(f'{Ctrl_Fk_Neck[i-1]}.rotateX',rot+90)
        smallUsefulFct.set_curve_color(Ctrl_Fk_Neck[i-1],15)
        smallUsefulFct.move(Ctrl_Fk_Neck[i-1])
        if i>1:
            cmds.parent(f'{Ctrl_Fk_Neck[i-1]}_Offset',Ctrl_Fk_Neck[i-2])
   

    #Constraints 
        #Root to Fk root/Ik/ Shoulder to Ik/ 
    cmds.parentConstraint(f'{Ctrl_Ik_Neck[0]}',f'{JntName[0]}_Move', maintainOffset=True, weight=1)
    cmds.parentConstraint(f'{Ctrl_Ik_Neck[0]}',f'{FkJnts[0]}_Move', maintainOffset=True, weight=1)
    cmds.parentConstraint(f'{Ctrl_Ik_Neck[0]}',f'{Ctrl_Fk_Neck[0]}_Move', maintainOffset=True, weight=1)
    cmds.parentConstraint(f'{Ctrl_Ik_Neck[1]}',f'{JntName[1]}_Move', maintainOffset=True, weight=1)
    cmds.parentConstraint(f'{Ctrl_Fk_Neck[len(Ctrl_Fk_Neck)-1]}',f'{Ctrl_Ik_Neck[1]}_Move', maintainOffset=True, weight=1)
        #Fk
    i=1
    while i<nbFkJnt :
        cmds.parentConstraint(f'{Ctrl_Fk_Neck[i-1]}',f'{FkJnts[i]}', maintainOffset=True, weight=1)
        i+=1

    #Organiser

    grp_Ctrl_Neck=cmds.group(empty=True, name="Grp_CTRL_Neck")
    cmds.parent(f'{Ctrl_Ik_Neck[0]}_Offset',grp_Ctrl_Neck)
    cmds.parent(f'{Ctrl_Ik_Neck[1]}_Offset',grp_Ctrl_Neck)
    cmds.parent(f'{Ctrl_Fk_Neck[0]}_Offset',grp_Ctrl_Neck)
    cmds.parent(grp_Ctrl_Neck,grp_Ctrl)

    grp_Jnt_Neck=cmds.group(empty=True, name="Grp_Jnt_Neck")
    cmds.parent(f'{FkJnts[0]}_Offset',grp_Jnt_Neck)
    cmds.parent(f'{IkJnts[0]}_Offset',grp_Jnt_Neck)
    cmds.parent(f'{JntName[0]}_Offset',grp_Jnt_Neck)
    cmds.parent(f'{JntName[1]}_Offset',grp_Jnt_Neck)
    cmds.parent(grp_Jnt_Neck,grp_Jnt)   
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
    if side == "Root" :
        Ik_jnt_Names = cmds.listRelatives("Bind_Root_Move", ad=True, fullPath=False, type="joint") or []
    
    else :
        raise ValueError("You need to select somethind that's end up by Arm_L or Leg_R for example ")
    



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
        distance_node = cmds.createNode('curveInfo', name=f'curveInfo_Neck')


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
        cmds.connectAttr(f'Crv_NeckShape.worldSpace', f'{distance_node}.inputCurve')
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
        if not cmds.objExists(f'CTRL_Root.Stretch_Neck'): 
            cmds.addAttr(f'CTRL_Root', longName=f'Stretch_Neck', attributeType='bool', defaultValue=0,keyable=True)
        cmds.connectAttr(f'CTRL_Root.Stretch_Neck', f'{cond_Stretch}.firstTerm')

    ##Tout CONNECTER AUX JOINTS 
    for ik in Ik_jnt_Names:
        cmds.connectAttr(f'{cond_Stretch}.outColorR',f'{ik}.scaleX')
        cmds.connectAttr(f'{cond_Stretch}.outColorG',f'{ik}.scaleY')
        cmds.connectAttr(f'{cond_Stretch}.outColorG',f'{ik}.scaleZ')