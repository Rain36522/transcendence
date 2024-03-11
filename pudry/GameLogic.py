from PutInShell import PutInShell
import sys
import select
import termios
import tty
from time import sleep

raqA = 25
raqB = 25
raqSize = 10

# Sauvegarde des paramètres du terminal
old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

try:
    i = 1
    ballx = 10
    j = 1
    bally = 2
    while True:
        # Vérifie si une touche est prête à être lue sur l'entrée standard
        if select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)
            if (key == 'w' or key == "W") and raqA - raqSize / 2 > 0: # Touche W pour monter
                raqA -= 1
                # print("Touche W pour monter")
            elif (key == 's' or key == "S") and raqA + raqSize / 2 < 50: # Touche S pour descendre
                raqA += 1
            elif key == "q" or key == "Q":
                break
                # print("Touche S pour descendre")
        ballx += i
        bally += j
        if ballx >= 99:
            i = -1
        elif ballx <= 1:
            i = 1
        if bally >= 50:
            j = -1
        elif bally <= 0:
            j = 1
        # Mettre à jour l'affichage ou effectuer d'autres actions ici
        # print("loop")
        PutInShell(ballx, bally, raqA, raqB, raqSize)
        sleep(0.02)
finally:
    # Restauration des paramètres du terminal
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
