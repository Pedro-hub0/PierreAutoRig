import maya.cmds as cmds
import re

def gael_Rivet( name='Rivet' ):
    '''
    Launch build Rivet for between given edges or on each given faces
    name : to define the Rivet name
    '''
    
    #--- Load needed plugin
    load_plugin( toLoad= ['matrixNodes'] )
    
    #--- Get subComponent Selection
    sels = cmds.ls(sl=True)
    
    #--- keep only edges and faces
    edges = cmds.filterExpand(sels, sm=32) or []
    faces = cmds.filterExpand(sels, sm=34) or []
    
    #--- Launch Build
    if len(edges) == 2 :
        #--- Create a Rivet inbetween to edges
        gael_build_Rivet(name, edges[0], edges[1])
    elif faces :
        for face in faces:
            #--- Create a Rivet for each face selected
            edges = convert_face_to_edges(face)
            print (edges)
            gael_build_Rivet(name, edges[0], edges[1])
    else:
        print ('select 2 edges or faces to build Rivet')

def load_plugin( toLoad= list() ):
    '''
    Check if the needed plugin already load. if not loaded, load and autoload check for the plugin
    
    :param toLoad: A list of the plugin name to load.
    :type toLoad: list
    '''
    # Get the plugin already loaded
    plugin_loaded = cmds.pluginInfo( query=True, listPlugins=True )
    
    for plugin in toLoad:
        # Check if the plugin wasn't already load
        if not plugin in plugin_loaded:
            # Load plugin
            cmds.loadPlugin( plugin )
        # autoLoad plugin
        if not cmds.pluginInfo( plugin, query=True, autoload=True ):
            cmds.pluginInfo( plugin, edit=True, autoload=True )

def convert_face_to_edges(face):
    '''
    For a given face return two uncontinus edges
    '''
    #--- convert face to edges
    edges = cmds.ls( cmds.polyListComponentConversion( face, ff=True, te=True ), fl=True )

    #--- Create a vertex set with the first edge
    setEdgeA = set(cmds.ls(cmds.polyListComponentConversion(edges[0], fe=True, tv=True), fl=True))
    
    #--- Search an edge without commun vertex
    for i in range( 1, len(edges) ):
        setEdgeB = set(cmds.ls(cmds.polyListComponentConversion(edges[i], fe=True, tv=True), fl=True))
        if not setEdgeA & setEdgeB:
            #--- return uncontinus edges
            return [edges[0], edges[i]]


