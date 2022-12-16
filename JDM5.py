from affiche_jdm import*
from gameplay_jdm import*

plateau = cree_plateau()
cree_fenetre(hauteur, largeur)
dessine_plateau()
joueur = "black"
compteur = {"black": 9, "white": 9}
running, phase1 = True, True
phase2, deplacement = False, False

while True: 
    ev = attend_ev()
    tev = type_ev(ev)

    if tev == "Quitte":
        running = False
        break 

    elif phase1 and tev == "ClicGauche":
        case = donne_case(plateau) #renvoie la case sur laquelle se trouve la souris
        if case and est_libre(case):
            place(case, joueur)
            dessine_pion(plateau, case)
            compteur[joueur] -= 1
            joueur = change_joueur(joueur)

    elif deplacement == True and tev == "ClicGauche":
        case_visee = donne_case(plateau)
        if case_visee and case_visee in case_select.voisines(plateau):
            deplace(case_select, case_visee, joueur)
            efface_pion(plateau, case_select)
            dessine_pion(plateau, case_visee)
            efface("case_possible")
            deplacement = False
            joueur = change_joueur(joueur)
        
    elif phase2 and tev == "ClicGauche":
        case_select = donne_case(plateau)
        if case_select and case_select.couleur == joueur:
            deplacement = True
            affiche_liste_case(plateau, case_select.voisines(plateau))

    #CHANGEMENT DE PHASE
    if phase1 and compteur["black"] == 0 and compteur["white"] == 0:
        phase1 = False
        phase2 = True
    elif phase2 and (compteur["black"] == 7 or compteur["white"] == 7):
        print("Le joueur", joueur, " a gagné!!")
        break
    mise_a_jour()

ferme_fenetre()
