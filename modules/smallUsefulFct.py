import maya.cmds as cmds
import math
import os
import sys

###################################
###   SMALL USEFUL FUNCTIONS   ####
###################################        
def rotate_object_with_offset(object_name, x,y,z):
    # Get the current rotation of the object
    current_rotation = cmds.xform(object_name, query=True, rotation=True, worldSpace=True)
    # Add 90 degrees to the Y-axis rotation
    new_rotation = [current_rotation[0]+x, current_rotation[1] + y, current_rotation[2]+z]
    # Set the new rotation to the object
    cmds.xform(object_name, rotation=new_rotation, worldSpace=True)

def copy_rotation_to_list(source,destination):
    for i in range(0,len(source)):
        destination.append(cmds.xform(source[i], query=True, rotation=True, worldSpace=True))

def copy_translation_to_list(source,destination):
    for i in range(0,len(source)):
        destination.append(cmds.xform(source[i], q=True, t=True, ws=True))


def lock_and_hide_attributes(object_name):
# Lock and hide scale translation rotation attributes
    for axis in ['X', 'Y', 'Z']:
        cmds.setAttr(object_name + '.scale' + axis, lock=True, keyable=False)
        cmds.setAttr(object_name + '.translate' + axis, lock=True, keyable=False)
        cmds.setAttr(object_name + '.rotate' + axis, lock=True, keyable=False)


def copy_transform(source, destination):
    # Get translation and rotation values from the source object
    translation = cmds.xform(source, query=True, translation=True, worldSpace=True)
    rotation = cmds.xform(source, query=True, rotation=True, worldSpace=True)
    
    # Apply translation and rotation to the destination object
    cmds.move(translation[0], translation[1], translation[2], destination, absolute=True)
    cmds.rotate(rotation[0], rotation[1], rotation[2], destination, absolute=True)
    
def offset(selected):   

    # Create an empty group with the "_Offset" suffix
    offset = cmds.group(empty=True, name=selected + "_Offset")
    copy_transform(selected, offset)
    cmds.parent(selected, offset)

def offset2(selected):   
    # Create an empty group with the "_Offset" suffix
    offset = cmds.group(empty=True, name=selected + "_Offset")
    parent=cmds.listRelatives(selected,parent=True)

    copy_transform(selected, offset)
    cmds.parent(selected, offset)
    if  parent is not None:
        cmds.parent(offset,parent[0])

def move(selected):   
    # Create an empty group with the "_Offset" suffix
    offset = cmds.group(empty=True, name=selected + "_Move")
    copy_transform(selected, offset)
    cmds.parent(selected, offset)
    # Create an empty group with the "_Offset" suffix
    offset2 = cmds.group(empty=True, name=selected + "_Offset")
    copy_transform(offset, offset2)
    cmds.parent(offset, offset2)
    return offset2

def hook(selected):   
    # Create an empty group with the "_Move" suffix
    offset = cmds.group(empty=True, name=selected + "_Move")
    copy_transform(selected, offset)
    cmds.parent(selected, offset)
    # Create an empty group with the "_Hook" suffix
    offset2 = cmds.group(empty=True, name=selected + "_Hook")
    copy_transform(offset, offset2)
    cmds.parent(offset, offset2)
    # Create an empty group with the "_Offset" suffix
    offset3 = cmds.group(empty=True, name=selected + "_Offset")
    copy_transform(offset2, offset3)
    cmds.parent(offset2, offset3)
    
def organiser():
    if cmds.objExists("CTRL"):
        grp_Ctrl="CTRL"
    else:
        grp_Ctrl = cmds.group(empty=True, name="CTRL")
   
    if cmds.objExists("JNT"):
        grp_Jnt="JNT"
    else:
        grp_Jnt = cmds.group(empty=True, name="JNT")

    if cmds.objExists("Perso01"):
        grp_Perso="Perso01"
    else:
        grp_Perso = cmds.group(empty=True, name="Perso01")
    if cmds.objExists("Preserve_Jnts"):
        grp_preserve="Preserve_Jnts"
    else:
        grp_preserve = cmds.group(empty=True, name="Preserve_Jnts")
        cmds.parent(grp_preserve,grp_Jnt)

    if cmds.objExists('IKs'):
        grp_Iks='IKs'
    else:
        grp_Iks = cmds.group(empty=True, name="IKs")
    if not cmds.objExists('ExtraNodes'):
        grp_Extranode = cmds.group(empty=True, name="ExtraNodes")
    else:
        grp_Extranode="ExtraNodes"
    if cmds.objExists('GlobalMove'):
        grp_Global='GlobalMove'
    else:
        grp_Global = cmds.group(empty=True, name="GlobalMove")

        cmds.parent(f'{grp_Iks}',grp_Global)
        cmds.parent(f'{grp_Ctrl}',grp_Global)
        cmds.parent(f'{grp_Jnt}',grp_Global)
        cmds.parent(f'{grp_Extranode}',grp_Perso)
        cmds.parent(f'{grp_Global}',grp_Perso)




