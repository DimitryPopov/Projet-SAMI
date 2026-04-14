import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'optitrack-master//src'))
import mocap_node as mcn
import time, matplotlib.pyplot as plt

mymcn = mcn.MocapNode("PC169")
mymcn.run()

mymcn.updateModelInfo()
liste_valeur_x = []
liste_valeur_y = []
for i in range(200):
    pos2D , yaw = mymcn.getPos2DAndYaw("Lego7")
    liste_valeur_x.append(pos2D[0])
    liste_valeur_y.append(pos2D[1])
    print(pos2D,yaw)
    time.sleep(0.1)
mymcn.stop()
plt.plot(liste_valeur_x,liste_valeur_y)
plt.plot([0, 0, 3, 3, 0], [0, 3, 3, 0, 0])
plt.show()