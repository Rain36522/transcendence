from PutInShell import PutInShell
import readchar
from time import sleep
import sys
import select


raqA = 25
raqB = 25
raqSize = 10

while True:
    # Vérifie si une touche est prête à être lue sur l'entrée standard
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        key = readchar.readkey()
        if key == "w" and raqA - raqSize / 2 > 0: # Touche W pour monter
            raqA -= 1
            print("Touche W pour monter")
        elif key == "s" and raqA + raqSize / 2 < 50: # Touche S pour descendre
            raqA += 1
            print("Touche S pour descendre")
    
    # Mettre à jour l'affichage ou effectuer d'autres actions ici
    print("loop")
    sleep(0.1)
