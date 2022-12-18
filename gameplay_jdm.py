class Case:
    ''' Définit une case d'un plateau'''
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
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

    def voisines(self):
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



def deplace(dep, dest, joueur):
    ''' Déplace un pion '''
    dep.retire()
    dest.place(joueur)


def change_joueur(joueur):
    ''' Change le joueur '''
    if joueur == "black":
        return "white"
    else:
        return "black"


def est_libre(case):
    ''' Vérifie que la case est libre '''

    if case.couleur == "":
        return True
    else:
        return False


def cases_libres(plateau):
    ''' Renvoie la liste des cases libres d'un plateau '''
    cases_libres = []

    for i in range(len(plateau)-1):
        for j in range(len(plateau[i])-1):
            if plateau[i][j].est_vide() == True:
                cases_libres.append(plateau[i][j])
    return cases_libres


def donne_voisines(plateau, x, y):
        ''' Renvoie la liste des cases adjacentes rectilignes '''
        liste = []
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


def peut_deplacer(dep, dest):
    ''' Vérifie que le déplacement voulu soit possible '''
    if dest.couleur == "" and dest in dep.voisines():
        return True
    return False


def occurence_e(liste, element):
    compteur = 0
    for e in liste:
        if e == element:
            compteur += 1
    return compteur > 1


def occurrence(liste):
    for element in liste:
        if occurence_e(liste, element):
            return True
    return False


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
    for voisine in voisines[str(case.x)+str(case.y)]:
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


### INITIALISATION DU MODELE ###

#Création du plateau
plateau = cree_plateau()
#Définition des voisines de chaque case
voisines = {"00":[], "03":[], "06":[], "10":[], "11":[],
            "13":[], "15":[], "22":[], "23":[], "24":[],
            "30":[], "31":[], "32":[], "34":[], "35":[],
            "36":[], "42":[], "43":[], "44":[], "51":[],
            "53":[], "55":[], "60":[], "63":[], "66":[], }
for i in range(7):
    for j in range(7):
        voisines[str(i)+str(j)] = donne_voisines(plateau, i, j)
#Définit le nombre de jetons
nb_jetons = 3
