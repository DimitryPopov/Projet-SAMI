# coding: utf-8

""" Second exemple pour le noeud Motion Capture

Illustre le fonctionnement d'un noeud, comment obtenir une pose dans le repère Motive ou SAMI
et comment obtenir une position 2D et un yaw directement dans le repère SAMI

Auteur : Clement FAUVEL, Jean-Luc METZGER
Date : Février 2021
"""


import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'optitrack//src'))

import numpy as np

import mocap_node as mcn
import Natnet_Client as nnc
from debug import *
from common import *




def main():
    #  Remove former logfile
    if os.path.isfile(".trace.txt"):
        os.remove(".trace.txt")

    # Lego
    LegoName = "Lego3"

    # Configure fake server
    srvAddr = "100.64.212.150"
    srvPort  = 1510
    
    # Configure Natnet client
    cltAddr = "100.64.212.156"
    # cltAddr = "127.0.0.1"
    cltDataPort = 1511
    multcastaddr = "225.1.1.1"
    cltCmdPort = 0
    # natnet_client = nnc.NatnetClient(srvAddr,cltAddr,multcastaddr,srvPort,cltDataPort)   
    
    # Start a MocapNode
    mymcn = mcn.MocapNode("PCENSEM")
    mymcn.run()
    mymcn.updateModelInfo()

    # Affiche l'orientation du Lego 1 dans le repère Motive
    L1_pos, L1_rot = mymcn.getPose(LegoName)
    trace("EXEMPLE 1 - Demande la pose du {}".format(LegoName))
    trace("\tPosition repère Motive en [m]:\n\t\t[{:10.4f},{:10.4f},{:10.4f}]".format(*L1_pos))
    trace("\tRotation repère Motive en [°] :\n\t\t[{:10.4f},{:10.4f},{:10.4f}]".format(*np.degrees(euler_from_quaternion(*L1_rot))))
    # Effectue un changement de repère (facultatif)
    posSami = position_motive_to_sami(L1_pos)
    eulSami = orientation_motive_to_sami(L1_rot)
    # Affiche le résultat
    trace("\tPosition repère SAMI en [m] :\n\t\t[{:10.4f},{:10.4f},{:10.4f}]".format(*posSami))
    trace("\tRotation repère SAMI en [°] :\n\t\t[{:10.4f},{:10.4f},{:10.4f}]".format(*np.degrees(eulSami)))
    trace("EXEMPLE - FIN  --------------\n\n")

    # Demande directement la position 2D et le yaw dans le repère SAMI
    L1_pos2D, L1_yaw = mymcn.getPos2DAndYaw(LegoName)
    trace("EXEMPLE 2 - Demande directement la position 2D et le yaw du {}".format(LegoName))
    # Affiche le résultat
    trace("\tPosition repère SAMI en [m] :\n\t\t[{:10.4f},{:10.4f}]".format(*L1_pos2D))
    trace("\tRotation repère SAMI en [°] :\n\t\t[{:10.4f}]".format(*np.degrees(L1_yaw)))
    trace("EXEMPLE - FIN  --------------\n\n")

    # Stop threads
    mymcn.stop()
    trace("EXEMPLE - Arrêt du noeud MoCap")
    trace(mymcn.to_string() + "--------------\n\n")






if __name__ == "__main__":
    main()