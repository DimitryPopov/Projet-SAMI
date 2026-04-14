Le protocole natif de Motive est nommé NatNet. Les trame au format NatNet sont transmises en broadcast pour fournir les positions des mobiles.

Un exemple en Python permet de suivre le fonctionnement de la communication entre un observateur (PythonClient) et le logiciel Motive.

Le module PythonClient se trouve dans le NatNetSDK/Samples. Il est constitué de 2 fichiers Python NatNetClient et PythonSample.py. Le second n'a pour objectif que d'intencier un objet NatNetClient avec 2 threads : receiveNewFrame, receiveRigidBodyFrame prêt à dialoguer avec Motive avant d'exécuter le client (méthode run).


## NatNatClent

### Les méthods

  * run : appelé par le PythonClient.py
  * sendCommand : appelé à la fin de la méthode run.
  * __processMessage : regarde les 4 premiers octets pour connaitre le type de trame et la longueur du message avant de ventiler vers les méthodes de décriptage des messages. Les types de trame sont :
    * NAT_PING                  = 0 
    * NAT_PINGRESPONSE          = 1 : retourne la version des trames NatNet par défaut 3.0.0.0 
    * NAT_REQUEST               = 2
    * NAT_RESPONSE              = 3 : utiliser par trace (débuggage)
    * NAT_REQUEST_MODELDEF      = 4
    * NAT_MODELDEF              = 5 : appel __unpackDataDescriptions
    * NAT_REQUEST_FRAMEOFDATA   = 6
    * NAT_FRAMEOFDATA           = 7 : appel __unpackMocapData
    * NAT_MESSAGESTRING         = 8 : utiliser par trace (débuggage)
    * NAT_DISCONNECT            = 9 
    * NAT_UNRECOGNIZED_REQUEST  = 100 : utiliser par trace (débuggage)
  * __dataThreadFunction : cette fonction écoute la socket avec un buffer de 32ko et tramet les trames à __processMessage
  * __unpackDataDescriptions : décrypte les trames NAT_MODELDEF (5)
  * __unpackSkeletonDescription
  * __unpackRigidBodyDescription
  * __unpackMarkerSetDescription
  * __unpackMocapData : décrypte les trames NAT_FRAMEOFDATA (7)
  * __unpackSkeleton  : appelé par __unpackMocapData
  * __unpackRigidBody : appelé par __unpackMocapData et __unpackSkeleton
  * __createCommandSocket
  * __createDataSocket
  * __init__

### Les Tests

Le dossier Tests contient les codes Ruby de tests ; notamment d'analyse des trames sur la base de l'exemple PythonClient des Samples du NatNatSDK. Un dossier streamData contient un certtain nombre de collècte de trame effectué en écoutant le multicast avec le programme serveurOptitrack.rb qui écoute le réseau et récupère les messages/trames transmises par Motive.

  * Test_streamNatNet : permet de lire les différents fichiers du dossier streamData et détermine sur les premiers octet le type de trame transmise.
  * Test_unpackMocapData analyse les trames de type NAT_FRAMEOFDATA 7
  * Test_unpackMocapData analyse les trames de type NAT_MODELDEF 5. Pour le moment nous n'avons pas d'extraction de tel messages.

### __unpackMocapData
Lorsqu'on séléctione RigidBody, des informations sur les RigidBody sont transmise avec le nom du corps dans la trame. C'est le premier type de trame étudié contenu dans les fichiers Asset&RigidBody20201012.bin et trameAssetM_RigidB.bin.

### __unpackDataDescriptions