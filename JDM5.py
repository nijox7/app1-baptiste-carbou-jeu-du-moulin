from affiche_jdm import*
from gameplay_jdm import*

plateau = cree_plateau()
cree_fenetre(hauteur, largeur)
dessine_plateau()
joueur = "black"
noir, blanc = 9, 9
running, phase1 = True, True
phase2 = False

while True:
    if phase1:
        while True:
            ev = attend_ev()
            tev = type_ev(ev) 

            if tev == "Quitte":
                ferme_fenetre()
                running = False
                break
            elif tev == "ClicGauche":
                case = donne_case(plateau)
                if case and est_libre(case):
                    place_pion(case, joueur)
                    dessine_pion(plateau, case)
                    if joueur == "black":
                        noir -= 1
                    else:
                        blanc -= 1

    elif phase2:
        while True:
            ev = attend_ev()
            tev = type_ev(ev)
            if tev == "Quitte":
                ferme_fenetre()
                running = False
                break
            elif tev == "ClicGauche":
                case = donne_case(plateau)
                if case and 
        

    #CHANGEMENT DE PHASE
    if phase1 and noir == 0 and blanc == 0:
        phase1 = False
        phase2 = False

    joueur = change_joueur(joueur)
    mise_a_jour()

