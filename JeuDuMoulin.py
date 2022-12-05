plateau = [["" for i in range(8) ] for i in range(3)]
print(plateau[0][1])
blanc = 9
noir = 9
phase1 = True
phase2 = False
phase3 = False
joueur = "noir"


def change_joueur(joueur):
    if joueur == "noir":
        joueur = "blanc"
    else:
        joueur = "noir"


def jouer_coup(coord, plateau, joueur):
    plateau[coord[0]][coord[1]] = joueur


def places_libres(plateau, joueur):
    places_libres = []
    for i in range(len(plateau)-1):
        for j in range(len(plateau[i])-1):
            if jouer_coup((i,j), plateau, joueur) == True:
                places_libres.append((i,j))
    return places_libres


def est_libre(coord, plateau):
    if plateau[coord[0]][coord[1]] == "":
        return True
    else:
        return False


def deplacement_possible(coord, pleteau, joueur):
    


while phase1:
#Décide de quel joueur joue
    change_joueur(joueur)
#Le joueur joue un coup
    place_libre = False
    while not place_libre:
        print("Le joueur", joueur, "doit choisir une case :")
        carre = int(input())
        point = int(input())
        coord = (carre,point)
        place_libre = est_libre(coord, plateau)
    jouer_coup(coord, plateau, joueur)
    if joueur == "blanc":
        blanc -= 1
    else:
        noir -= 1
#Changement de phase
    if blanc == 0 or noir == 0:
        phase1 = False
        phase2 = True
        break
    coup_possible = False


while phase2:
    print("phase2")
#Décide de quel joueur joue
    change_joueur(joueur)
#Changement de phase
    if blanc == 3 or noir == 3:
        phase2 = False
        phase3 = True
        break
#Le joueur joue un coup
    coup_possible = False:
    while not coup_possible:
        print("Le joueur", joueur, "doit choisir une case :")
        carre = int(input())
        point = int(input())
        coord = (carre, point)
        coup_possible = deplacement_possible(coord, plateau)
    jouer_coup(coord, plateau, joueur)


while phase3:
    if blanc == 2:
        print("Le joueur noir a gagné.")
        break
    elif noir == 2:
        print("Le joueur blanc a gagné.")
        break
