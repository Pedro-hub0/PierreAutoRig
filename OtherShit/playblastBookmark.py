### Script by PierreLip - 2025 ##



import maya.cmds as cmds

def open_file_dialog(*args):
    # Open a file dialog to select a file
    folder_path = cmds.fileDialog2(fileMode=3, caption="Select File")

    # Check if a file was selected
    if folder_path:
        selected_folder = folder_path[0]  # Get the first selected folder
        print(f"Selected folder: {selected_folder}")

        # Update the text field with the selected folder path
        cmds.textField("folderPathTextField", edit=True, text=selected_folder)
        return selected_folder
    else:
        print("No file selected.")
        return None



def create_ui():
    # Create a window
    if cmds.window("WindoPlayblast", exists=True):
        cmds.deleteUI("WindoPlayblast", window=True)

    window = cmds.window("WindoPlayblast",title="Playblast Bookmark", widthHeight=(300, 150),sizeable=False)
    # Create a layout
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.separator(h=15)
    cmds.text(label="- Name your Cam: cam_NAME", font = "plainLabelFont" , w = 200, align = "left")
    cmds.text(label="- Name your Bookmark: NAME", font = "plainLabelFont" , w = 200, align = "left")
    cmds.text(label="- Select Cam or Nothing then Create Playblast", font = "plainLabelFont" , w = 200, align = "left")
    cmds.separator(h=15)
    # Create a button
    cmds.button(label="Select File", command=open_file_dialog)

    # Create a text field to display the selected folder path
    path=cmds.textField("folderPathTextField", editable=False, width=380)    # Create a button
    cmds.button(label='Create Playblast', command=lambda x:bookmarkPlayblast(path),width=150)
    cmds.button(label='Create Playblast 02', command=lambda x:bookmarkPlayblastAllBookmarkOneCam(path),width=150)
    # Show the window
    cmds.showWindow(window)


def do_playblast(cam, start_frame, end_frame,path,name):
    # Set the current camera to the specified camera
    n=f'pb_{name}'
    pathName=f'{path}/{n}'
    print(f'NAME : {pathName}')
    cmds.lookThru(cam)
    cmds.playblast(
        format="qt",
        filename=pathName,
        sequenceTime=False,
        clearCache=True,
        viewer=True,
        showOrnaments=False,
        fp=4,
        percent=100,
        compression="H.264",
        quality=100,
        startTime=start_frame,
        endTime=end_frame,
        forceOverwrite=True,
        widthHeight=(2048, 857)  # Add this flag to overwrite existing files
    )
    print(f"Playblast created from frame {start_frame} to {end_frame} with {cam}")
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


def bookmarkPlayblast(path="Documents"):
    if path != "Documents":
        path=cmds.textField(path,query=True, text=True)
    # Get all bookmarks
    bookmarks = cmds.ls('*timeSliderBookmark*') or []
    selection=cmds.ls(selection=True)
    if len(selection)>0:
        for sel in selection:
            name = sel.split('_')[-1]
            for bookmark in bookmarks:
                attName=cmds.getAttr(f'{bookmark}.name')
                if name in attName:
                    # Get the start time of the bookmark
                    start_time = int(cmds.getAttr(f'{bookmark}.timeRangeStart'))
                    # Get the end time of the bookmark (if it has a range)
                    end_time = int(cmds.getAttr(f'{bookmark}.timeRangeStop'))
                    cam=sel
                    if is_camera(cam):
                        do_playblast(cam,start_time,end_time,path,name)
    else: 
        if bookmarks:
            for bookmark in bookmarks:
                # Get the name of the bookmark
                name = cmds.getAttr(f'{bookmark}.name')
                
                # Get the start time of the bookmark
                start_time = int(cmds.getAttr(f'{bookmark}.timeRangeStart'))

                # Get the end time of the bookmark (if it has a range)
                end_time = int(cmds.getAttr(f'{bookmark}.timeRangeStop'))

                print(f"Bookmark: {name}, Start: {start_time}, End: {end_time if end_time else 'No range'} {path}")
                cam=f'cam_{name}'
                if cmds.objExists(cam):
                    do_playblast(cam,start_time,end_time,path,name)

        else:
            print("No bookmarks found.")

def bookmarkPlayblastAllBookmarkOneCam(path="Documents"):
    if path != "Documents":
        path=cmds.textField(path,query=True, text=True)
    # Get all bookmarks
    bookmarks = cmds.ls('*timeSliderBookmark*') or []
    selection=cmds.ls(selection=True)
    if len(selection)>0:
        for sel in selection:
            name = sel.split('_')[-1]
            for bookmark in bookmarks:
                attName=cmds.getAttr(f'{bookmark}.name')

                # Get the start time of the bookmark
                start_time = int(cmds.getAttr(f'{bookmark}.timeRangeStart'))
                # Get the end time of the bookmark (if it has a range)
                end_time = int(cmds.getAttr(f'{bookmark}.timeRangeStop'))
                cam=sel
                if is_camera(cam):
                    do_playblast(cam,start_time,end_time,path,attName)


# Call the function to create the UI
create_ui()