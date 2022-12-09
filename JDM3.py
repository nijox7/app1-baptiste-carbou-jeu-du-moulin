import fonctions_moulin 

def cree_plateau_9j():
    ''' Renvoie un plateau vide de la variante à 9 jetons '''
    t = [["X" for i in range(7)] for i in range(7)]
    for i in range(7):
        t[i][i], t[i][6-i] = "", ""
        t[3][i], t[i][3] = "", ""
    t[3][3] = "Centre"
    return t


def place(plateau, coord, joueur):
    ''' Place un pion sur la case demandée '''
    plateau[coord[0]][coord[1]] = joueur


def retire(plateau, coord):
    ''' Retire un pion '''
    plateau[coord[0]][coord[1]] = ""


def deplace(plateau, coord1, coord2, joueur):
    ''' Déplace un pion '''
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
    ''' Renvoie la liste des cases libres d'un plateau '''
    cases_libres = []

    for i in range(len(plateau)-1):
        for j in range(len(plateau[i])-1):
            if est_libre(plateau, (i,j)) == True:
                cases_libres.append((i,j))
    return cases_libres


def est_libre(plateau, coord):
    ''' Vérifie que la case est libre '''

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
    ''' Vérifie que le déplacement voulu soit possible '''
    x, y = coord2[0], coord2[1]

    if plateau[x][y] != "":
        return False
    elif (x,y) not in cases_adjacentes(plateau, coord1):
        return False
    return True


def parcours_largeur(plateau, coord):
    '''
    Renvoie la liste des coordononnées des cases latérales
    '''
    x, y = coord[0], coord[1]
    liste = []

    for j in range(y, -1, -1):
        if plateau[x][j] != "X":
            liste.append((x,j))
    liste.append(coord)
    for j in range(y, len(plateau[x])):
        if plateau[x][j]:
            liste.append((x,j))
    print("largeur", liste)
    return liste


def parcours_hauteur(plateau, coord):
    '''Renvoie les coordonnées des cases en hauteur'''
    liste = []
    x, y = coord[0], coord[1]
    for i in range(x, -1, -1):
         if plateau[i][y] != "X":
             liste.append((i, y))
    liste.append(coord)
    for i in range(x, len(plateau[y])):
        if plateau[i][y] != "X":
            liste.append((i, y))
    print("hauteur", liste)
    return liste


def donne_moulin(plateau, coord, joueur):
    '''
    Renvoie, si il y a formation de moulin, la liste
    des coordonnées des cases du moulin.
    '''
    liste1 = parcours_largeur(plateau, coord)
    moulin = []
    for coord in liste1:
        if plateau[coord[0]][coord[1]] != joueur:
            moulin = []
            break
    if moulin != []:
        return moulin

    liste2 = parcours_hauteur(plateau, coord)
    moulin = []
    for coord in liste2:
        if plateau[coord[0]][coord[1]] != joueur:
            moulin = []
            break
    return moulin


def forme_moulin(plateau, moulin):
    ''' Forme un moulin '''
    for coord in moulin:
        plateau[coord[0]][coord[1]] += "-m"


def suppr_moulin(plateau, m, liste_m, joueur):
    ''' Supprime un moulin '''
    for i in range(len(liste_m)):
        if liste_m[i] == m:
            liste_m.pop(i)
            break
    for coord in m:
        for e in liste_m:
            if coord not in e:
                plateau[coord[0]][coord[1]] = joueur


def peut_retirer(plateau, coord, joueur):
    case = plateau[coord[0]][coord[1]]
    if case == "blanc" or case == "noir":
        return True
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
        #Pion à déplacer
        while True:
            print("Le joueur", joueur, "doit choisir un pion à déplacer :")
            x1 = int(input())
            y1 = int(input())
            coord1 = (x, y) #Coordonnées du pion choisi
            if plateau[x1][y1] == joueur:
                break
        #Case visée par le joueur
        while True:
            print("Le joueur", joueur, "doit choisir une case :")
            x2 = int(input())
            y2 = int(input())
            coord2 = (x, y) #Coordonnées de la case visée
            if deplacement_possible(plateau, (x1, y1), (x2, y2)) == True:
                break
        #Supprime un moulin si le joueur déplace le pion d'un moulin.
        for moulin in liste_moulins:
            if coord1 in moulin:
                suppr_moulin(plateau, moulin, liste_moulins, joueur)
        deplace(plateau, coord1, coord2, joueur)

    '''Formation d'un moulin'''
    moulin = donne_moulin(plateau, (x,y), joueur)
    print(moulin)
    if len(moulin) == 3: #Vérifie si un moulin est formé
        forme_moulin(plateau, moulin)
        liste_moulins.append(moulin)
        #Demande au joueur de retirer un pion adverse
        while True:
            print("Le joueur", joueur,"doit choisir un pion à éliminer.")
            x = int(input())
            y = int(input())
            coord = (x, y)
            if peut_retirer(plateau, coord) == True:
                break
        retire(plateau, coord)

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
