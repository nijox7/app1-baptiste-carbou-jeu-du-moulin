from fltk import*
from Case import*

largeur, hauteur = 900, 900
moyenne = (largeur + hauteur) / 2 #Moyenne qui permet d'ajuster la taille du quadrillage
a = 0.25 * moyenne #Distance du centre au bord de la grille


def cree_plateau():
    ''' Renvoie un plateau vide de la variante à 9 jetons '''
    t = [[Case(i, j, "X") for j in range(7)] for i in range(7)]
    for i in range(7):
        t[i][i], t[i][6-i] = Case(i, i, ""), Case(i, 6-i, "")
        t[3][i], t[i][3] = Case(3, i, ""), Case(i, 3, "")
    t[3][3] = Case(3, 3, "Centre")
    return t


def dessine_plateau():
    ''' Dessine un plateau pour 9 jetons '''

    rectangle(largeur/2 - a, hauteur/2 - a,
              largeur/2 + a, hauteur/2 + a, epaisseur=5)
    rectangle(largeur/2 - a * 2/3, hauteur/2 - a * 2/3,
              largeur/2 + a * 2/3, hauteur/2 + a * 2/3,
              epaisseur=5)
    rectangle(largeur/2 - a * 1/3, hauteur/2 - a * 1/3,
              largeur/2 + a * 1/3, hauteur/2 + a * 1/3,
              epaisseur=5)
    ligne(largeur/2 - a, hauteur/2, largeur/2 - a * 1/3, hauteur/2,
          epaisseur=5)
    ligne(largeur/2 + a, hauteur/2, largeur/2 + a * 1/3, hauteur/2,
          epaisseur=5)
    ligne(largeur/2, hauteur/2 - a, largeur/2, hauteur/2 - a * 1/3,
          epaisseur=5)
    ligne(largeur/2, hauteur/2 + a, largeur/2, hauteur/2 + a * 1/3,
          epaisseur=5)


def dessine_pion(plateau, case):
    ''' Dessine un pion sur une case '''
    nom = str(case.x)+str(case.y)
    cercle(largeur/2 - a + case.y * (a/3),  hauteur/2 - a + case.x * (a/3),
           moyenne * 0.02, remplissage = case.couleur, couleur = case.couleur,
           tag="pion"+str(case.x)+str(case.y), epaisseur=2)


def efface_pion(plateau, case):
    ''' Efface le pion d'une casse '''
    efface("pion" + str(case.x) + str(case.y))


def distance (x, y):
    ''' Calcul la distance de la souris au point '''
    return (abs(ordonnee_souris() - x) ** 2 + abs(abscisse_souris() - y) ** 2) ** (1/2)


def donne_case(plateau):
    ''' Renvoie la case sur laquelle se trouve la souris, sinon None '''
    for i in range(7):
        for j in range(7):
            x = largeur/2 - a + i * (a/3)
            y = hauteur/2 - a + j * (a/3)
            if distance(x, y) <= moyenne * 0.02:
                return plateau[i][j]


def affiche_liste_case(plateau, liste):
    ''' Affiche une liste de case '''
    for case in liste:
        cercle(largeur/2 - a + case.x * (a/3), hauteur/2 - a + case.y * (a/3),
               moyenne * 0.02, couleur="red", tag="case_possible")

