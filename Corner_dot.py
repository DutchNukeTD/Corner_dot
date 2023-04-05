# Create dot in the corner or move it to opposites corner. 
# 30-12-2021
# Bug fix
# 07-02-223

import nuke

#Selected nodes
def selectNodes():
    global nodes 
    nodes = nuke.selectedNodes()

    global lenNodes
    lenNodes = len(nodes)
    return nodes


#Getting info on selected nodes. 
def positions(nodeList):

    xpositions = []
    ypositions = []
    nWidth = []
    nHeight = []
    positions.count = 0
    dotList = []

    for node in nodeList:
        xpos = node.xpos()
        ypos = node.ypos()
        xpositions.append(xpos)
        ypositions.append(ypos)
        nWidth.append(node.screenWidth())
        nHeight.append(node.screenHeight())   

    positions.upperNode = ''
    positions.lowerNode = ''
    positions.leftNode = ''
    positions.rightNode = ''
    
    # checking lowerNode / upperNode
    for node in nodeList:
        if node.ypos() == max(ypositions):
            positions.lowerNode = node
        if node.ypos() == min(ypositions):
            positions.upperNode = node

    # checking leftNode / rightNode
    for node in nodeList:        
        if node.xpos() == min(xpositions):
            positions.leftNode = node
        if node.xpos() == max(xpositions):
            positions.rightNode = node


    # Dot info
    dot = nuke.nodes.Dot()
    positions.dotWidth  = dot.screenWidth()
    positions.dotHeight = dot.screenHeight()
    nuke.delete(dot)

    positions.downRight =  [ positions.upperNode.xpos() + ((positions.upperNode.screenWidth() * .5) - (positions.dotWidth * .5)), positions.lowerNode.ypos() + ((positions.lowerNode.screenHeight() *.5) - (positions.dotHeight *.5)) ]
    positions.downLeft =   [ positions.upperNode.xpos() + ((positions.upperNode.screenWidth() * .5) - (positions.dotWidth * .5)), positions.lowerNode.ypos() + ((positions.lowerNode.screenHeight() *.5) - (positions.dotHeight *.5)) ]
    positions.upperRight = [ positions.lowerNode.xpos() + ((positions.lowerNode.screenWidth() * .5) - (positions.dotWidth * .5)), positions.upperNode.ypos() + ((positions.upperNode.screenHeight() *.5) - (positions.dotHeight *.5)) ]
    positions.upperLeft =  [ positions.lowerNode.xpos() + ((positions.lowerNode.screenWidth() * .5) - (positions.dotWidth * .5)), positions.upperNode.ypos() - ((positions.upperNode.screenHeight() *.5) - (positions.dotHeight *.5)) ]


    if lenNodes == 1:
        if nodes[0].xpos() == positions.downLeft[0] and nodes[0].ypos() == positions.downLeft[1]:
            nodes[0].setXYpos( int(positions.upperRight[0]), int(positions.upperRight[1]) )
        else: # Upper Right --> Down Left
            nodes[0].setXYpos( int(positions.downLeft[0]), int(positions.downLeft[1]) )

    elif lenNodes == 2:
        dot = nuke.nodes.Dot() # Dot is created.

       # input checks from selected nodes. 
        
        # lowerNode has no node in inputs
        if positions.lowerNode.inputs() == False:
            # Checking if upperNode inputs match lowerNode. 
            for input in range(0, positions.upperNode.inputs()):
                if positions.upperNode.input(input) == positions.lowerNode:
                    print('Hier is waar het fout gaat!') 
                    dot.setInput(0, positions.lowerNode)
                    positions.upperNode.setInput(input, dot)
            else:
                dot.setInput(0, positions.upperNode)
                positions.lowerNode.setInput(0, dot) # Connect dot to input B

        # only B input has a input
        elif positions.lowerNode.inputs() == 1:
            if positions.lowerNode.input(0) == positions.upperNode: # input is selectednode
                dot.setInput(0, positions.upperNode)
                positions.lowerNode.setInput(0, dot) # Connect dot to input B

            else: # selectednode is connected to A input.
                dot.setInput(0, positions.upperNode)
                positions.lowerNode.setInput(1, dot) # Connect dot to input A

        # lowernode has 2 or more inputs
        elif positions.lowerNode.inputs() >= 2:
            # check all inputs and add them to a list.
            nodeInputs = []

            for input in range(positions.lowerNode.inputs()):
                if positions.lowerNode.input(input) == None: # Add's 'Empty' to 'MergeInputs'
                    empty = 'Empty'
                    nodeInputs.append(empty)
                else:
                    nodeInputs.append(positions.lowerNode.input(input).name())

            # Check if selected nodes are already connected.
            if positions.upperNode.name() in nodeInputs:    
                dot.setInput(0, positions.upperNode)
                positions.lowerNode.setInput(nodeInputs.index(positions.upperNode.name()), dot)

            # If not connected and input >= 2 set input + 1.
            elif positions.upperNode.name() not in nodeInputs and 'Empty' not in nodeInputs:
                newInput = len(nodeInputs)
                dot.setInput(0, positions.upperNode)
                positions.lowerNode.setInput(newInput, dot)

            else: # Connected to empty input A of B
                dot.setInput(0, positions.upperNode)
                positions.lowerNode.setInput(nodeInputs.index('Empty'), dot)
        
        # Deselect all. 
        # Set dot as selected. 
        # assign nuke.selected to the dot. 
        # restart script. Now only with dot selected. 
        for i in nuke.allNodes():
            i.setSelected(False)
