def cree_plateau_9j():
    '''
    Renvoie un plateau vide de la variante à 9 jetons
    '''
    t = [["X" for i in range(7)] for i in range(7)]
    for i in range(7):
        t[i][i], t[i][6-i] = "", ""
        t[3][i], t[i][3] = "", ""
    t[3][3] = "Centre"
    return t


def place(plateau, coord, joueur):
    '''
    Place un pion sur la case demandée
    '''
    plateau[coord[0]][coord[1]] = joueur


def retire(plateau, coord):
    '''
    Retire un pion
    '''
    plateau[coord[0]][coord[1]] = ""


def deplace(plateau, coord1, coord2, joueur):
    retire(plateau, coord1)
    place(plateau, coord2, joueur)


def change_joueur(joueur):
    '''
    Change le joueur
    '''
    if joueur == "noir":
        return "blanc"
    else:
        return "noir"


def cases_libres(plateau):
    '''
    Renvoie la liste des cases libres d'un plateau
    '''
    cases_libres = []

    for i in range(len(plateau)-1):
        for j in range(len(plateau[i])-1):
            if est_libre(plateau, (i,j)) == True:
                cases_libres.append((i,j))
    return cases_libres


def est_libre(plateau, coord):
    '''
    Vérifie que la case est libre
    '''

    if plateau[coord[0]][coord[1]] == "":
        return True
    else:
        return False


def cases_adjacentes(plateau, coord):
    '''
    Renvoie la liste des coordonnées des cases adjacentes rectilignes
    '''
    liste = []
    x, y = coord[0], coord[1]

    #Parcours latéral
    for j in range(y, -1, -1):
        if plateau[x][j] != "X":
            liste.append((x,j))
            break
    for j in range(y, len(plateau[x])-1):
        if plateau[x][j] == "X":
            liste.append((x,j))
            break
    #Parcours en hauteur
    for i in range(x, -1, -1):
        if plateau[i][y] != "X":
            liste.append((i,y))
            break
    for i in range(x, len(plateau)-1):
        if plateau[i][y] != "X":
            liste.append((i,y))
            break

    return liste


def deplacement_possible(plateau, coord1, coord2):
    '''
    Vérifie que le déplacement voulu soit possible
    '''
    x, y = coord2[0], coord2[1]

    if plateau[x][y] != "":
        return False
    elif (x,y) not in cases_adjacentes(plateau, coord1):
        return False
    return True


def donne_moulin(plateau, coord, joueur):
    '''
    Renvoie les coordonnées des cases d'un moulin.
    '''
    moulin = []
    x, y = coord[0], coord[1]

    #Parcours latéral du plateau
    compteur = 0
    for j in range(y, -1, -1):
        case = plateau[x][j]
        if case == joueur:
            compteur += 1
            moulin.append((x,j))
        elif case != "X":
            break
            
    for j in range(y, len(plateau[0])-1):
        case = plateau[x][j]
        if case == joueur:
            compteur += 1
            moulin.append((x,j))
        elif case != "X":
            break

    if compteur == 3:
        return moulin

    #Parcours en hauteur du plateau
    moulin = []
    compteur = 0
    for i in range(x, -1, -1):
        case = plateau[i][y]
        if case == joueur:
            compteur += 1
            moulin.append((x,j))
        elif case != "X":
            break

    for i in range(x, len(plateau)-1):
        case = plateau[i][y]
        if case == joueur:
            compteur += 1
            moulin.append((x,j))
        elif case != "X":
            break
    return moulin


def kill_possible(plateau, coord):
    '''
    Vérifie si le pion peut être retiré.
    '''
    case = plateau[coord[0]][coord[1]]
    if case == "noir" or case == "blanc":
        True
    return False


## INITIALISATION ##

#Créer le plateau
plateau = cree_plateau_9j()
#Compteurs de jetons
blanc = 9 
noir = 9
#Déclencheur des différentes phases
phase1 = True
phase2 = False
phase3 = False
#Désigne le joueur qui joue en premier
joueur = "noir"
#Liste des moulins formés
liste_moulins = []

## LANCEMENT DU JEU ##
running = True
while running:

    '''Affiche le tableau du plateau'''
    for ligne in plateau:
        print(ligne)
    if phase1 == True:
        '''Placement d'un pion'''
        while True:
            print("Le joueur", joueur, "doit choisir une case :")
            x = int(input())
            y = int(input())
            coord = (x, y)
            if est_libre(plateau, coord) == True:
                break
        place(plateau, coord, joueur)
        if joueur == "blanc":
            blanc -= 1
        else:
            noir -= 1

    elif phase2 == True:
        '''Déplacement d'un pion'''
        while True:
            print("Le joueur", joueur, "doit choisir un pion à déplacer :")
            x1 = int(input())
            y1 = int(input())
            coord1 = (x, y)
            if plateau[x1][y1] == joueur:
                break
        while True:
            print("Le joueur", joueur, "doit choisir une case :")
            x2 = int(input())
            y2 = int(input())
            coord2 = (x, y)
            if deplacement_possible(plateau, (x1, y1), (x2, y2)) == True:
                break
        deplace(plateau, coord1, coord2, joueur)

#    '''Formation d'un moulin'''
#    moulin = donne_moulin(plateau, (x,y), joueur)
#    if len(moulin) == 3:
#        for coord in moulin:
#            plateau[coord[0]][coord[1]] += "-m"
#        while True:
#           print("Veuillez choisir un pion à retirer")
#            x = int(input())
#            y = int(input())
#            if kill_possible(plateau, coord) == True:
#                break
#        retire_pion(x, y)
#        liste_moulins.append(moulin)
#        if joueur == "noir":
#            noir += 1
#        else:
#            blanc += 1

    '''Désigne le joueur qui joue au prochain tour'''
    joueur = change_joueur(joueur)

    '''Changement de phase'''
    if phase1 == True and (blanc == 0 or noir == 0):
        phase1 = False
        phase2 = True

    elif phase2 == True and (blanc == 7 or noir == 7):
        print("oui",phase2)
        print("Le joueur ", joueur, "a gagné!!")
        running = False
        
