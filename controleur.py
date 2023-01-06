from vue import*
from modele import*
import time

### INITIALISATION DU MODELE ###
nb_jetons = 9
#Création du plateau
plateau = cree_plateau_9j()

#Définition des voisines et des alignements possibles de chaque case
for i in range (len(plateau)):
    for j in range(len(plateau)):
        case = plateau[i][j]
        if case.couleur == "":
            case.voisines = vois_hor(plateau, i, j) + vois_vert(plateau, i, j)
            case.alignements[0] = ligne_aligne(plateau, i, j)
            case.alignements[1] = col_aligne(plateau, i, j)
            if nb_jetons == 12:
                case.alignements[2], case.alignements[3] = diag_aligne(plateau, i, j)

cree_fenetre(largeur, hauteur)
image(largeur/2, hauteur/2, "fond1.gif", ancrage="center")
j1 = "black"
j2 = "white"
joueur = j1
nb_pion_main = {j1: nb_jetons, j2: nb_jetons}
nb_pion_plat = {j1: 0, j2: 0}

#dessine_plateau_9j()

affiche_case(plateau)
phase1 = True
phase2 = False
phase3 = {j1: False, j2: False}
deplacement = False
saut = False
retire = False
game = False
menu = True

#Affichage du menu
boutons = {"Jouer": [(largeur/2 - a, hauteur/2 - a/4), (largeur/2 + a, hauteur/2 + a/4)],
           "Quitter": [(largeur/2 - a, hauteur/2 + a/2), (largeur/2 + a, hauteur/2 + a)]}
rectangle(largeur/2 - a, hauteur/2 - a/4, largeur/2 + a, hauteur/2 + a/4, epaisseur=5, tag="Jouer", remplissage='red')
rectangle(largeur/2 - a, hauteur/2 + a/2, largeur/2 + a, hauteur/2 + a, epaisseur=5, tag="Quitter", remplissage='blue')

debut = time.time() #compte le temps

while menu:
    frametime = time.time()
    ev = donne_ev()
    tev = type_ev(ev)
    if tev == "ClicGauche":
        if touche_rectangle(boutons["Jouer"]):
            efface("Jouer")
            efface("Quitter")
            dessine_plateau_9j()
            affiche_case(plateau)
            game = True
            while game:
                ev = attend_ev()
                tev = type_ev(ev)

                if tev == "Quitte":
                    running = False
                    break 

                if tev == "ClicGauche":
                    case = donne_case(plateau)
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
                                    if phase2:
                                        if nb_pion_plat[joueur] == 3:
                                            phase3[joueur] = True
                                        elif nb_pion_plat[joueur] < 3:
                                            game = False
                                            break

                        #Le joueur doit placer un pion
                        elif phase1:
                            print("dans phase1")
                            #Renvoie si la souris se trouve sur une case du plateau
                            if case.est_vide():
                                case.place(joueur)
                                dessine_pion(case)
                                nb_pion_main[joueur] -= 1
                                nb_pion_plat[joueur] +=1
                                #Si un moulin est formé, le joueur doit retirer un pion
                                liste_aligne = detect_moulin(case)
                                if liste_aligne != []:
                                    case.moulin = True
                                    dessine_moulin(case)
                                    for alignement in liste_aligne:
                                        for case_aligne in alignement:
                                            case_aligne.moulin = True
                                            dessine_moulin(case_aligne)
                                    retire = True
                                else:
                                    joueur = joueur_adv(joueur, j1, j2)
                            #Détecte quand chaque joueur a joué la totalité de ses pions
                            if phase1 and nb_pion_main[j1] == 0 and nb_pion_main[j2] == 0:
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
                                dessine_pion(dest)
                                deplacement = False
                                saut = False
                                #Supprime l'ancien marquage
                                if liste_aligne_dep != []:
                                    efface_moulin(depart)
                                    for alignement in liste_aligne_dep:
                                        for case_aligne in alignement:
                                            if detect_moulin(case_aligne) == []:
                                                case_aligne.moulin = False #La case n'est plus alignée
                                                efface_moulin(case_aligne)
                                #Marque les cases si alignement
                                if liste_aligne_dest != []:
                                    retire = True
                                    dest.moulin = True
                                    dessine_moulin(dest)
                                    for alignement in liste_aligne_dest:
                                        for case_aligne in alignement:
                                            case_aligne.moulin = True #Marque la case comme alignée
                                            dessine_moulin(case_aligne)
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
                                dessine_liste_cases(cases_vides(plateau))

                        #Le joueur sélectionne un pion à déplacer
                        elif phase2:
                            print("dans phase2")
                            depart = case
                            if depart.couleur == joueur:
                                deplacement = True
                                for case in depart.voisines:
                                    if case.couleur == "":
                                        dessine_liste_cases([case])
    #FPS
    elapsed_time = time.time() - frametime
    if elapsed_time < 1.0/60:
        time.sleep(1.0 / 90 - elapsed_time)

print("Le joueur", joueur_adv(joueur, j1, j2), "a gagné!")
ferme_fenetre()
