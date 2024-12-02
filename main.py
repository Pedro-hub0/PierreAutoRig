
import maya.cmds as cmds
import sys
import os
import importlib

# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)

import modules.armLeg, modules.clavicule, modules.foot, modules.spine, modules.tools, modules.stretch,modules.hips,modules.ribbon,modules.globalscale,modules.head,modules.hand

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
importlib.reload(modules.hand)


from modules import *
colors = [
    ("White", (1, 1, 1)),
    ("Black", (0, 0, 0)),
    ("Red", (1, 0, 0)),
    ("Green", (0, 1, 0)),
    ("Blue", (0, 0, 1)),
    ("Yellow", (1, 1, 0)),
    ("Cyan", (0, 1, 1)),
    ("Magenta", (1, 0, 1)),
    ("Gray", (0.5, 0.5, 0.5)),
    ("Light Gray", (0.75, 0.75, 0.75)),
    ("Dark Gray", (0.25, 0.25, 0.25)),
    ("Orange", (1, 0.5, 0)),
    ("Purple", (0.5, 0, 0.5)),
    ("Pink", (1, 0.75, 0.8)),
    ("Brown", (0.6, 0.3, 0)),
    ("Olive", (0.5, 0.5, 0)),
    ("Teal", (0, 0.5, 0.5)),
    ("Navy", (0, 0, 0.5)),
    ("Light Blue", (0.5, 0.75, 1)),
    ("Lime", (0.5, 1, 0))
]

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
    sizeCtrlArm = cmds.intField(value=1,width=150,ann="Size")
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cmds.button(label='Create Locs Scale', command=lambda x:tools.LocScale(),width=150)
    cmds.button(label='Get Scale', command=lambda x:smallUsefulFct.GetDistLocScale(sizeCtrlArm),width=150)
    cmds.setParent('..')


    ########################### FULL AUTO ##############################
    cmds.separator(h=8)
    # Crée une frame layout (volet repliable)
    cmds.frameLayout(label='FULL AUTO', collapsable=True, collapse=True)
    cmds.separator(h=3)
    cmds.text(label="Place Locs and Joints", font = "boldLabelFont" , w = 50, align = "left")
    cmds.rowLayout(numberOfColumns=5, columnWidth5=[50,25,50,25,50])
    cmds.text(label="Spine", font = "boldLabelFont" , w = 50, align = "left")
    cmds.text(label="Ik", font = "boldLabelFont" , w = 50, align = "left")
    fullspineIk = cmds.intField(value=6,width=75)
    cmds.text(label="Fk", font = "boldLabelFont" , w = 50, align = "left")
    fullspineFk = cmds.intField(value=3,width=75)
    cmds.setParent('..')
    

    cmds.rowLayout(numberOfColumns=3, columnWidth3=[50,25,75])
    cmds.text(label="Neck", font = "boldLabelFont" , w = 50, align = "left")
    cmds.text(label="Fk", font = "boldLabelFont" , w = 50, align = "left")
    fullneckFk = cmds.intField(value=1,width=75)
    cmds.setParent('..')
    cb_RibbonFullAuto= cmds.checkBox(label="Ribbons Export",v=False)
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100, 100,100])
    textToe2=cmds.text(label="Toes Number", font = "boldLabelFont" , w = 50, align = "left")
    cb_ToeNumber2=cmds.intField(value=5,width=100)
    cb_Toe2=cmds.checkBox(label="Toe",changeCommand=lambda *args:update_text_field2(textToe2,cb_ToeNumber2,cb_Toe2,*args))
    cmds.setParent('..')
    cmds.text(textToe2, edit=True, enable=False)
    cmds.intField(cb_ToeNumber2,value=5, edit=True, enable=False)

    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cmds.button(label='Create Locs', command=lambda x:createLocsFulllAuto(sizeCtrlArm,cb_ToeNumber2,cb_Toe2),width=100)
    cmds.button(label='Create Skeleton', command=lambda x:createSkeleton(sizeCtrlArm,fullspineIk,fullspineFk,fullneckFk,cb_RibbonFullAuto,cb_ToeNumber2,cb_Toe2),width=100)
    cmds.setParent('..') 
    cmds.setParent('..')

    ########################### STEP BY STEP ##############################

    cmds.separator(h=5)
    cmds.frameLayout(label='Step By Step', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.button(label='Squash And Stretch', command=lambda x:stretch.Stretchfct(),width=120)
    cmds.button(label='Follows', command=lambda x:tools.CreateFollows(),width=120)

    cmds.separator(h=10)
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
    cmds.button(label='Create Joints', command=lambda x:armLeg.createJnts(sizeCtrlArm),width=100)
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100,100,100])
    cmds.button(label='Freeze And Orient', command=lambda x:armLeg.FreezeOrient(),width=100)
    cmds.button(label='Ik_Fk_Arm/Leg', command=lambda x:armLeg.createIkFk(sizeCtrlArm),width=100)
    cmds.button(label='Mirror', command=lambda x:armLeg.mirror(sizeCtrlArm),width=100)
    cmds.setParent('..') 
    cmds.separator(h=8)
    cmds.setParent('..')

    cmds.frameLayout(label='Clavicle', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cmds.button(label='Create Loc', command=lambda x:clavicule.locClavicule(),width=100)
    cmds.button(label='Create Clavicle', command=lambda x:clavicule.createClavicule(sizeCtrlArm),width=100)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cb_jnt_clav= cmds.checkBox(label="Create",v=True)
    cmds.button(label='Mirror', command=lambda x:clavicule.mirorClav(cb_jnt_clav,sizeCtrlArm),width=100)
    cmds.setParent('..')
    cmds.setParent('..')


    cmds.frameLayout(label='Foot', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.text(label="Creates locs Then place it", font = "boldLabelFont" , w = 50, align = "left")
    cmds.separator(h=3)
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100, 100,100])
    textToe=cmds.text(label="Toes Number", font = "boldLabelFont" , w = 50, align = "left")
    cb_ToeNumber=cmds.intField(value=1,width=100)
    cb_Toe=cmds.checkBox(label="Toe",changeCommand=lambda *args:update_text_field2(textToe,cb_ToeNumber,cb_Toe,*args))
    cmds.setParent('..')
    cmds.text(textToe, edit=True, enable=False)
    cmds.intField(cb_ToeNumber,value=5, edit=True, enable=False)

    cmds.rowLayout(numberOfColumns=3, columnWidth3=[80, 100,100])
    cmds.button(label=' Creates Locs', command=lambda x:foot.createLocs(cb_ToeNumber,cb_Toe),width=80)
    cmds.button(label=' Organise Locs', command=lambda x:foot.OrganiseLocs(sizeCtrlArm,cb_ToeNumber,cb_Toe),width=110)
    cmds.button(label='  Nodale', command=lambda x:foot.ConnectFoot(),width=80)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[75,75,150])
    cb_jnt_hand= cmds.checkBox(label="Organise")
    cb_ctrl_hand = cmds.checkBox(label="Nodale")
    cmds.button(label='Mirror', command=lambda x:foot.mirorFoot(cb_jnt_hand,cb_ctrl_hand,sizeCtrlArm,cb_ToeNumber,cb_Toe),width=100)
    cmds.setParent('..')    
    cmds.separator(h=8)
    cmds.setParent('..')


    cmds.frameLayout(label='Hand', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[100,100,100])
    cmds.button(label='Create Locators', command=lambda x:hand.locHand(sizeCtrlArm),width=100)
    cmds.button(label='Create Hand', command=lambda x:hand.createHand(),width=100)
    cmds.button(label='Create Controllers', command=lambda x: hand.ctrlHand(sizeCtrlArm),width=100)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cb_ctrl_foot = cmds.checkBox(label="Ctrl")
    cmds.button(label='Mirror', command=lambda x:hand.mirorHand2(cb_ctrl_foot,sizeCtrlArm),width=100)
    cmds.setParent('..')
    cmds.button(label='Hand Attribut', command=lambda x:hand.CtrlPoses(sizeCtrlArm),width=100)

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




    cmds.frameLayout(label='Neck', collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.button(label='Neck Locs',  w = 150,command=lambda x:head.LocNeck(),width=100) 
    #cmds.rowLayout(numberOfColumns=4, columnWidth4=[75,75,75,75])
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[100,100])
    #cmds.text(label="Ik", font = "boldLabelFont" , w = 75, align = "center")
    #neckIk = cmds.intField(value=6,width=75)
    cmds.text(label="Nbr Jnts", font = "boldLabelFont" , w = 75, align = "center")
    neckFk = cmds.intField(value=1,width=75)
    cmds.setParent('..')
    cmds.button(label='Neck Fk', command=lambda x:head.createNeckAlt(neckFk,sizeCtrlArm),width=100)
    #cmds.button(label='Neck Ik/Fk', command=lambda x:head.createNeck(neckIk,neckFk,sizeCtrlArm),width=100)
    cmds.setParent('..')
    
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
    cmds.setParent('..')

    cmds.separator(h=12)


    ########################### TOOLS ##############################

    cmds.setParent('..')


    cmds.separator(h=8)
    cmds.text(label="TOOLS", font = "boldLabelFont" , w = 300, align = "center")
    cmds.separator(h=8)

    cmds.frameLayout(label='CTRL On Selection',w = 300, collapsable=True, collapse=True)
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[75,75,75,75])
    cb_parent= cmds.checkBox(label="Parent",v=True)
    cb_cstr_Point = cmds.checkBox(label="Point",v=False)
    cb_cstr_Orient = cmds.checkBox(label="Orient",v=False)
    cb_cstr_Move= cmds.checkBox(label="Move",v=True)
    cmds.setParent('..')
  

    cb_cstr=[cb_parent,cb_cstr_Point,cb_cstr_Orient,cb_cstr_Move]
    cmds.button(label='Controllers On Selection', command=lambda x:tools.CtrlParentCreate(cb_cstr),width=300)
    cmds.setParent('..')
    
    
    cmds.frameLayout(label='Lock Attribute',w = 300, collapsable=True, collapse=True)
    cmds.separator(h=8)
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[75,75,75,75])
    cb_loc_Translate= cmds.checkBox(label="Translate",v=True)
    cb_loc_tx = cmds.checkBox(label="X",v=False)
    cb_loc_ty = cmds.checkBox(label="Y",v=False)
    cb_loc_tz= cmds.checkBox(label="Z",v=False)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[75,75,75,75])
    cb_loc_Rotate= cmds.checkBox(label="Rotate",v=True)
    cb_loc_rx = cmds.checkBox(label="X",v=False)
    cb_loc_ry = cmds.checkBox(label="Y",v=False)
    cb_loc_rz= cmds.checkBox(label="Z",v=False)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[75,75,75,75])
    cb_loc_Scale= cmds.checkBox(label="Scale",v=True)
    cb_loc_sx = cmds.checkBox(label="X",v=False)
    cb_loc_sy = cmds.checkBox(label="Y",v=False)
    cb_loc_sz= cmds.checkBox(label="Z",v=False)
    cmds.setParent('..')
    cb_loc_hide= cmds.checkBox(label="Hide",v=True)
    cbMove=cb_loc_Translate,cb_loc_Rotate,cb_loc_Scale
    cbaxes=[cb_loc_tx,cb_loc_ty,cb_loc_tz,
            cb_loc_rx,cb_loc_ry,cb_loc_rz,
            cb_loc_sx,cb_loc_sy,cb_loc_sz]
    cmds.button(label='Lock/Unlock Translate', command=lambda x:tools.lockUnlock(cbMove,cbaxes,cb_loc_hide),width=100)

    cmds.setParent('..')


    cmds.button(label='Replace Ctrl', command=lambda x:tools.parentshape(),width=300)
    cmds.button(label='Select Bind', command=lambda x:tools.selectJnt("Bind"),width=300)
    cmds.frameLayout(label='JOINT PATH CONSTRAINTS', collapsable=True, collapse=True,w = 300)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cnNamePath = cmds.textField(placeholderText="Name",text="Bind_Name",w=150)
    cnNumberPath = cmds.intField(value=5,width=75)
    cmds.setParent('..')    
    # Create an option menu (enum dropdown)
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150,150])
    cbObjUp=cmds.textField(placeholderText="CTRL UP",w=150,enable=False)
    enum_dropdown = cmds.optionMenu(label="World Up Type", changeCommand=lambda *args:update_text_field(enum_dropdown,cbObjUp,*args))
    cmds.menuItem(label="Scene Up")
    cmds.menuItem(label="Object Up")
    cmds.menuItem(label="Object Rotation Up")
    cmds.menuItem(label="Vector")
    cmds.menuItem(label="Normal")



    cmds.setParent('..')    

    cmds.button(label='Joint Path Constraints', command=lambda x:tools.PathJointContraint(cnNumberPath,cnNamePath,enum_dropdown,cbObjUp),width=150)

    cmds.setParent('..')
    cmds.separator(h=10)
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[50,50,50,50])
    cmds.button(label='Scale', command=lambda x:tools.Cstr("Scale"),width=50)
    cmds.button(label='Parent', command=lambda x:tools.Cstr("Parent"),width=50)
    cmds.button(label='Point', command=lambda x:tools.Cstr("Point"),width=50)
    cmds.button(label='Orient', command=lambda x:tools.Cstr("Orient"),width=50)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=2, columnWidth2=[150, 150])
    cmds.button(label=' LRA On ', command=lambda x:tools.toggleRotateVisibilityFct(True),width=150)
    cmds.button(label=' LRA Off ', command=lambda x:tools.toggleRotateVisibilityFct(False),width=150)
    cmds.setParent('..')
    cmds.text(label=" Match Ik/Fk ", font = "boldLabelFont" , w = 300, align = "left")
    cmds.separator(h=20)
    # Create a text field
    txt_mamespace = cmds.textField(placeholderText="Namespace")
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[150, 75,75])
    cmds.button(label='Match Auto', command=lambda x:tools.matchIkFk(2,txt_mamespace),width=150)
    cmds.button(label='Fk/Ik', command=lambda x:tools.matchIkFk(0,txt_mamespace),width=75)
    cmds.button(label='Ik/Fk', command=lambda x:tools.matchIkFk(1,txt_mamespace),width=75)
    # Show the window
    cmds.showWindow(window_name)


