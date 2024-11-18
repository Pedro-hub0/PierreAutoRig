
import maya.cmds as cmds
import sys
import os
import importlib


# Get the folder containing the current script
script_dir = os.path.dirname(__file__)

# Add that folder to sys.path
sys.path.append(script_dir)

import modules.smallUsefulFct
import modules.RivetGael


importlib.reload(modules.smallUsefulFct)
importlib.reload(modules.RivetGael)



"""Script created by Pierre LIPPENS """

def create_window():
    """
    Create a window with a button.
    """
    # Check if the window already exists, and delete it if it does
    if cmds.window("myWindow", exists=True):
        cmds.deleteUI("myWindow", window=True)

    # Create the window
    window_name = cmds.window("myWindow", title="MatchIkFk_PierreAuto", widthHeight=(410, 200), sizeable=False)
    # Create a layout for the window
    scroll_layout = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)

    column_layout= cmds.columnLayout(adjustableColumn=True)


    cmds.separator(h=8)
    cmds.text(label="Zip", font = "boldLabelFont" , w = 300, align = "center")
    cmds.separator(h=8)

    cmds.text(label=" JntOnRivet ", font = "boldLabelFont" , w = 300, align = "left")
    cmds.text(label=" - Create 2 curves, Rebuild it. Use the script. Bind the curve to the head joints " , w = 300, align = "left")
    cmds.text(label=" - Bind the curve to the head joints " , w = 300, align = "left")
    cmds.text(label=" - Delete historic non deformer on the curves " , w = 300, align = "left")
    cmds.text(label=" - Bind the Joints to the geo " , w = 300, align = "left")

    cmds.separator(h=5)




    # Create a text field
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[100,100,100,100])
    cmds.text(label="Speed", font = "boldLabelFont" , w = 50, align = "left")
    speed = cmds.floatField(value=1.3,width=75)
    cmds.text(label="length", font = "boldLabelFont" , w = 50, align = "left")
    number = cmds.intField(value=10,width=75)
    cmds.setParent('..')

    cmds.frameLayout(label='RIVET VERSION',w = 300, collapsable=True, collapse=True)
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[100,100,100,100])
    cmds.button(label='Rivets Up', command=lambda x:modules.RivetGael.gael_Rivet("Riv_Up_"))
    cmds.button(label='Rivets Dwn', command=lambda x:modules.RivetGael.gael_Rivet("Riv_Dwn_"))
    cmds.button(label='Jnt', command=lambda x:createJnt())
    cmds.button(label='Blend', command=lambda x:createBlend(speed,number,'Rivet'))
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(label='Curve VERSION',w = 300, collapsable=True, collapse=True)

    cmds.button(label='Create Curve And Rebuild', command=lambda x:createCurveAndRebuild())

    cmds.button(label='Blend', command=lambda x:createBlend(speed,number,'Curve'))
    cmds.setParent('..')
    # RENAME
    cmds.frameLayout(label='RENAME',w = 300, collapsable=True, collapse=True)
    cmds.rowLayout(numberOfColumns=4, columnWidth4=[100,100,100,100])
    cmds.button(label='Rename Riv Up', command=lambda x:renameRiv('Riv_Up'),width=100)
    cmds.button(label='Rename Riv Dwn', command=lambda x:renameRiv('Riv_Dwn'),width=100)
    cmds.button(label='Rename Jnt Up', command=lambda x:renameRiv('Bind_Zip_Lips_Up'),width=100)
    cmds.button(label='Rename Jnt Dwn', command=lambda x:renameRiv('Bind_Zip_Lips_Dwn'),width=100)
    cmds.setParent('..')
    cmds.setParent('..')


    # Show the window
    cmds.showWindow(window_name)

def createJnt():
    jnts=[]

    selection=cmds.ls(selection=True)
    length=5
    for sel in selection:
        tr=cmds.xform(sel, query=True, worldSpace=True, translation=True)
        cmds.select(clear=True)
        jnt=cmds.joint(n=f'Bind_{sel}',p=tr)
        jnts.append(jnt)
        cmds.xform(jnt,translation=tr,worldSpace=True)

        
