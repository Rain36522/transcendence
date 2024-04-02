from blessed import Terminal
import sys
import time

# Initialisation de la bibliothèque blessed
term = Terminal()

# Taille de l'écran
largeur = 120
hauteur = 50

# Paramètres de la balle
balle_x = largeur // 2
balle_y = hauteur // 2
balle_vitesse_x = 1
balle_vitesse_y = 1

# Fonction pour effacer l'écran et dessiner le cadre
def effacer_ecran():
    print(term.clear + term.move_xy(0, 0))
    print(term.bold('+') + term.bold('-' * (largeur - 2)) + term.bold('+'))
    for _ in range(hauteur - 2):
        print(term.bold('|') + ' ' * (largeur - 2) + term.bold('|'))
    print(term.bold('+') + term.bold('-' * (largeur - 2)) + term.bold('+'))

# Fonction pour dessiner la balle à une position donnée
def dessiner_balle(x, y):
    with term.location(x, y):
        print('O')

# Boucle principale
with term.cbreak(), term.hidden_cursor():
    while True:
        effacer_ecran()

        # Mise à jour de la position de la balle
        balle_x += balle_vitesse_x
        balle_y += balle_vitesse_y

        # Rebond de la balle sur les bords de l'écran
        if balle_x <= 1 or balle_x >= largeur - 2:
            balle_vitesse_x = -balle_vitesse_x
        if balle_y <= 1 or balle_y >= hauteur - 2:
            balle_vitesse_y = -balle_vitesse_y

        # Dessiner la balle à sa nouvelle position
        dessiner_balle(balle_x, balle_y)

        # Mettre en pause pour contrôler la vitesse de déplacement de la balle
        time.sleep(0.01)