def createLocsFulllAuto(sz,cbnbToe,CbToe):
    spine.creatLocsSpine()
    armLeg.createJnts(sz)
    cmds.select("Arm_L")
    clavicule.locClavicule()
    cmds.select("Arm_L")
    hand.locHand(sz)
    cmds.select("Leg_L")
    foot.createLocs(cbnbToe,CbToe)
    head.CreatelocHeadStructure(True)
    head.LocNeck()

def createSkeleton(sz,cbIkSpine,cbFkSpine,cbFkNeck,cbRib,cbnbToe,CbToe):
    cb_Rib=cmds.checkBox(cbRib, query=True, value=True)
    #Spine
    spine.createSpine(cbIkSpine,cbFkSpine,sz)

    #Arm 
    cmds.select("Arm_L")
    armLeg.FreezeOrient()
    cmds.select("Arm_L")
    armLeg.createIkFk(sz)
    cmds.select("CTRL_IkFk_Arm_L")
    armLeg.mirror(sz)

    #Leg
    cmds.select("Leg_L")
    armLeg.FreezeOrient()
    cmds.select("Leg_L")
    armLeg.createIkFk(sz)
    cmds.select("CTRL_IkFk_Leg_L")
    armLeg.mirror(sz)

    #Stretch and Squash
    cmds.select("CTRL_IkFk_Leg_L")
    stretch.Stretchfct()
    cmds.select("CTRL_IkFk_Leg_R")
    stretch.Stretchfct()
    cmds.select("CTRL_IkFk_Arm_R")
    stretch.Stretchfct()
    cmds.select("CTRL_IkFk_Arm_L")
    stretch.Stretchfct()    
    cmds.select("CTRL_Root")
    stretch.Stretchfct()   
    
    #Clav
    cmds.select("CTRL_IkFk_Arm_L")
    clavicule.createClavicule(sz)
    cmds.select("CTRL_IkFk_Arm_L")
    clavicule.mirorClav(True,sz)
    cmds.select("CTRL_IkFk_Arm_L")

    #Hips
    cmds.select(clear=True)
    hips.create_hips()
    cmds.select(clear=True)
    hips.create_hips_Ctrl(sz)

    #Hand
    cmds.select("CTRL_IkFk_Arm_L")
    hand.createHand()
    cmds.select("CTRL_IkFk_Arm_L")
    hand.ctrlHand(sz)
    cmds.select("CTRL_IkFk_Arm_L")
    hand.CtrlPoses(sz)
    cmds.select("CTRL_IkFk_Arm_L")
    hand.mirorHand2(True,sz)
    
    #Foot 
    cmds.select("CTRL_IkFk_Leg_L")
    foot.OrganiseLocs(sz,cbnbToe,CbToe)
    cmds.select("CTRL_IkFk_Leg_L")
    foot.ConnectFoot()
    cmds.select("CTRL_IkFk_Leg_L")
    foot.mirorFoot(True,True,sz,cbnbToe,CbToe)

    #Neck 
    cmds.select(clear=True)
    head.createNeckAlt(cbFkNeck,sz)

    #Head 
    cmds.select(clear=True)
    head.HeadStructure()
    head.CtrlHeadStructure(sz)

    #Ribbon 
    if cb_Rib:
        if smallUsefulFct.importFileFromScene('Ribbon_MatX'):
            cb_attach=[True,True,True,True,True,True,True,True]
            ribbon.AttachRib(cb_attach)

        
    #General 
    cmds.select(clear=True)
    globalscale.CreateGlobal(sz)

    #Follows
    tools.CreateFollows()



# Function to set the selected color
def set_color(color):
    global selected_color
    selected_color = color

# Callback function to lock/unlock the text field
def update_text_field(enum_dropdown,cbObjUp,*arg):
    # Get the selected option
    selected = cmds.optionMenu(enum_dropdown, query=True, value=True)

    # Lock or unlock the text field based on selection
    if selected in("Object Up","Object Rotation Up"):
        cmds.textField(cbObjUp, edit=True, enable=True)
    else :
        cmds.textField(cbObjUp, edit=True, enable=False)

def update_text_field2(obj1,obj2,cbObjUp,*arg):
    is_checked = cmds.checkBox(cbObjUp, query=True, value=True)
    if is_checked:
        cmds.text(obj1, edit=True, enable=True)
        cmds.intField(obj2, edit=True, enable=True)
    else:
        cmds.text(obj1, edit=True, enable=False)
        cmds.intField(obj2, edit=True, enable=False)