def createBlendRivet(speed,l):
    if not cmds.objExists("Zip_Ctrl"):
        Ctrls=cmds.circle(name=f'Zip_Ctrl',nr=[1,0,0])[0] 
    attrZipL="Zip_Ctrl.Zip_L"
    attrZipR="Zip_Ctrl.Zip_R"
    sp=cmds.floatField(speed, query=True, value=True) 
    length=cmds.intField(l, query=True, value=True)   
    for i in range(1,length+1):
        if not cmds.attributeQuery(f'Zip_R', node='Zip_Ctrl', exists=True):
            cmds.addAttr('Zip_Ctrl', longName=f'Zip_R',attributeType='float', defaultValue=0,min=0,max=1,keyable=True)
        if not cmds.attributeQuery(f'Zip_L', node='Zip_Ctrl', exists=True):
            cmds.addAttr('Zip_Ctrl', longName=f'Zip_L',attributeType='float', defaultValue=0,min=0,max=1,keyable=True)
        if not cmds.attributeQuery(f'Zip_Avg', node='Zip_Ctrl', exists=True):
            cmds.addAttr('Zip_Ctrl', longName=f'Zip_Avg',attributeType='float', defaultValue=0.5,min=0,max=1,keyable=True)
               
        ##NODES
        zipremap01= cmds.createNode('setRange', name=f'Zip_setRange_{i}')
        val=(length-i)*(1/length)
        #Time Space between every pinche join 
        val2=(length-i)*(1/length)+sp/length
        initialiseRemap(zipremap01,0,1,val,val2,'X')
        initialiseRemap(zipremap01,0,1,1-val2,1-val,'Y')
        initialiseRemap(zipremap01,0,1,0,1,'Z')
        blendavg = cmds.createNode('blendColors', name=f'Zip_blendavg_{i}')
        blendup = cmds.createNode('blendColors', name=f'Zip_blendup_{i}')
        blendwn = cmds.createNode('blendColors', name=f'Zip_blendwn_{i}')
        pmaLR = cmds.createNode('plusMinusAverage', name=f'Zip_pmaLR_{i}')
        cmds.setAttr(f'{pmaLR}.operation',1)


        ##NODES Connexions
        
        
        #Set Range
        cmds.connectAttr(attrZipR,f'{zipremap01}.valueX')
        cmds.connectAttr(attrZipL,f'{zipremap01}.valueY')
        cmds.connectAttr(f'Riv_Dwn_0{i}.translate',f'{blendavg}.color2')
        cmds.connectAttr(f'Riv_Up_0{i}.translate',f'{blendavg}.color1')
        cmds.connectAttr(f'Zip_Ctrl.Zip_Avg',f'{blendavg}.blender')

        #System L R
        cmds.connectAttr(f'{zipremap01}.outValueX',f'{pmaLR}.input1D[0]')
        cmds.connectAttr(f'{zipremap01}.outValueY',f'{pmaLR}.input1D[1]')
        cmds.connectAttr(f'{pmaLR}.output1D',f'{zipremap01}.valueZ')

        #Blend
        cmds.connectAttr(f'{zipremap01}.outValueZ',f'{blendup}.blender')
        cmds.connectAttr(f'{zipremap01}.outValueZ',f'{blendwn}.blender')
        cmds.connectAttr(f'{blendavg}.output',f'{blendup}.color1')
        cmds.connectAttr(f'{blendavg}.output',f'{blendwn}.color1')

        cmds.connectAttr(f'Riv_Dwn_0{i}.translate',f'{blendup}.color2')
        cmds.connectAttr(f'Riv_Up_0{i}.translate',f'{blendwn}.color2')

        #Connect to joints
        cmds.connectAttr(f'{blendup}.output',f'Bind_Zip_Lips_Dwn_0{i}.translate')
        cmds.connectAttr(f'{blendwn}.output',f'Bind_Zip_Lips_Up_0{i}.translate')




def createCurveAndRebuild():

    # Ensure something is selected
    selection = cmds.ls(selection=True, flatten=True)
    if not selection:
        cmds.error("Please select one or more edges.")

    # Filter the selection to edges
    edge_selection = [edge for edge in selection if ".e[" in edge]

    if not edge_selection:
        cmds.error("Please select valid edges.")
    curve = cmds.polyToCurve(form=2, degree=3, conformToSmoothMeshPreview=0)


    rebuilt_curve = cmds.rebuildCurve(curve, ch= 1 ,rpo =0,rt= 0 ,end =1 ,kr =0, kcp= 1 ,kep =1 ,kt =0,s=10 ,d= 3 ,tol= 0.01 )