def gael_build_Rivet(name, edgeA, edgeB):
    '''
    Build a Rivet between two given edges
    Edges can be from different mesh
    '''
    #---  init
    objA = edgeA.split('.')[0]
    objB = edgeB.split('.')[0]
    

    #--- Create Locator Rivet
    Rivet = cmds.spaceLocator(n=name)[0]
    
    #---  Create nodes
    nodes = []
    nodes.append( cmds.createNode('curveFromMeshEdge', n= Rivet + '_%s_Crv' %(objA)) )        # 0
    nodes.append( cmds.createNode('curveFromMeshEdge', n= Rivet + '_%s_Crv' %(objB)) )        # 1
    nodes.append( cmds.createNode('loft', n= Rivet + '_loft') )                               # 2
    nodes.append( cmds.createNode('pointOnSurfaceInfo', n= Rivet + 'posInfo') )               # 3
    nodes.append( cmds.createNode('fourByFourMatrix', n= Rivet + '_4by4_MTX') )               # 4
    nodes.append( cmds.createNode('decomposeMatrix', n= Rivet + '_dMTX') )                    # 5
    nodes.append( cmds.createNode('vectorProduct', n= Rivet + '_vectProd') )                  # 6
    
    #--- Set Nodes Connections
    #- Crv 1
    cmds.setAttr( nodes[0] + '.ei[0]', int(re.findall('\d+', edgeA)[-1]))
    cmds.connectAttr( objA + '.w', nodes[0] + '.im', f=True)
    
    #- Crv 2
    cmds.setAttr( nodes[1] + '.ei[0]', int(re.findall('\d+', edgeB)[-1]))
    cmds.connectAttr( objB + '.w', nodes[1] + '.im', f=True)
    
    #- Loft
    cmds.setAttr( nodes[2] + '.ic', size=2)
    cmds.setAttr( nodes[2] + '.u', True)
    cmds.setAttr( nodes[2] + '.rsn', True)
    cmds.connectAttr( nodes[0] + '.oc', nodes[2] + '.ic[0]', f=True) 
    cmds.connectAttr( nodes[1] + '.oc', nodes[2] + '.ic[1]', f=True) 

    #- Point on surface info
    cmds.setAttr( nodes[3] + '.turnOnPercentage', True)
    cmds.connectAttr( nodes[2] + '.os', nodes[3] + '.is', f=True) 

    #- Get Rotate
    cmds.connectAttr( nodes[3] + '.normal', nodes[6] + '.input1' ) 
    cmds.connectAttr( nodes[3] + '.tangentV', nodes[6] + '.input2' ) 
    cmds.connectAttr( nodes[6] + '.outputX', nodes[4] + '.in20' )
    cmds.connectAttr( nodes[6] + '.outputY', nodes[4] + '.in21' )
    cmds.connectAttr( nodes[6] + '.outputZ', nodes[4] + '.in22' )
    cmds.setAttr( nodes[6] + '.operation', 2)

    #--- Four By Four Matrix
    cmds.connectAttr( nodes[3] + '.positionX', nodes[4] + '.in30' )
    cmds.connectAttr( nodes[3] + '.positionY', nodes[4] + '.in31' )
    cmds.connectAttr( nodes[3] + '.positionZ', nodes[4] + '.in32' )
    cmds.connectAttr( nodes[3] + '.normalX', nodes[4] + '.in00' )
    cmds.connectAttr( nodes[3] + '.normalY', nodes[4] + '.in01' )
    cmds.connectAttr( nodes[3] + '.normalZ', nodes[4] + '.in02' )
    cmds.connectAttr( nodes[3] + '.tangentVx', nodes[4] + '.in10' )
    cmds.connectAttr( nodes[3] + '.tangentVy', nodes[4] + '.in11' )
    cmds.connectAttr( nodes[3] + '.tangentVz', nodes[4] + '.in12' )

    #--- Decompose Matrix
    cmds.connectAttr( nodes[4] + '.output', nodes[5] + '.inputMatrix' )

    #--- Drive Rivet
    cmds.connectAttr( nodes[5] + '.outputTranslate', Rivet + '.translate' )
    
    cmds.connectAttr( nodes[5] + '.outputRotate', Rivet + '.rotate' )

    #--- Add Ctrl attributes to Rivet
    cmds.addAttr(Rivet, ln='posU', at='float', min=.0, max=1.0, dv=.5, k=True)
    cmds.addAttr(Rivet, ln='posV', at='float', min=.0, max=1.0, dv=.5, k=True)
    
    cmds.connectAttr( Rivet + '.posU', nodes[3] + '.parameterU', f=True)
    cmds.connectAttr( Rivet + '.posV', nodes[3] + '.parameterV', f=True) 

    #--- Historical intereset
    for node in nodes :
        cmds.setAttr( node + '.ihi', 0)
    
    cmds.setAttr( Rivet + 'Shape.ihi', 0)

    #--- Clean
    for attr in ['t', 'r', 's'] :
        for axis in ['x', 'y', 'z'] :
            cmds.setAttr('%s.%s%s' %(Rivet, attr, axis), k=False)
    for axis in ['X', 'Y', 'Z'] :
        cmds.setAttr('%sShape.localPosition%s' %(Rivet, axis), k=False, cb=False)

gael_Rivet()