import curses

def main(stdscr):
    # Configuration de curses
    curses.curs_set(0)  # Masquer le curseur
    stdscr.nodelay(1)   # Mode non-bloquant pour la saisie

    while True:
        # Récupère la touche pressée
        key = stdscr.getch()
        if key != -1:
            if key == curses.KEY_UP:
                stdscr.addstr("Flèche vers le haut appuyée\n")
            elif key == curses.KEY_DOWN:
                stdscr.addstr("Flèche vers le bas appuyée\n")
            elif key == curses.KEY_LEFT:
                stdscr.addstr("Flèche vers la gauche appuyée\n")
            elif key == curses.KEY_RIGHT:
                stdscr.addstr("Flèche vers la droite appuyée\n")
            elif key == ord('q'):
                break  # Quitter si la touche 'q' est pressée
        stdscr.refresh()  # Rafraîchir l'écran pour afficher les changements

if __name__ == "__main__":
    curses.wrapper(main)