def createBlend(speed,l,obj):

    if obj == "Curve":
        selection=cmds.ls(selection=True)
        if len(selection)!=2:
            raise ValueError(f"You need to select 2 Curves, not {selection}")
        CurveUp=selection[0]
        CurveDwn=selection[1]

    sp=cmds.floatField(speed, query=True, value=True) 
    length=cmds.intField(l, query=True, value=True)   
    pocUp=[]
    pocDwn=[]  
    JntUp=[]
    JntDwn=[]    
    if not cmds.objExists("Zip_Ctrl"):
        Ctrl_Zip=cmds.circle(name=f'Zip_Ctrl',nr=[1,0,0])[0] 
    else:Ctrl_Zip=f'Zip_Ctrl'
    attrZipL=f"{Ctrl_Zip}.Zip_L"
    attrZipR=f"{Ctrl_Zip}.Zip_R"



    ##Organise
    grp_JntsZip = cmds.group(empty=True, name="grp_Bind_Lips_Zips")
    grp_JntsZipUp = cmds.group(empty=True, name="grp_Bind_Lips_Zips_Up")
    grp_JntsZipDwn = cmds.group(empty=True, name="grp_Bind_Lips_Zips_Dwn")
    cmds.parent(grp_JntsZipUp,grp_JntsZip)
    cmds.parent(grp_JntsZipDwn,grp_JntsZip)



    for i in range(1,length+1):
        cmds.select(clear=True)
        JntDwn.append(cmds.joint(n=f'Bind_Zip_Lips_Dwn_0{i}'))
        cmds.select(clear=True)
        JntUp.append(cmds.joint(n=f'Bind_Zip_Lips_Up_0{i}'))
        if obj == 'Curve':
            cmds.parent(JntDwn[i-1],grp_JntsZipDwn)
            cmds.parent(JntUp[i-1],grp_JntsZipUp)
        elif obj =='Rivet':
            cmds.parent(JntDwn[i-1],f'Riv_Dwn_0{i}')
            cmds.parent(JntUp[i-1],f'Riv_Up_0{i}')
        modules.smallUsefulFct.move2(JntDwn[i-1])
        modules.smallUsefulFct.move2(JntUp[i-1])


        if not cmds.attributeQuery(f'Zip_R', node=f'{Ctrl_Zip}', exists=True):
            cmds.addAttr(f'{Ctrl_Zip}', longName=f'Zip_R',attributeType='float', defaultValue=0,min=0,max=1,keyable=True)
        if not cmds.attributeQuery(f'Zip_L', node=f'{Ctrl_Zip}', exists=True):
            cmds.addAttr(f'{Ctrl_Zip}', longName=f'Zip_L',attributeType='float', defaultValue=0,min=0,max=1,keyable=True)
        if not cmds.attributeQuery(f'Zip_Avg', node=f'{Ctrl_Zip}', exists=True):
            cmds.addAttr(f'{Ctrl_Zip}', longName=f'Zip_Avg',attributeType='float', defaultValue=0.5,min=0,max=1,keyable=True)
        if not cmds.attributeQuery(f'Drop_Off', node=f'{Ctrl_Zip}', exists=True):
            cmds.addAttr(f'{Ctrl_Zip}', longName=f'Drop_Off',attributeType='float', defaultValue=0,keyable=True)
        #if not cmds.attributeQuery(f'Speed', node=f'{Ctrl_Zip}', exists=True):
        #    cmds.addAttr(f'{Ctrl_Zip}', longName=f'Speed',attributeType='float', defaultValue=sp,keyable=True)
                            
        ##NODES
            ## Point On Curves
        ##NODES Connexions

        val3=i*(1/length)
        pma_DropOff=cmds.createNode('plusMinusAverage', name=f'Zip_pma_Dropoff_{i}')
        cmds.setAttr(f'{pma_DropOff}.input1D[0]',1)
        cmds.setAttr(f"{pma_DropOff}.operation",2)
        cmds.connectAttr(f'{Ctrl_Zip}.Drop_Off',f'{pma_DropOff}.input1D[1]')
        
        #Time Space between every pinche join 
        val2=(length-i)*(1/length)+sp/length
        zipremap01= cmds.createNode('setRange', name=f'Zip_setRange_{i}')
        val=(length-i)*(1/length)


        initialiseRemap(zipremap01,0,1,val,val2,'X')
        initialiseRemap(zipremap01,0,1,1-val2,1-val,'Y')
        initialiseRemap(zipremap01,0,1,0,1,'Z')
        blendavg = cmds.createNode('blendColors', name=f'Zip_blendavg_{i}')
        blendup = cmds.createNode('blendColors', name=f'Zip_blendup_{i}')
        blendwn = cmds.createNode('blendColors', name=f'Zip_blendwn_{i}')
        pmaLR = cmds.createNode('plusMinusAverage', name=f'Zip_pmaLR_{i}')
        cmds.setAttr(f'{pmaLR}.operation',1)


        if obj == "Curve":
            pocDwn.append(cmds.createNode('pointOnCurveInfo', name=f'Zip_PocDwn_{i}'))
            pocUp.append(cmds.createNode('pointOnCurveInfo', name=f'Zip_PocUp_{i}'))
            cmds.setAttr(f"{pocDwn[i-1]}.parameter",val3)            
            cmds.setAttr(f"{pocUp[i-1]}.parameter",val3)
            cmds.connectAttr(f'{CurveUp}.worldSpace[0]',f'{pocUp[i-1]}.inputCurve')
            cmds.connectAttr(f'{CurveDwn}.worldSpace[0]',f'{pocDwn[i-1]}.inputCurve')
            cmds.connectAttr(f'{pocDwn[i-1]}.position',f'{blendavg}.color2')
            cmds.connectAttr(f'{pocUp[i-1]}.position',f'{blendavg}.color1')
        
        elif obj == "Rivet":
            cmds.connectAttr(f'Riv_Dwn_0{i}.translate',f'{blendavg}.color2')
            cmds.connectAttr(f'Riv_Up_0{i}.translate',f'{blendavg}.color1')
            



        #Set Range
        cmds.connectAttr(attrZipR,f'{zipremap01}.valueX')
        cmds.connectAttr(attrZipL,f'{zipremap01}.valueY')
        cmds.connectAttr(f'{Ctrl_Zip}.Zip_Avg',f'{blendavg}.blender')
        cmds.connectAttr(f'{pma_DropOff}.output1D',f'{zipremap01}.maxZ')

        #System L R
        cmds.connectAttr(f'{zipremap01}.outValueX',f'{pmaLR}.input1D[0]')
        cmds.connectAttr(f'{zipremap01}.outValueY',f'{pmaLR}.input1D[1]')
        cmds.connectAttr(f'{pmaLR}.output1D',f'{zipremap01}.valueZ')

        #Blend
        cmds.connectAttr(f'{zipremap01}.outValueZ',f'{blendup}.blender')
        cmds.connectAttr(f'{zipremap01}.outValueZ',f'{blendwn}.blender')
        cmds.connectAttr(f'{blendavg}.output',f'{blendup}.color1')
        cmds.connectAttr(f'{blendavg}.output',f'{blendwn}.color1')
        if obj == "Curve":
            cmds.connectAttr(f'{pocDwn[i-1]}.position',f'{blendup}.color2')
            cmds.connectAttr(f'{pocUp[i-1]}.position',f'{blendwn}.color2')
            
        elif obj == "Rivet":
            cmds.connectAttr(f'Riv_Dwn_0{i}.translate',f'{blendup}.color2')
            cmds.connectAttr(f'Riv_Up_0{i}.translate',f'{blendwn}.color2')

        #Connect to joints

        cmds.connectAttr(f'{blendup}.output',f'Bind_Zip_Lips_Dwn_0{i}_Move.translate')
        cmds.connectAttr(f'{blendwn}.output',f'Bind_Zip_Lips_Up_0{i}_Move.translate')
    
    if obj == "Curve":
        # Delete non-deformer history
        cmds.bakePartialHistory(CurveUp, prePostDeformers=True)
        cmds.bakePartialHistory(CurveUp, prePostDeformers=True)



def initialiseRemap(n,a,b,c,d,axe):
        cmds.setAttr(f'{n}.min{axe}', a)
        cmds.setAttr(f'{n}.max{axe}', b)
        cmds.setAttr(f'{n}.oldMin{axe}', c)
        cmds.setAttr(f'{n}.oldMax{axe}', d)

def renameRiv(n):
    selObj = cmds.ls(selection=True)
    for i in range(0,len(selObj)):
        cmds.rename(selObj[i],f'{n}_0{i+1}')


