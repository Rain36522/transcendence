
from random import randint

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BGREENLIGHT = "\033[92m"
ORANGE = "\033[38;2;255;165;0m"

def getMixLevel(player):
        game4p = 1
        game2p = 0
        player -= 4
        while player > 4 and not ((player) / 2) % 2:
            game4p += 1
            player -= 4
        while player >= 8:
            game4p += 1
            player -= 4
        while player:
            game2p += 1
            player -= 2
        if (game2p + game4p) % 2 and game2p >= 2:
            game2p -= 2
            game4p += 1
        while (game2p + game4p) % 2:
            game4p -= 1
            game2p += 2
        if not game2p and game4p >=  4:
            game2p = 4
            game4p -= 2
        if game4p >= 4:
            game4p -= 2
            game2p += 4
        liste = []
        while game4p and game2p:
            if randint(1, 2) % 2:
                liste.append(4)
                game4p -= 1
            else:
                liste.append(2)
                game2p -= 1
        while game4p:
            liste.append(4)
            game4p -= 1
            game2p -= 1
        return liste
        
def GenerateMixTree(player):
    MatchListe = []
    while player >= 6:
        print("loop", player)
        listeMatchLevel = getMixLevel(player)
        player = len(listeMatchLevel)
        MatchListe.append(listeMatchLevel)
    if player == 4:
        liste = [4]
    else:
        liste = [2]
    MatchListe.append(liste)
    return MatchListe
            
j = 6
while j <= 32:

    liste = GenerateMixTree(j)
    print(MAGENTA,"for", j, "players")
    for i in liste:
        y = 0
        for x in i:
            y += x
        if y == j:
            print(GREEN, end="")
        else:
            print(RED, end="")
        for x in i:
            print(str(x) + ", ", end="")
        print("")
    print(BLUE, "<======================================================>", RESET)

        
    print(RESET)
    j += 2


