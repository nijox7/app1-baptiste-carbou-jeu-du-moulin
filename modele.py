class Case:
    ''' Définit une case d'un plateau'''
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.voisines = ""
        self.alignements = [[],[],[],[]] # horizontal, vertical, oblique gauche, oblique droite
        self.couleur = couleur
        self.moulin = False

    def est_vide(self):
        ''' Renvoie si la case est vide'''
        if self.couleur == "":
            return True
        return False

    def place(self, joueur):
        '''Place un pion sur la case'''
        self.couleur = joueur

    def retire(self):
        '''Retire un pion de la case'''
        self.couleur = ""
        self.moulin = False


def cree_plateau():
    ''' Renvoie un plateau vide de la variante à 9 jetons '''
    t = [[Case(i, j, "X") for j in range(7)] for i in range(7)]
    for i in range(7):
        t[i][i] = Case(i, i, "")
        t[i][6-i] = Case(i, 6-i, "")
        t[3][i] = Case(3, i, "")
        t[i][3] = Case(i, 3, "")
    t[3][3] = Case(3, 3, "Centre")
    return t


def deplace(dep, dest, joueur):
    ''' Déplace un pion '''
    liste_moulin = detect_moulin(dep)
    dep.retire()
    if liste_moulin != []:
        for moulin in liste_moulin:
            for case in moulin:
                moulin2 = detect_moulin(case)
                if moulin2 is None:
                    case.moulin = False
    dest.place(joueur)


def joueur_adv(joueur):
    ''' Renvoie le joueur adverse '''
    if joueur == "black":
        return "white"
    else:
        return "black"


def peut_deplacer(dep, dest):
    ''' Vérifie que le déplacement voulu soit possible '''
    if dest.couleur == "" and dest in dep.voisines:
        return True
    return False


def cases_vides():
    ''' Renvoie toutes les cases libre du plateau '''
    cases_vides = []
    for i in range(len(plateau)-1):
        for j in range(len(plateau[i])-1):
            if plateau[i][j].est_vide() == True:
                cases_vides.append(plateau[i][j])
    return cases_vides


def vois_vert(plateau, x, y):
    ''' Renvoie la liste des cases voisines verticales '''
    liste = []
    long = len(plateau)
    for i in range(x-1, -1, -1):
        if plateau[i][y].couleur != "X":
            liste.append(plateau[i][y])
            break
    for i in range(x+1, long):
        if plateau[i][y].couleur != "X":
            liste.append(plateau[i][y])
            break
    return liste


def vois_hor(plateau, x, y):
    ''' Renvoie la liste des cases voisines horizontales '''
    liste = []
    long = len(plateau)
    for j in range(y-1, -1, -1):
        if plateau[x][j].couleur != "X":
            liste.append(plateau[x][j])
            break
    for j in range(y+1, long):
        if plateau[x][j].couleur != "X":
            liste.append(plateau[x][j])
            break
    return liste


def vois_obl(plateau, x, y):
    ''' Renvoie la liste des cases voisines obliques '''
    liste = []
    long = len(plateau)
    #Parcours oblique \
    if x == y:
        for k in range(x-1, -1, -1):
            if plateau[k][k].couleur != "X":
                liste.append(plateau[k][k])
                break
        for k in range(x+1, long):
            if plateau[k][k].couleur != "X":
                liste.append(plateau[k][k])
                break
    #Parcours oblique /
    if x + y == long - 1:
        for k in range(x-1, -1, -1):
            if plateau[k][long-1-k] != "X":
                liste.append(plateau[k][long-1-k])
                break
        for k in range(x+1, long):
            if plateau[k][long-1-k] != "X":
                liste.append(plateau[k][long-1-k])
                break
    return liste


def ligne_aligne(plateau, x, y):
    ''' Renvoie l'alignement de la ligne '''
    liste = []
    for j in range(y-1, -1, -1):
        case = plateau[x][j]
        if case.couleur == "":
            liste.append(plateau[x][j])
        elif case.couleur == "Centre":
            break
    for j in range(y+1, len(plateau)):
        case = plateau[x][j]
        if case.couleur == "":
            liste.append(case)
        elif case.couleur == "Centre":
            break
    return liste


def col_aligne(plateau, x, y):
    ''' Renvoie l'alignement de la colonne '''
    liste = []
    for i in range(x-1, -1, -1):
        case = plateau[i][y]
        if case.couleur == "":
            liste.append(case)
        elif case.couleur == "Centre":
            break  
    for i in range(x+1, len(plateau)):
        case = plateau[i][y]
        if case.couleur == "":
            liste.append(case)
        elif case.couleur == "Centre":
            break
    return liste

def diag_aligne(plateau, x, y):
    ''' Renvoie l'alignement des diagonales '''
    liste1 = []
    long = len(plateau)
    #Parcours oblique \
    if x == y:
        for k in range(x-1, -1, -1):
            case = plateau[k][k]
            if case.couleur == "Centre":
                break
            elif case.couleur != "X":
                liste1.append(plateau[k][k])
        for k in range(x+1, long):
            case = plateau[k][k]
            if case.couleur == "Centre":
                break
            elif case.couleur != "X":
                liste1.append(plateau[k][k])

    #Parcours oblique /
    liste2 = []
    if x + y == long - 1:
        for k in range(x-1, -1, -1):
            case = plateau[k][long-1-k]
            if case.couleur == "Centre":
                break
            elif case.couleur != "X":
                liste2.append(case)
        for k in range(x+1, long):
            case = plateau[k][long-1-k]
            if case.couleur == "Centre":
                break
            elif case.couleur != "X":
                liste2.append(case)
    return liste1, liste2


def detect_moulin(case):
    ''' Détecte et renvoie la liste des alignements '''
    liste = []
    #Parcours tous les alignements possibles à la case
    for alignement in case.alignements:
        moulin = True
        for case_a in alignement:
            #Si la case ne correspond pas, alors pas d'alignement
            if case_a.couleur != case.couleur:
                moulin = False
                break
        if moulin == True and alignement != []:
            liste.append(alignement)
    return liste


### INITIALISATION DU MODELE ###

#Définit le nombre de jetons
nb_jetons = 9

#Création du plateau
plateau = cree_plateau()

#Définition des voisines et des alignements possibles de chaque case
for i in range (7):
    for j in range(7):
        case = plateau[i][j]
        if case.couleur == "":
            case.voisines = vois_hor(plateau, i, j) + vois_vert(plateau, i, j)
            case.alignements[0] = ligne_aligne(plateau, i, j)
            case.alignements[1] = col_aligne(plateau, i, j)
            case.alignements[2], case.alignements[3] = diag_aligne(plateau, i, j)