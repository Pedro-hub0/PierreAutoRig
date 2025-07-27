import maya.cmds as cmds
import maya.mel as mel
import os

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
    if cmds.window("WindoExportAbc", exists=True):
        cmds.deleteUI("WindoExportAbc", window=True)

    window = cmds.window("WindoExportAbc",title="ABC Sunbed Multi Export", widthHeight=(300, 150),sizeable=False)
    # Create a layout
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.separator(h=15)
    cmds.text(label="- Select GEOs", font = "plainLabelFont" , w = 200, align = "left")
    cmds.separator(h=15)
    # Create a button
    cmds.button(label="Select File", command=open_file_dialog)
    cmds.rowLayout(numberOfColumns=3, columnWidth3=[75,75,75])
    txt_Seq=cmds.textField(placeholderText="Sequence",width=100)
    txt_Shot=cmds.textField(placeholderText="Shot",width=100)
    txt_Version=cmds.textField(placeholderText="Version",width=100)
    cmds.setParent("..")
    # Create a text field to display the selected folder path
    path=cmds.textField("folderPathTextField", editable=False, width=380)    # Create a button
    txt=[txt_Seq,txt_Shot,txt_Version]
    cmds.button(label='Export ABC', command=lambda x:ExportAlembic(path,txt),width=150)

    # Show the window
    cmds.showWindow(window)


def ExportAlembic(path,txt):
    path=cmds.textField(path,query=True, text=True)
    # Get the selected objects
    selection = cmds.ls(selection=True, long=True)
    newtxt=[]
    # Get the timeline range from Maya playback options
    start_frame = int(cmds.playbackOptions(q=True, min=True))
    end_frame = int(cmds.playbackOptions(q=True, max=True))
    for txtextract in txt:
        txttemp=cmds.textField(txtextract, query=True, text=True)
        newtxt.append(txttemp)
        

    for obj in selection:
        # Get the short name for the object (strip namespaces or long names)
        obj_short_name = obj.split('|')[-1].split(':')[0].replace('|', '')

        
        # Build the output file path
        abc_filename = f"SS_seq{newtxt[0]}_sh{newtxt[1]}_{obj_short_name}_{newtxt[2]}.abc"
        print(abc_filename)
        abc_filepath = f"{path}/{abc_filename}"

        # Build Alembic export command
        abc_cmd = f'-frameRange {start_frame} {end_frame} -attr ptnum -attr shop_materialpath -stripNamespaces -uvWrite -writeVisibility -writeUVSets -dataFormat ogawa -root {obj} -file {abc_filepath}'

        # Run the export
        mel.eval(f'AbcExport -j "{abc_cmd}"')

        print(f"Exported {obj} to {abc_filepath}")


create_ui()