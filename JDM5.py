from affiche_jdm import*
from gameplay_jdm import*

cree_fenetre(largeur, hauteur)
dessine_plateau()
joueur = "black"
compteur = {"black": nb_jetons, "white": nb_jetons}
running = True
phase1 = True
phase2 = False
deplacement = False

while True: 
    ev = attend_ev()
    tev = type_ev(ev)

    if tev == "Quitte":
        running = False
        break 

    if tev == "ClicGauche":
        if phase1:
            case = donne_case(plateau) #renvoie la case sur laquelle se trouve la souris
            if case and case.est_vide():
                case.place(joueur)
                dessine_pion(case)
                compteur[joueur] -= 1
                joueur = change_joueur(joueur)
            if phase1 and compteur["black"] == 0 and compteur["white"] == 0:
                phase1 = False
                phase2 = True

        elif deplacement:
            #Le joueur sélectionne sa destination
            dest = donne_case(plateau)
            if dest and peut_deplacer(depart, dest):
                deplace(depart, dest, joueur)
                efface_pion(depart)
                efface("case_possible")
                dessine_pion(dest)
                deplacement = False
                joueur = change_joueur(joueur)
            else:
                deplacement = False
            efface("case_possible")
            #Met fin au jeu si un des joueur gagne
            if phase2 and (compteur["black"] == 7 or compteur["white"] == 7): 
                running = False
                break 

        elif phase2:
            #Le joueur sélectionne le pion qu'il veut jouer
            depart = donne_case(plateau)
            if depart and depart.couleur == joueur:
                deplacement = True
                dessine_liste_cases(depart.voisines())


ferme_fenetre()
