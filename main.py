
import maya.cmds as cmds
import sys
import os
import importlib

# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)

import modules.armLeg, modules.clavicule, modules.foot, modules.spine, modules.tools, modules.stretch,modules.hips,modules.ribbon,modules.globalscale,modules.head

importlib.reload(modules.armLeg)
importlib.reload(modules.clavicule)
importlib.reload(modules.foot)
importlib.reload(modules.spine)
importlib.reload(modules.tools)
importlib.reload(modules.stretch)
importlib.reload(modules.hips)
importlib.reload(modules.ribbon)
importlib.reload(modules.globalscale)
importlib.reload(modules.head)


from modules import *


"""Script created by Pierre LIPPENS """

def create_window():
    """
    Create a window with a button.
    """
    # Check if the window already exists, and delete it if it does
    if cmds.window("myWindow", exists=True):
        cmds.deleteUI("myWindow", window=True)

    # Create the window
    window_name = cmds.window("myWindow", title="PierreAutoRig01", widthHeight=(310, 500), sizeable=False)
    scroll_layout = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    # Create a layout for the window
    column_layout= cmds.columnLayout(adjustableColumn=True)
    # Create a text field for user input of the name of the ik fk variable
    cmds.separator(h=15)
    cmds.text(label="AUTO RIG", font = "boldLabelFont" , w = 200, align = "center")
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cmds.text(label="CTRL Size", font = "boldLabelFont" , w = 150, align = "center")
    sizeCtrlArm = cmds.intField(value=2,width=150,ann="Size")
    cmds.setParent('..')
    cmds.separator(h=8)
    cmds.button(label='Squash And Stretch', command=lambda x:stretch.Stretchfct(),width=120)
    cmds.separator(h=8)
    # Crée une frame layout (volet repliable)
    cmds.frameLayout(label='Spine', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[75,75,75,75])
    cmds.text(label="Ik", font = "boldLabelFont" , w = 75, align = "center")
    spineIk = cmds.intField(value=6,width=75)
    cmds.text(label="Fk", font = "boldLabelFont" , w = 75, align = "center")
    spineFk = cmds.intField(value=3,width=75)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cmds.button(label='Create Locs', command=lambda x:spine.creatLocsSpine(),width=150)
    cmds.button(label='Spine', command=lambda x:spine.createSpine(spineIk,spineFk,sizeCtrlArm),width=150)
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(label='Arm/Leg', collapsable=True, collapse=True)
    cmds.separator(h=3)
    cmds.text(label="Create 3 Joint for your Arm / Leg", font = "boldLabelFont" , w = 50, align = "left")
    cmds.text(label="Select Joint Parent : Name Arm/Leg_L/R", font = "boldLabelFont" , w = 50, align = "left")
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100,100,100])
    cmds.button(label='Freeze And Orient', command=lambda x:armLeg.createLegArmLocs(),width=100)
    cmds.button(label='Ik_Fk_Arm/Leg', command=lambda x:armLeg.createIkFk(sizeCtrlArm),width=100)
    cmds.button(label='Mirror', command=lambda x:armLeg.mirror(sizeCtrlArm),width=100)
    cmds.setParent('..') 
    cmds.separator(h=15)
    cmds.setParent('..')

    cmds.frameLayout(label='Clavicle', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cmds.button(label='Create Loc', command=lambda x:clavicule.locClavicule(),width=100)
    cmds.button(label='Create Clavicle', command=lambda x:clavicule.createClavicule(),width=100)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cb_jnt_clav= cmds.checkBox(label="Create",v=True)
    cmds.button(label='Mirror', command=lambda x:clavicule.mirorClav(cb_jnt_clav),width=100)
    cmds.setParent('..')
    cmds.setParent('..')


    cmds.frameLayout(label='Foot', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.text(label="Creates locs Then place it", font = "boldLabelFont" , w = 50, align = "left")
    cmds.separator(h=3)
    cmds.rowLayout(numberOfColumns=3, columnWidth2=[100, 100])
    cmds.button(label=' Creates Locs', command=lambda x:foot.createLocs(),width=100)
    cmds.button(label=' Organise Locs', command=lambda x:foot.OrganiseLocs(sizeCtrlArm),width=100)
    cmds.button(label='  Nodale', command=lambda x:foot.ConnectFoot(),width=100)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[75,75,150])
    cb_jnt_hand= cmds.checkBox(label="Organise")
    cb_ctrl_hand = cmds.checkBox(label="Nodale")
    cmds.button(label='Mirror', command=lambda x:foot.mirorFoot(cb_jnt_hand,cb_ctrl_hand,sizeCtrlArm),width=100)
    cmds.setParent('..')    
    cmds.separator(h=8)
    cmds.setParent('..')


    cmds.frameLayout(label='Hand', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100,100,100])
    cmds.button(label='Create Locators', command=lambda x:hand.locHand(),width=100)
    cmds.button(label='Create Hand', command=lambda x:hand.createHand(),width=100)
    cmds.button(label='Create Controllers', command=lambda x: hand.ctrlHand(sizeCtrlArm),width=100)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[75,75,150])
    cb_jnt_foot = cmds.checkBox(label="Joints")
    cb_ctrl_foot = cmds.checkBox(label="Ctrl")
    cmds.button(label='Mirror', command=lambda x:hand.mirorHand(cb_jnt_foot,cb_ctrl_foot,sizeCtrlArm),width=100)
    cmds.setParent('..')
    cmds.separator(h=8)
    cmds.setParent('..')



    cmds.frameLayout(label='Hips', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cmds.button(label='Create Hips', command=lambda x:hips.create_hips(),width=100)
    cmds.button(label='Create CTRL Hips', command=lambda x:hips.create_hips_Ctrl(sizeCtrlArm),width=100)
    cmds.setParent('..')
    cmds.setParent('..')


    cmds.frameLayout(label='Attach Ribbon', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.button(label='Create Ribbon', command=lambda x:ribbon.createRibbon(),width=100)
    cmds.separator(h=4)
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100,100,100])
    cmds.text(label="Shoulder", font = "boldLabelFont" , w = 75, align = "center")
    cb_attach_shoulder_L= cmds.checkBox(label="L",v=True)
    cb_attach_shoulder_R = cmds.checkBox(label="R",v=False)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100,100,100])
    cmds.text(label="Elbow", font = "boldLabelFont" , w = 75, align = "center")
    cb_attach_elbow_L= cmds.checkBox(label="L",v=False)
    cb_attach_elbow_R = cmds.checkBox(label="R",v=False)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100,100,100])
    cmds.text(label="Leg", font = "boldLabelFont" , w = 75, align = "center")
    cb_attach_Leg_L = cmds.checkBox(label="L",v=False)
    cb_attach_Leg_R= cmds.checkBox(label="R",v=False)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100,100,100])
    cmds.text(label="Knee", font = "boldLabelFont" , w = 75, align = "center")
    cb_attach_Knee_L = cmds.checkBox(label="L",v=False)
    cb_attach_Knee_R= cmds.checkBox(label="R",v=False)
    cmds.setParent('..')

    cb_attach=[cb_attach_shoulder_L,cb_attach_shoulder_R,cb_attach_elbow_L,cb_attach_elbow_R,cb_attach_Leg_L,cb_attach_Leg_R,cb_attach_Knee_L,cb_attach_Knee_R]
    cmds.button(label='Attach', command=lambda x:ribbon.AttachRib(cb_attach),width=100)

    cmds.setParent('..')

    cmds.frameLayout(label='Ctrl General Scale', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.button(label='Create Ctrl Global', command=lambda x:globalscale.CreateGlobal(sizeCtrlArm),width=100)
    cmds.setParent('..')
    cmds.separator(h=4)

    cmds.frameLayout(label='Head', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cb_orga_locs_head= cmds.checkBox(label="Orga",v=False, w = 150)
    cmds.button(label='Head Structure Locs',  w = 150,command=lambda x:head.CreatelocHeadStructure(cb_orga_locs_head),width=100)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cmds.button(label='Create Joints', command=lambda x:head.HeadStructure(),width=100)
    cmds.button(label='Create CTRL', command=lambda x:head.CtrlHeadStructure(sizeCtrlArm),width=100)
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.separator(h=8)
    cmds.setParent('..')


    cmds.separator(h=8)
    cmds.text(label="TOOLS", font = "boldLabelFont" , w = 300, align = "center")
    cmds.separator(h=8)

    cmds.frameLayout(label='Lock Attribute',w = 300, collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[75,75,75,75])
    cb_loc_Translate= cmds.checkBox(label="Translate",v=True)
    cb_loc_tx = cmds.checkBox(label="X",v=True)
    cb_loc_ty = cmds.checkBox(label="Y",v=True)
    cb_loc_tz= cmds.checkBox(label="Z",v=True)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[75,75,75,75])
    cb_loc_Rotate= cmds.checkBox(label="Rotate",v=True)
    cb_loc_rx = cmds.checkBox(label="X",v=True)
    cb_loc_ry = cmds.checkBox(label="Y",v=True)
    cb_loc_rz= cmds.checkBox(label="Z",v=True)
    cmds.setParent('..')
    cmds.button(label='Lock/Unlock Translate', command=lambda x:tools.lockUnlock(cb_loc_Translate,cb_loc_tx,cb_loc_ty,cb_loc_tz,cb_loc_Rotate,cb_loc_rx,cb_loc_ry,cb_loc_rz),width=100)

    cmds.setParent('..')
    cmds.button(label='Replace Ctrl', command=lambda x:tools.parentshape(),width=300)
    cmds.button(label='Select Bind', command=lambda x:tools.selectJnt("Bind"),width=300)

    cmds.text(label=" Match Ik/Fk ", font = "boldLabelFont" , w = 300, align = "left")
    cmds.separator(h=5)
    # Create a text field
    txt_mamespace = cmds.textField(placeholderText="Namespace")
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[150, 75,75])
    cmds.button(label='Match Auto', command=lambda x:tools.matchIkFk(2,txt_mamespace),width=150)
    cmds.button(label='Fk/Ik', command=lambda x:tools.matchIkFk(0,txt_mamespace),width=75)
    cmds.button(label='Ik/Fk', command=lambda x:tools.matchIkFk(1,txt_mamespace),width=75)
    # Show the window
    cmds.showWindow(window_name)