#        nukescripts.clear_selection_recursive()
        dot.setSelected(True)
        nodes[0] = dot
        jumpDot()


def jumpDot():
    dotUp = ''
    dotDown = ''
    
    if len(selectNodes()) == 1:
        if nodes[0].Class() == 'Dot':    
            dot = nodes[0]
            dotUp = dot.dependencies()
            dotUp = dotUp[0]
            dotDown = dot.dependent()
            dotDown = dotDown[0]

    dotDepends = [dotUp, dotDown]
    positions(dotDepends)
    
    
# check de selected nodes
def checkSelected():
    
    # if dot is selected
    if len(selectNodes()) == 1:
        if nodes[0].Class() == 'Dot':
            if len(nodes[0].dependencies()) and len(nodes[0].dependent()) == 1: ## Dot has a upper AND lower connection. 
                jumpDot()
            else:
                pass ## Dot has no connections --> doens't know where to jump too
        else: ## selectNode is not a Dot. --> runs cornerNode()
            cornerNode()    
    
    # if 2 nodes are selected
    # check nodes info. 
    elif len(selectNodes()) == 2:
        positions(selectNodes())
    else:
        pass 

#checkSelected()

#############################################
## Created another script, but joined here ##
## cornerNode.py ############################
#############################################

# Move selected node to the corner of connected node. 
# 27-06-2022


def cornerNode():
    selectedNode = nuke.selectedNode()
    ## SelectedNode info
    selectedNodeScreenHeight = selectedNode.screenHeight()
    selectedNodeScreenWidth = selectedNode.screenWidth()        

    ## Check inputs
    if selectedNode.Class() == 'Dot':
        pass ## This is done by another script. 
    else:
        if len(selectedNode.dependencies()) == 1 and len(selectedNode.dependent()) == 1:
            print('1')
            targetUp = selectedNode.dependencies()[0]
            targetUpXpos = targetUp['xpos'].value()
            targetUpYpos = targetUp['ypos'].value()
            targetUpScreenHeight = targetUp.screenHeight()
            targetUpScreenWidth = targetUp.screenWidth()
    
            targetDown = selectedNode.dependent()[0]
            targetDownXpos = targetDown['xpos'].value()
            targetDownYpos = targetDown['ypos'].value()
            targetDownScreenHeight = targetDown.screenHeight()
            targetDownScreenWidth = targetDown.screenWidth()
    
            if selectedNodeScreenHeight == targetUpScreenHeight and selectedNodeScreenHeight == targetDownScreenHeight: ## Node sizes are the same
                if selectedNode['xpos'].value() == targetUpXpos and selectedNode['ypos'].value() == targetDownYpos: ## Switch corners 
                    selectedNode.setXpos(int(targetDownXpos))
                    selectedNode.setYpos(int(targetUpYpos))
                else:
                    selectedNode.setXpos(int(targetUpXpos))
                    selectedNode.setYpos(int(targetDownYpos))

            else:
                if targetDown.Class() == 'Dot': ## Set targetDownXpos if targetDown == Dot##
                    targetDownXpos = targetDownXpos - ((selectedNodeScreenWidth*.5) - (targetDownScreenWidth *.5) )

                if targetUp.Class() == 'Dot': ## Set targetDownXpos if targetDown == Dot
                    targetUpXpos = targetUpXpos - ((selectedNodeScreenWidth *.5 ) - (targetUpScreenWidth * .5) )

                targetUpYpos = targetUpYpos + ((targetUpScreenHeight *.5 ) - (selectedNodeScreenHeight * .5))
                targetDownYpos = targetDownYpos + ((targetDownScreenHeight *.5 ) - (selectedNodeScreenHeight * .5))
                    

                if selectedNode['xpos'].value() == targetUpXpos and selectedNode['ypos'].value() == targetDownYpos:
                    selectedNode.setXpos(int(targetDownXpos))
                    selectedNode.setYpos(int(targetUpYpos)) 
                else:
                    selectedNode.setXpos(int(targetUpXpos))
                    selectedNode.setYpos(int(targetDownYpos))   

        elif len(selectedNode.dependencies()) == 2: ## Nodes with multi inputs (Merge and copy etc) Always A of the lift and B up. 
            targetUp = selectedNode.dependencies()[0]
            targetUpXpos = targetUp['xpos'].value()
            targetUpScreenWidth = targetUp.screenWidth()
            targetDown = selectedNode.dependencies()[1]
            targetDownXpos =targetDown['xpos'].value()
            targetDownYpos = targetDown['ypos'].value()
            targetDownScreenHeight = targetDown.screenHeight()
            targetDownScreenWidth = targetDown.screenWidth()

            print('targetUp = ' + str(targetUp.Class()))


            
            if selectedNodeScreenHeight == targetDownScreenHeight:    
                selectedNode.setXpos(int(targetUpXpos))
                selectedNode.setYpos(int(targetDownYpos))
            else:
                targetDownYpos = targetDownYpos + ((targetDownScreenHeight *.5 ) - (selectedNodeScreenHeight * .5))
            if targetUp.Class() == 'Dot': ## Set targetDownXpos if targetDown == Dot
                print('Dit moet uitgevoerd worden')
                targetUpXpos = targetUpXpos - ((selectedNodeScreenWidth *.5) - (targetUpScreenWidth * .5)) 

                selectedNode.setXpos(int(targetUpXpos))
                selectedNode.setYpos(int(targetDownYpos))
        else:
            pass 

#cornerNode()