###### CHAT GPT #####
def getDistBetweenJnts(jnt01,jnt02):
    # Get the world space position of the two joints
    joint1_pos = cmds.xform(jnt01, query=True, worldSpace=True, translation=True)
    joint2_pos = cmds.xform(jnt02, query=True, worldSpace=True, translation=True)

    # Calculate the Euclidean distance between the two points
    distance = math.sqrt((joint2_pos[0] - joint1_pos[0]) ** 2 +
                        (joint2_pos[1] - joint1_pos[1]) ** 2 +
                        (joint2_pos[2] - joint1_pos[2]) ** 2)
    return distance


def set_curve_color(curve_name, color_index):
    # Get the shape node of the curve
    curve_shape = cmds.listRelatives(curve_name, shapes=True)[0]
    if curve_shape:
        # Set the overrideColor attribute to the specified color index
        cmds.setAttr(curve_shape + '.overrideEnabled', 1)
        cmds.setAttr(curve_shape + '.overrideColor', color_index)

def match_pivot(source_obj, target_obj):
    # Get the translation of the pivot of the target object
    pivot_translation = cmds.xform(target_obj, query=True, rotatePivot=True, worldSpace=True)
    # Set the translation of the pivot of the source object
    cmds.xform(source_obj, rotatePivot=pivot_translation, worldSpace=True)

def rotate_circle_vertices(circle_name,x,y,z):
    # Select the circle
    cmds.select(circle_name)
    current_translation = cmds.xform(circle_name, query=True, translation=True, worldSpace=True)
    # Convert selection to component mode (vertices)
    cmds.ConvertSelectionToVertices()

    # Get the selected vertices
    selected_vertices = cmds.ls(selection=True, flatten=True)

    # Rotate each selected vertex 90 degrees around the Y-axis
    for vertex in selected_vertices:
        cmds.rotate(x, y, z, vertex, relative=True, pivot=current_translation)

def move_object(object_name, translation,abs):
    # Translate the object
    if abs:
        cmds.move(translation[0], translation[1], translation[2], object_name, absolute=True)
    else:
        cmds.move(translation[0], translation[1], translation[2], object_name, r=True)

def is_joint(obj_name):
    """
    Check if the specified object is a joint.
    """
    if cmds.objectType(obj_name) == "joint":
        return True
    else:
        return False
    
def attribute_exists(obj_name, attr_name):
    """
    Check if the specified attribute exists on the given object.
    """
    return cmds.attributeQuery(attr_name, node=obj_name, exists=True)

def delete_non_joints_in_hierarchy(root_joint):
    # Get all descendants of the root_joint
    all_descendants = cmds.listRelatives(root_joint, allDescendents=True, fullPath=False) or []
    # Filter out the joints
    for node in all_descendants :
        if cmds.nodeType(node) != 'joint':
            cmds.delete(node)
    

def controller(n,tr,na,sz):
    # Define the control points
    control_points = [
        (-sz, sz, sz),
        (-sz, sz, -sz),
        (sz, sz, -sz),
        (sz, sz, sz),
        (-sz, sz, sz),
        (-sz, -sz, sz),
        (-sz, -sz, -sz),
        (-sz, sz, -sz),
        (-sz, sz, sz),
        (-sz, -sz, sz),
        (sz, -sz, sz),
        (sz, sz, sz),
        (sz, sz, -sz),
        (sz, -sz, -sz),
        (sz, -sz, sz),
        (sz, -sz, -sz),
        (-sz, -sz, -sz)
    ]

    # Create the curve
    if n==1:
        Translate=cmds.xform(tr, query=True, translation=True, worldSpace=True)
        curve = cmds.curve(d=1, p=control_points, k=[i for i in range(len(control_points))],name=na)
        cmds.move(Translate[0], Translate[1], Translate[2], curve, absolute=True)
        return curve



def importFileFromScene(file): 
        # Get the directory of the current Maya scene
    scene_path = cmds.file(query=True, sceneName=True)

    if scene_path:
        # Get the directory of the current scene
        scene_dir = os.path.dirname(scene_path)
        
        # Specify the file you want to import (replace "myFile.ma" with your file name)
        file_to_import = os.path.join(scene_dir, f"{file}.ma")

        # Check if the file exists
        if os.path.exists(file_to_import):
            # Import the .ma file into the current scene
            cmds.file(file_to_import, i=True)
            print(f"Imported: {file_to_import}")
        else:
            print(f"File not found: {file_to_import}")
    else:
        print("No scene is currently open.")


def addSuffix(obj,suffix): 
    list_obj=[]
    list_obj=cmds.listRelatives(obj,allDescendents=True)

    for l in list_obj:
        tempObj=l.split("|")[-1]
        cmds.rename(tempObj,f'{tempObj}{suffix}')

    cmds.rename(obj,f'{obj}{suffix}')


def cleanTransform(object_name):
    # Set translate to 0
    cmds.setAttr(f"{object_name}.translateX", 0)
    cmds.setAttr(f"{object_name}.translateY", 0)
    cmds.setAttr(f"{object_name}.translateZ", 0)

    # Set rotate to 0
    cmds.setAttr(f"{object_name}.rotateX", 0)
    cmds.setAttr(f"{object_name}.rotateY", 0)
    cmds.setAttr(f"{object_name}.rotateZ", 0)