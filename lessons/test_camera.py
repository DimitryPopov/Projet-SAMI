import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'optitrack-master//src'))
import mocap_node as mcn
import time

mymcn = mcn.MocapNode("PC5")
mymcn.run()

mymcn.updateModelInfo()
for i in range(100):
    pos2D, yaw = mymcn.getPos2DAndYaw("Lego3" )
    print(pos2D,yaw)
    time.sleep(1)
mymcn.stop()