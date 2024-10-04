import maya.cmds as cmds
import sys
import os
import smallUsefulFct
import importlib
importlib.reload(smallUsefulFct)

def create_hips():
    ##Initialisation##
    jnt_Names = ['Bind_Hip','Bind_Leg_L','Bind_Leg_R']
    target_jnt_Names = ['Bind_Root','DrvJnt_Leg_L','DrvJnt_Leg_R']
    Ctrl_Fk=['CTRL_Fk_Leg_L_Move','CTRL_Fk_Leg_R_Move']

    # Create a new joint
    for jnt_n in jnt_Names:
        cmds.select(clear=True)
        jnt_hips = cmds.joint(n=jnt_n)

    ##Move Jnt 
    for i in range(len(target_jnt_Names)):
        target_translation = cmds.xform(target_jnt_Names[i], query=True, worldSpace=True, translation=True)
        cmds.xform(jnt_Names[i], worldSpace=True, translation=target_translation)

    ##Parent Joint
    cmds.parent(jnt_Names[0],target_jnt_Names[0])
    for i in range(len(jnt_Names)-1):
        cmds.parent(jnt_Names[i+1],jnt_Names[0])

    ##Constraint Parent Joint
    for i in range(len(jnt_Names)-1):
        cmds.parentConstraint(jnt_Names[i+1],f'{target_jnt_Names[i+1]}_Move', maintainOffset=True, weight=1)
        cmds.parentConstraint(jnt_Names[i+1],Ctrl_Fk[i], maintainOffset=True, weight=1)
    
def create_hips_Ctrl(size):
    if cmds.objExists('Bind_Hip'):
        size=cmds.intField(size, query=True, value=True)
        ##Create Controller 
        Ctrl_hip=cmds.circle(name=f'CTRL_Hips',radius=size,nr=[0,1,0])[0]
        target_translation = cmds.xform('Bind_Root', query=True, worldSpace=True, translation=True)
        cmds.xform(Ctrl_hip, worldSpace=True, translation=target_translation)
        smallUsefulFct.move(Ctrl_hip)

        if cmds.objExists('CTRL'):
            cmds.parent(f'{Ctrl_hip}_Offset','CTRL')
        
        #parent 
        cmds.parentConstraint(Ctrl_hip,'Bind_Hip', maintainOffset=True, weight=1)
    else:
        raise ValueError("You need to create Hips Before")





