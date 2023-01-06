from vue import*
from modele import*
import time

cree_fenetre(largeur, hauteur)
image(largeur/2, hauteur/2, "fond1.gif", ancrage="center")
### INITIALISATION DU MODELE ###
nb_jetons = 6
if nb_jetons == 12:
    plateau = cree_plateau_9j()
    dessine_plateau_12j()
    coeff = 1
elif nb_jetons == 9:
    plateau = cree_plateau_9j()
    dessine_plateau_9j()
    coeff = 1
elif nb_jetons == 6:
    plateau = cree_plateau_6j()
    dessine_plateau_6j()
    coeff = 2/3
elif nb_jetons == 3:
    plateau = cree_plateau_3j()
    dessine_plateau_3j()
    coeff = 1/3

#Définition des voisines et des alignements possibles de chaque case
for i in range (len(plateau)):
    for j in range(len(plateau)):
        print(i,j)
        case = plateau[i][j]
        if case.couleur == "":
            case.voisines = vois_hor(plateau, i, j) + vois_vert(plateau, i, j)
            case.alignements[0] = ligne_aligne(plateau, i, j)
            case.alignements[1] = col_aligne(plateau, i, j)
            if nb_jetons == 12 or nb_jetons == 3:
                case.alignements[2], case.alignements[3] = diag_aligne(plateau, i, j)
                case.voisines += vois_obl(plateau, i, j)
            for k in range (len(case.alignements)):
                if len(case.alignements[k]) != 2 :
                    case.alignements[k] = []
affiche_case(plateau, coeff)

j1 = "black"
j2 = "white"
joueur = j1
nb_pion_main = {j1: nb_jetons, j2: nb_jetons}
nb_pion_plat = {j1: 0, j2: 0}
phase1 = True
phase2 = False
phase3 = {j1: False, j2: False}
deplacement = False
saut = False
retire = False


while True:
    ev = attend_ev()
    tev = type_ev(ev)
    if tev == "Quitte":
        running = False
        break 

    if tev == "ClicGauche":
        case = donne_case(plateau, coeff)
        if case:
        #Le joueur retire un pion après la formation d'un moulin
            if retire:
                print("dans retire")
                #vérifie que le joueur peut retirer le pion
                if case.couleur == joueur_adv(joueur, j1, j2):
                    if (case.moulin == False or phase3[joueur_adv(joueur, j1, j2)]):
                        case.retire()
                        nb_pion_plat[joueur_adv(joueur, j1, j2)] -= 1
                        efface_pion(case)
                        retire = False
                        joueur = joueur_adv(joueur, j1, j2)
                        if phase2 and nb_pion_plat[joueur] == 3:
                            phase3[joueur] = True
                        elif nb_pion_plat[joueur] + nb_pion_main[joueur] < 3: #Vérifie si le joueur a perdu
                            print("Le joueur", joueur_adv(joueur, j1, j2), "a gagné!")
                            break

            #Le joueur doit placer un pion
            elif phase1:
                print("dans phase1")
                #Renvoie si la souris se trouve sur une case du plateau
                if case.est_vide():
                    case.place(joueur)
                    dessine_pion(case, coeff)
                    nb_pion_main[joueur] -= 1
                    nb_pion_plat[joueur] +=1
                    #Formation d'un moulin
                    liste_aligne = detect_moulin(case)
                    if liste_aligne != []:
                        case.moulin = True
                        dessine_moulin(case, coeff)
                        for alignement in liste_aligne:
                            for case_aligne in alignement:
                                case_aligne.moulin = True
                                dessine_moulin(case_aligne, coeff)
                                retire = True
                    else:
                        joueur = joueur_adv(joueur, j1, j2)
                        #Détecte quand chaque joueur a joué la totalité de ses pions
                        if phase1 and nb_pion_main[j1] == 0 and nb_pion_main[j2] == 0:
                            if nb_pion_plat[j1] + nb_pion_plat[j2] == 24:
                                print("MATCH NUL")
                                break
                            phase1 = False
                            phase2 = True

            #Le joueur choisit où déplacer son pion
            elif deplacement or saut:
                print("en déplacement ou saut")
                #Le joueur sélectionne sa destination
                dest = case
                if (saut and case.couleur == "") or peut_deplacer(depart, dest):
                    liste_aligne_dep = detect_moulin(depart) #liste des cases alignées à la case de départ
                    deplace(depart, dest, joueur)
                    liste_aligne_dest = detect_moulin(dest) #liste des cases alignées à la case de destination
                    efface_pion(depart)
                    efface("case_possible")
                    dessine_pion(dest, coeff)
                    deplacement = False
                    saut = False
                    #Supprime un moulin
                    if liste_aligne_dep != []:
                        efface_moulin(depart)
                        for alignement in liste_aligne_dep:
                            for case_aligne in alignement:
                                if detect_moulin(case_aligne) == []:
                                    case_aligne.moulin = False #La case n'est plus alignée
                                    efface_moulin(case_aligne)
                    #Formation d'un moulin
                    if liste_aligne_dest != []:
                        retire = True
                        dest.moulin = True
                        dessine_moulin(dest, coeff)
                        for alignement in liste_aligne_dest:
                            for case_aligne in alignement:
                                case_aligne.moulin = True #Marque la case comme alignée
                                dessine_moulin(case_aligne, coeff)
                    else:
                        joueur = joueur_adv(joueur, j1, j2)
                else:
                    deplacement = False
                    saut = False
                    efface("case_possible")           

            elif phase3[joueur] == True:
                print("dans phase3")
                depart = case
                if depart.couleur == joueur:
                    saut = True
                    dessine_liste_cases(cases_vides(plateau), coeff)

            #Le joueur sélectionne un pion à déplacer
            elif phase2:
                print("dans phase2")
                depart = case
                if depart.couleur == joueur:
                    deplacement = True
                    for case in depart.voisines:
                        if case.couleur == "":
                            dessine_liste_cases([case], coeff)

ferme_fenetre()

