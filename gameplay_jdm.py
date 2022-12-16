class Case:

    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.moulin = False

    def voisines(self, plateau):
        ''' Renvoie la liste des cases adjacentes rectilignes '''
        liste = []
        x, y = self.x, self.y
        #Parcours latéral
        for j in range(y-1, -1, -1):
            if plateau[x][j].couleur != "X":
                liste.append((plateau[x][j]))
                break
        for j in range(y + 1, len(plateau[x])):
            if plateau[x][j].couleur != "X":
                liste.append(plateau[x][j])
                break
        #Parcours en hauteur
        for i in range(x - 1, -1, -1):
            if plateau[i][y].couleur != "X":
                liste.append(plateau[i][y])
                break
        for i in range(x + 1, len(plateau)):
            if plateau[i][y].couleur != "X":
                liste.append(plateau[i][y])
                break

        return liste


def cree_plateau():
    ''' Renvoie un plateau vide de la variante à 9 jetons '''
    t = [[Case(i, j, "X") for j in range(7)] for i in range(7)]
    for i in range(7):
        t[i][i], t[i][6-i] = Case(i, i, ""), Case(i, 6-i, "")
        t[3][i], t[i][3] = Case(3, i, ""), Case(i, 3, "")
    t[3][3] = Case(3, 3, "Centre")
    return t


def place(case, joueur):
    ''' Place un pion sur la case demandée '''
    case.couleur = joueur


def retire(case):
    ''' Retire un pion '''
    case.couleur = ""


def deplace(case1, case2, joueur):
    ''' Déplace un pion '''
    retire(case1)
    place(case2, joueur)


def change_joueur(joueur):
    ''' Change le joueur '''
    if joueur == "black":
        return "white"
    else:
        return "black"


def cases_libres(plateau):
    ''' Renvoie la liste des cases libres d'un plateau '''
    cases_libres = []

    for i in range(len(plateau)-1):
        for j in range(len(plateau[i])-1):
            if est_libre(plateau, (i,j)) == True:
                cases_libres.append(plateau[i][j])
    return cases_libres


def est_libre(case):
    ''' Vérifie que la case est libre '''

    if case.couleur == "":
        return True
    else:
        return False


def deplacement_possible(case1, case2):
    ''' Vérifie que le déplacement voulu soit possible '''
    if case2 != "":
        return False
    elif case2 not in case1.voisines():
        return False
    return True


def occurence_e(liste, element):
    compteur = 0
    for e in liste:
        if e == element:
            compteur += 1
    if compteur > 1:
        return True


def occurrence(liste):
    for element in liste:
        if occurence_e(liste, element):
            return True


def donne_moulin(case, joueur):
    '''
    Renvoie si la case est au centre d'un moulin,
    la liste des cases intégrées au moulin.
    Si plusieurs moulins sont mis en jeu, la fonction
    renvoie les cases de tous les moulins.
    Si la case n'est pas au centre d'un moulin, renvoie None
    '''
    
    liste = []
    lx = []
    ly = []
    for voisine in case.voisines():
        if voisine.couleur == joueur:
            lx.append(voisine.x)
            ly.append(voisine.y)
    occ_x, occ_y = occurrence(lx), occurrence(ly)
    if occ_x:
        liste.append(plateau[case.x][case.y -1], case, plateau[case.x][case.y + 1])
    if occ_y:
        liste.append(plateau[case.x - 1][case.y], case, plateau[case.x + 1][case.y])
    return liste


def forme_moulin(moulin):
    ''' Forme un moulin '''
    for case in moulin:
        case.moulin = True


def suppr_moulin(moulin):
    ''' Supprime un moulin '''
    for case in moulin:
        case.moulin = False


def peut_retirer(case):
    if case.moulin == False:
        return True
    return False
