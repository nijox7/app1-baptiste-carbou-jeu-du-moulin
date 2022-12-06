#Plateau à 9 jetons
t = [["X" for i in range(7)] for i in range(7)]
for i in range(7):
    t[i][i], t[i][6-i] = "", ""
    t[3][i], t[i][3] = "", ""
t[3][3] = "X"
plateau = t

blanc = 9 #compteurs de pions dans la main du joueur
noir = 9
phase1 = True
phase2 = False
phase3 = False
joueur = "noir"


def change_joueur(joueur):
    '''
    Change le joueur
    '''
    if joueur == "noir":
        return "blanc"
    else:
        return "noir"


def jouer_coup(plateau, coord, joueur):
    plateau[coord[0]][coord[1]] = joueur


def cases_libres(plateau, joueur):
    '''
    Renvoie la liste des places libres
    '''
    places_libres = []
    for i in range(len(plateau)-1):
        for j in range(len(plateau[i])-1):
            if est_libre((i,j), plateau, joueur) == True:
                places_libres.append((i,j))
    return places_libres


def est_libre(plateau, coord):
    '''
    Vérifie si la case est libre ou non
    '''
    if plateau[coord[0]][coord[1]] == "":
        return True
    else:
        return False


def deplacement_possible(plateau, pion, case):
    '''
    Fonction qui renvoie si le déplacement est réalisable ou pas
    '''
    if pion == case:
        return False
    elif not pion[0] == case[0] and not pion[1] == case[1]:
        return False
    elif pion[0] == case[0]:
        i = pion[0]
        if pion[0] < case[0]:
            for j in range(pion[1], case[1]):
                if plateau[i][j] == "":
                   return False
        else:
            for j in range(case[1], pion[1]):
               if plateau[i][j] == "":
                   return False
    elif pion[1] == case[1]:
        j = pion[1]
        if pion[1] < case[1]:
            for i in range(pion[0], case[0]):
                if plateau[i][j] == "":
                   return False
        else:
            for j in range(case[0], pion[0]):
               if plateau[i][j] == "":
                   return False
    return True
        
while phase1:
#Décide de quel joueur joue
    joueur = change_joueur(joueur)
    print(joueur)
#Le joueur joue un coup
    case_libre = False
    while not case_libre:
        print("Le joueur", joueur, "doit choisir une case :")
        x = int(input())
        y = int(input())
        coord = (x, y)
        case_libre = est_libre(plateau, coord)
    jouer_coup(plateau, coord, joueur)
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
    coup_possible = False
    while not coup_possible:
        print("Le joueur", joueur, "doit choisir une case :")
        x = int(input())
        y = int(input())
        coord = (x, y)
        coup_possible = deplacement_possible(plateau, coord)
    jouer_coup(plateau, coord, joueur)
    for i in range (len(plateau)):
        print(plateau(i))


while phase3:
    if blanc == 2:
        print("Le joueur noir a gagné.")
        break
    elif noir == 2:
        print("Le joueur blanc a gagné.")
        break
