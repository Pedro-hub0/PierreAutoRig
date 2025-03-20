### Script by PierreLip - 2025 ##

import maya.cmds as cmds
import sys
import os

def create_ui():
    # Create a window
    if cmds.window("WindoCamShake", exists=True):
        cmds.deleteUI("WindoCamShake", window=True)

    window = cmds.window("WindoCamShake",title="Cam Shake", widthHeight=(300, 100),sizeable=False)
    # Create a layout
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.separator(h=15)
    cmds.text(label="- Select your camera", font = "plainLabelFont" , w = 200, align = "left")
    cmds.text(label="- Click on camera shake", font = "plainLabelFont" , w = 200, align = "left")
    cmds.separator(h=15)
    # Create a button
    cmds.button(label='Create CAM SHAKE Attributes', command=lambda x:camShake(),width=150)
    # Show the window
    cmds.showWindow(window)


def camShake():
    selection=cmds.ls(selection=True)
    for sel in selection:
        if is_camera(sel):
            cmds.addAttr(sel, longName='Shake_Vertical', attributeType='enum', enumName='___', defaultValue=0,keyable=True)
            cmds.setAttr(sel + '.Shake_Vertical', lock=True)
            cmds.addAttr(sel, longName='V_Speed', attributeType='float', defaultValue=0,keyable=True)
            cmds.addAttr(sel, longName='V_Intensity', attributeType='float', defaultValue=0,keyable=True)
            cmds.addAttr(sel, longName='Shake_Horizontal', attributeType='enum', enumName='___', defaultValue=0,keyable=True)
            cmds.setAttr(sel + '.Shake_Horizontal', lock=True)
            cmds.addAttr(sel, longName='H_Speed', attributeType='float', defaultValue=0,keyable=True)
            cmds.addAttr(sel, longName='H_Intensity', attributeType='float', defaultValue=0,keyable=True)

            cam_Shape=get_camera_shape(sel)
            exp_Shake = f'''{cam_Shape}.horizontalShake=noise(frame*{sel}.H_Speed)*{sel}.H_Intensity;
{cam_Shape}.verticalShake=noise(frame*{sel}.V_Speed)*{sel}.V_Intensity;
                        '''
            cmds.setAttr(f"{cam_Shape}.shakeEnabled",1)

            exp_name_Shake = f"Exp_Shake_{sel}"
            cmds.expression(name=exp_name_Shake, string=exp_Shake)


        


def get_camera_shape(camera_transform):
    # Check if the transform node exists
    if cmds.objExists(camera_transform):
        # List the shape nodes under the transform node
        shapes = cmds.listRelatives(camera_transform, shapes=True, type='camera')

        # Return the first shape node found (usually there's only one)
        if shapes:
            return shapes[0]
    return None

def is_camera(node):
    # Check if the node exists
    if cmds.objExists(node):
        # List the shapes under the transform node
        shapes = cmds.listRelatives(node, shapes=True) or []

        # Check if any of the shapes are of type 'camera'
        for shape in shapes:
            if cmds.nodeType(shape) == 'camera':
                return True
    return False

create_ui()