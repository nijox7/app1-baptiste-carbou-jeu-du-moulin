from vue import*

cree_fenetre(largeur, hauteur)
#image(largeur/2, hauteur/2, "fond1.gif", ancrage="center")
dessine_plateau()
affiche_case()
j1 = "black"
j2 = "white"
joueur = "black"
compteur = {j1: nb_jetons, j2: nb_jetons}
running = True
phase1 = True
phase2 = False
phase3_j1 = False
phase3_j2 = False
deplacement = False
retire = False

while True: 
    ev = attend_ev()
    tev = type_ev(ev)

    if tev == "Quitte":
        running = False
        break 

    if tev == "ClicGauche":
        
        #Le joueur retire un pion après la formation d'un moulin
        if retire:
            print("dans retire")
            case = donne_case()
            if case and case.couleur == joueur_adv(joueur) and case.moulin == False:
                case.retire()
                efface_pion(case)
                retire = False
                joueur = joueur_adv(joueur)

        #Le joueur doit placer un pion
        elif phase1:
            print("dans phase 1")
            #Renvoie si la souris se trouve sur une case du plateau
            case = donne_case()
            if case and case.est_vide():
                case.place(joueur)
                dessine_pion(case)
                compteur[joueur] -= 1
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
                    joueur = joueur_adv(joueur)
            #Détecte quand chaque joueur a joué la totalité de ses pions
            if phase1 and compteur["black"] == 0 and compteur["white"] == 0:
                phase1 = False
                phase2 = True

        #Le joueur choisit où déplacer son pion
        elif deplacement:
            print("se déplace")
            #Le joueur sélectionne sa destination
            dest = donne_case()
            if dest and peut_deplacer(depart, dest):
                liste_aligne_dep = detect_moulin(depart)
                deplace(depart, dest, joueur)
                liste_aligne_dest = detect_moulin(dest)
                efface_pion(depart)
                efface("case_possible")
                dessine_pion(dest)
                deplacement = False
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
                    joueur = joueur_adv(joueur)
            else:
                deplacement = False
            efface("case_possible")
            #Met fin au jeu si un des joueur gagne
            if phase2 and (compteur["black"] == 7 or compteur["white"] == 7):
                running = False
                break

        #Le joueur sélectionne un pion à déplacer
        elif phase2:
            print("dans phase 2")
            depart = donne_case()
            if depart and depart.couleur == joueur:
                deplacement = True
                for case in depart.voisines:
                    if case.couleur == "":
                        dessine_liste_cases([case])
ferme_fenetre()
