# pyspacemouse-OSC
Un script python pour convertir en OSC la Spacemouse de 3Dconnexon

# Sommaire
- Problématique
- Explications techniques
- Installation
  - Dépendances
  - Windows/Linux/Mac x86 (proc intel)
  - MAC ARM (M1 et supérieur)
- Test
- Crédits

# Problématique
On souhaite exploiter les capacités de la Spacemouse dans le logiciel chataigne.
Cela permettrai de l'exploiter dans n'importe quelle installation de spectacle.
Mais la spacemouse n'a pas d'API direct pour l'exploiter, mais fonctionne via le protocole HID.
On veut donc récupérer les informations HID envoyées par la spacemouse et les convertir dans un langage que chataigne peut comprendre.

# Explications techniques
On va récupeérer les infos HID, les convertir en infos OSC, et chataigne pourra se connecter sur le serveur OSC pour recevoir les données (valable pour n'importe quel logiciel qui supporte OSC)
On va utiliser python pour obtenir un script fonctionnel autant sur Windows que sur Mac.
Il existe déjà une librairie pour recevoir le hid de la spacemouse.

# Installation
  #Dépendances
  - python 3.8 ou supérieur : https://www.python.org/downloads/
  - python-osc : https://pypi.org/project/python-osc/
  - pyspacemouse : https://pypi.org/project/pyspacemouse/
  - pour MAC ARM : le fichier exécutable libhidapi.dylib

  # Windows/linux/Mac x86
  - téléchargez et installez python 3
  - pour installer la librairie python-osc exécutez la commande suivante : pip3 install python-osc
  - pour installer pyspacemouse et libhidapi suivez les indications ici (remplacez pip par pip3) : https://pypi.org/project/pyspacemouse/
  - téléchargez le script spacemouse_to_OSC.py

  # MAC ARM (M1 et supérieur)
  - téléchargez et installez python 3
  - via terminal.app : pour installer la librairie python-osc exécutez la commande suivante : pip3 install python-osc
  - téléchargez le script spacemouse_to_OSC.py et le fichier exécutable libhidapi.dylib ; ils doivent impérativement être dans le même dossier

  # Test
  - exécutez le script spacemouse_to_OSC.py
  - déplacez la spacemouse pour tester le bon fonctionnement
  - le bouton de droite permet de change de mode
  - pour vous connecter à l'OSC, choisissez l'IP de votre machine, ou si vous êtes sur la même machine : 127.0.0.1; choisissez comme port : 32764
  - vérifiez que vous recevez bien les paquets OSC sur les adresses : /spacemouse/x (y, z, a, e, d, yaw, pitch, roll)

  # Crédits
  - pyspacemouse :  Jakub Andrýsek et kuband
  - script : tainalo2 Alexandre RONGIER : alexandre-rongier.fr
  - Un projet financé par la Fabsonic : https://lafabsonic.fr/
