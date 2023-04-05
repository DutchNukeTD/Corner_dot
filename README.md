# Corner_dot
Connects two nodes with a dot inbetween in the corner with 'shift+.'. The scripts checks if the lowest node is left or right from the upper node and always creates the dot below the upper node. 
Make the dot jump to the other corner with the same keyboard shortcut. 

## install
1. Copy the Corner_dot.py file to your .nuke folder. 
2. Add the following text to your menu.py:

from Corner_dot import *

nuke.menu('Nodes').addCommand('Golan gizmos/Golan/cornerDot', "checkSelected()", "shift+.")
