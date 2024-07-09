

# **Projet IA02**

  

Ines ABBACHE

  
Bartlomiej GRZADZIEL

  
  

## **1. La modélisation en SAT de la phase 1**

### **Variable :**

  

- $I_{i,j}$ représente un Invité à la position (i,j),

- $G_{i,j}$ représente un Garde à la position (i,j),

- $Cor_{i,j}$ représente une Corde à la position (i,j),

- $Cos_{i,j}$ représente un Costume à la position (i,j),

- $M_{i,j}$ représente un Mur à la position (i,j),

- $V_{i,j}$ représente un case Vide à la position (i,j),

- $N_{i,j}$ La personne en (i,j) regarde vers le Nord ,

- $S_{i,j}$ La personne en (i,j) regarde vers le Sud ,

- $Est_{i,j}$ La personne en (i,j) regarde vers l'Est ,

- $O_{i,j}$ La personne en (i,j) regarde vers l'Ouest ,

- $Ent_{i,j}$ représente une Entité à la position (i,j)

- $Personne_{i,j}$ représente une Personne à la position (i,j),



### **Règles :**

  

- Règle 1 : Existence et unicité d'élément sur une case (i,j) : une personne, un objet , vide ou bien un mur

  

  + $I_{i,j} \leftrightarrow \neg G_{i,j} \land \neg Cib_{i,j} \land \neg Cor_{i,j}\land \neg Cos_{i,j}\land \neg M_{i,j} \land \neg V_{i,j}$

    

  + $G_{i,j} \leftrightarrow \neg I_{i,j} \land \neg Cib_{i,j} \land \neg Cor_{i,j}\land \neg Cos_{i,j}\land \neg M_{i,j} \land \neg V_{i,j}$


    

  + $Cor_{i,j} \leftrightarrow \neg I_{i,j} \land \neg G_{i,j} \land \neg Cib_{i,j}\land \neg Cos_{i,j}\land \neg M_{i,j} \land \neg V_{i,j}$

    

  + $Cos_{i,j} \leftrightarrow \neg I_{i,j} \land \neg G_{i,j} \land \neg Cib_{i,j}\land \neg Cor_{i,j}\land \neg M_{i,j} \land \neg V_{i,j}$

    

  + $M_{i,j} \leftrightarrow \neg I_{i,j} \land \neg G_{i,j} \land \neg Cib_{i,j}\land \neg Cor_{i,j}\land \neg Cos_{i,j} \land \neg V_{i,j}$

    

  + $V_{i,j} \leftrightarrow \neg I_{i,j} \land \neg G_{i,j} \land \neg Cib_{i,j}\land \neg Cor_{i,j}\land \neg Cos_{i,j} \land \neg M_{i,j}$

  

- Règle 2 : Existence et unicité de direction par personne sur une case(i,j) soit : Nord, Sud, Est ou Ouest

  + $N_{i,j} \leftrightarrow \neg S_{i,j} \land \neg Est_{i,j} \land \neg O_{i,j}$

    

  + $S_{i,j} \leftrightarrow \neg N_{i,j} \land \neg Est_{i,j} \land \neg O_{i,j}$

    

  + $E_{i,j} \leftrightarrow \neg N_{i,j} \land \neg S_{i,j} \land \neg O_{i,j}$

    

  + $O_{i,j} \leftrightarrow \neg N_{i,j} \land \neg S_{i,j} \land \neg Est_{i,j}$

    

  + $I_{i,j} \rightarrow N_{i,j} \lor Est_{i,j} \lor O_{i,j} \lor O_{i,j}$

    

  + $G_{i,j} \rightarrow N_{i,j} \lor S_{i,j} \lor Est_{i,j} \lor O_{i,j}$

  

- Règle 3 : Existence et unicité du costume, de la corde et de la cible

  

  + $Cos_{i,j} \leftrightarrow ( \land  \neg Cos_{k,l} ) avec (k,l) \neq (i,j)$  

  	$(k,l) \in  \llbracket  0,n-1\rrbracket* \llbracket0,n-1\rrbracket$

    

  + $Cor_{i,j} \leftrightarrow ( \land \neg Cor_{k,l} ) avec (k,l) \neq (i,j)$

  	$(k,l) \in  \llbracket  0,n-1\rrbracket* \llbracket0,n-1\rrbracket$

    

  + $Cib_{i,j} \leftrightarrow ( \land \neg Cib_{k,l} ) avec (k,l) \neq (i,j)$

  	$(k,l) \in  \llbracket  0,n-1\rrbracket* \llbracket0,n-1\rrbracket$


  
  

## **2. Programme en Python phase 1**

**Structures des données:**

Nous avons créé des alias de type afin de faciliter la compréhension du code python.

    # alias de types
    Map = List[List[HC]]
    PropositionnalVariable = int
    Literal = int
    Clause = List[Literal]
    ClauseBase = List[Clause]
    Model = List[Literal]

**Fonctionnement du programme :**

  
  
Pour le fonctionnement du programme de la phase1, nous avons utilisé un algorithme aléatoire de recherche (basé sur A* mais qui ne prend pas de carte en paramètre). Il se base sur une carte vide et renvoie le chemin le plus cours vers une case x à partir d'une case y.

Avant d'élaborer nos étapes, il faut noter que dans notre programme tout ce que voit hitman est enregistré dans un dictionnaire.

**Nous procédons dans la recherche en deux étapes:**
	- La première est de faire déplacer Hitman dans les coins de la carte.
	Nous faisons d'abord déplacer Hitman dans la case haute gauche de la carte, ensuite dans la case haut droite de la carte, dans la case bas gauche de la carte.

 

   -La deuxième étape est de faire déplacer Hitman dans des cases aléatoires de la carte. Nous générons une case aléatoire avec des random et essayons de faire déplacer Hitman sur cette case.
Tout ce que voit Hitman est enregistré dans un dictionnaire et ce dictionnaire sera renvoyé vérifier à la fin de la fonction.

  

**En nous basant sur le modèle du TP3, nous avons codé des règles pour la phase 1 :**

D'abord nous convertissons chaque case de la carte sous forme de variables. Par exemple si la carte a une taille 6,7 alors nous récupérons 6x7x13 = 546 variables ce qui nous fait 6000 clauses au lancement de la phase1. Nous pouvons inversement récupérer les données de la case en utilisant varaible_to_cell.
Nous avons programmé différentes fonctions "cell_to_variable" pour que notre base de clause n'augmente pas de taille exponentiellement. Par exemple cell_to_variable_zone_ecoute renvoie des clauses correspondantes aux 25 cases autour d'Hitman au lieux de toute la carte afin de ne pas surcharger notre fichier dimac.

  
**Voici nos 6 règles :**
- rule1_box_constraints(...) : Cette règle vérifie que chaque case sur la carte ne peut contenir qu'un seul élément parmi un mur, un garde ,un invité...

- rule2_object_map_constraints(...) : Cette règle vérifie qu'il y'a qu'un seul costume,corde et cible sur la carte.

- rule3_vision_gain(...) : Cette règle rajoute les clauses associées à ce que voit hitman (converti la vision de hitman en clauses).

- rule4_number_civils(...) : Cette règle vérifie que le nombre de civils vus par Hitman jusqu'ici est égal au nombre de civils présent sur la carte, si c'est le cas on sait que toutes les cases restantes ne contiennent pas d'invités.

- rule5_number_guards(...) : Cette règle vérifie que le nombre de gardes vus par Hitman jusqu'ici est égal au nombre de gardes présent sur la carte, si c'est le cas on sait que toutes les cases restantes ne contiennent pas de gardes.

- rule6_ecoute(...) : Cette règle nous renvoie toutes les informations liés à l'écoute :
		Si on entend rien alors les 25 cases autour de nous ne peuvent pas contenir de gardes ni d'invités.
		Dans les 25 cases autour de nous, en fonction de l'écoute, renvoie la base de clause contenant toutes les combinaisons possibles de personnes sur les 25 gardes autour de nous.
		
Ces 6 règles renvoient des clauses qui s'ajoutent automatiquement à notre base de clause finale. On a ajouté aussi une fonction "add_clause_to_dimacs" qui permet de mettre à jour le fichier cnf avec de nouvelles clauses.


Nous avions pu ensuite générer un fichier dimac avec ces règles mais par manque de temps nous n'avons pas pu implémenter SAT dans notre algorithme de découverte de la carte et donc nous ne pouvons faire aucune déduction dans les déplacements.

  

**Forces du programme :**

  

Hitman ne se déplace jamais en direction des cases qu'il a déjà visités.
Un dictionnaire est toujours renvoyé par notre programme et le dictionnaire correspond, en fonction de la difficulté de la carte, en grande partie à la carte recherchée.
  
**Faiblesses du programme :**

La plus grande faiblesse de notre programme est que nous avons pas réussi à implémenter SAT dans notre algorithme de découverte de la carte. Nous pouvons donc faire aucune déductions lors de notre parcours et donc Hitman se balade aléatoirement sur différentes cases de la carte.

  

**Comment faire fonctionner le programme :**

  

Afin de faire fonctionner notre programme, il suffit de faire lancer notre fonction main.py avec le fichier hitman dans le même dossier.
Afin de modifier la carte il suffit de modifier la carteword_example dans le fichier hitman.py.

Nous avons générés les affichages qui renvoient d'abord la carte trouvé par Hitman, ensuite nous affichons send.content et enfin end.phase1.

  

  
  

## **3. La modélisation STRIPS de la phase 2**

  

## **Prédicats :**

    wall(x,y) = Un mur est sur la case (x,y)

    cible(x,y) = La position de la cible est (x,y) 

    invite(x,y,o) = La position de l'invité est (x,y) avec l'orientation o

    garde(x,y,o) = La position du garde est (x,y) avec l'orientation o

    costume(x,y) = Le costume est sur la case(x,y)

    corde(x,y) = La corde est sur la case (x,y)


## **Fluentes :**

    at(x,y,o) = Hitman est sur la case (x,y) avec l'orientation o
    clear(x,y) = La case (x,y) est libre
    orientation(o) = Hitman est orianté vers o
    porte_le_costume(x) = Hitman porte le costume
    possède_le_costume(x) = Hitman possède le costume
    possède_la_corde(x) = Hitman possède la corde
    pénalités(x) =  le nombre x de pénalités
    est_dans_le_champ_de_vision_garde(x) = Hitman est dans le champ de vision de x garde
    est_dans_le_champ_de_vision_invité(x) = Hitman est dans le champ de vision de x invité 
    cible_est_morte()
    garde_est_mort()
    invité_est_mort()

  
## **Etat initial :**

Plaçons nous dans le cas du world_example présent dans hitman.py

    Init(at(0,0,N) ^ clear(0,1) ^ wall(0,2) ^ cible(0,3) ^ clear(0,4) ^ clear(0,5) ^ clear(1,0) ^ ....)

## **But :**

Pour gagner le joueur doit aller chercher la corde, puis aller tuer la cible et enfin retourné sur la case (0,0)

    Goal(cible_est_morte() ^ at(0, 0,_))

## **Actions :**


+  ## **Actions de déplacements :**

#### **Action(tourner_horaire())**

    PRECOND :

	orientation(N) ^ at(x,y,N)  
    orientation(E) ^ at(x,y,E) 
    orientation(S) ^ at(x,y,S) 
    orientation(W) ^ at(x,y,W)  

    orientation(N) ^ at(x,y,N) ^  est_dans_le_champ_de_vision_garde(z)
    orientation(E) ^ at(x,y,E) ^  est_dans_le_champ_de_vision_garde(z)
    orientation(S) ^ at(x,y,S) ^  est_dans_le_champ_de_vision_garde(z)
    orientation(W) ^ at(x,y,W) ^  est_dans_le_champ_de_vision_garde(z)

	EFFECT :

	¬orientation(N) ^ orientation(E) ^ at(x,y,E) ^ pénalités(1) 
    ¬orientation(E) ^ orientation(S) ^ at(x,y,S) ^ pénalités(1) 
    ¬orientation(S) ^ orientation(W) ^ at(x,y,W) ^ pénalités(1)
    ¬orientation(W) ^ orientation(N) ^ at(x,y,N) ^ pénalités(1)

    ¬orientation(N) ^ orientation(E) ^ at(x,y,E) ^ pénalités(5*z) 
    ¬orientation(E) ^ orientation(S) ^ at(x,y,S) ^ pénalités(5*z) 
    ¬orientation(S) ^ orientation(W) ^ at(x,y,W) ^ pénalités(5*z)
    ¬orientation(W) ^ orientation(N) ^ at(x,y,N) ^ pénalités(5*z)


#### **Action(tourner_anti_horaire())**

    PRECOND :

	orientation(N) ^ at(x,y,N) 
    orientation(E) ^ at(x,y,E) 
    orientation(S) ^ at(x,y,S) 
    orientation(W) ^ at(x,y,W)  

    orientation(N) ^ at(x,y,N) ^  est_dans_le_champ_de_vision_garde(z)
    orientation(E) ^ at(x,y,E) ^  est_dans_le_champ_de_vision_garde(z)
    orientation(S) ^ at(x,y,S) ^  est_dans_le_champ_de_vision_garde(z)
    orientation(W) ^ at(x,y,W) ^  est_dans_le_champ_de_vision_garde(z)

	EFFECT :

	¬orientation(N) ^ orientation(W) ^ at(x,y,W) ^ pénalités(1)
    ¬orientation(E) ^ orientation(N) ^ at(x,y,N) ^ pénalités(1)
    ¬orientation(S) ^ orientation(E) ^ at(x,y,E) ^ pénalités(1)
    ¬orientation(W) ^ orientation(S) ^ at(x,y,S) ^ pénalités(1)

    ¬orientation(N) ^ orientation(W) ^ at(x,y,W) ^ pénalités(5*z)
    ¬orientation(E) ^ orientation(N) ^ at(x,y,N) ^ pénalités(5*z)
    ¬orientation(S) ^ orientation(E) ^ at(x,y,E) ^ pénalités(5*z)
    ¬orientation(W) ^ orientation(S) ^ at(x,y,S) ^ pénalités(5*z)

#### **Action(avancer())**

  
	PRECOND :

	orientation(N) ^ at(x,y,N)  
    orientation(E) ^ at(x,y,E) 
    orientation(S) ^ at(x,y,S) 
    orientation(W) ^ at(x,y,W) 

	EFFECT :

	orientation(N) ^ at(x,y+1,N) ∧ ¬at(x,y,N) ^ pénalités(1)
    orientation(E) ^ at(x+1,y,E) ∧ ¬at(x,y,E) ^ pénalités(1)
    orientation(S) ^ at(x,y-1,S) ∧ ¬at(x,y,S) ^ pénalités(1)
    orientation(W) ^ at(x-1,y,W) ∧ ¬at(x,y,W) ^ pénalités(1)

    orientation(N) ^ at(x,y+1,N) ∧ ¬at(x,y,N) ^ est_dans_le_champ_de_vision_garde(z) ^ pénalités(5*z)
    orientation(E) ^ at(x+1,y,E) ∧ ¬at(x,y,E) ^ est_dans_le_champ_de_vision_garde(z) ^ pénalités(5*z)
    orientation(S) ^ at(x,y-1,S) ∧ ¬at(x,y,S) ^ est_dans_le_champ_de_vision_garde(z) ^ pénalités(5*z)
    orientation(W) ^ at(x-1,y,W) ∧ ¬at(x,y,W) ^ est_dans_le_champ_de_vision_garde(z) ^ pénalités(5*z)

  

#### **Action(tuer_cible())**

    PRECOND:  

    at(x,y,o) ^ cible(x,y) ^ possède_l_arme()

    at(x,y,o) ^ cible(x,y) ^ possède_l_arme() ^ est_dans_le_champ_de_vision_garde(z) 

    at(x,y,o) ^ cible(x,y) ^ possède_l_arme() ^ est_dans_le_champ_de_vision_invité(k)

    at(x,y,o) ^ cible(x,y) ^ possède_l_arme() ^ est_dans_le_champ_de_vision_invité(k) ^ est_dans_le_champ_de_vision_garde(z) 
        
    EFFECT:

    at(x,y,o) ^ ¬cible(x,y) ^ cible_est_morte()

    at(x,y,o) ^ ¬cible(x,y) ^ cible_est_morte() ^ pénalités(100 * z)

    at(x,y,o) ^ ¬cible(x,y) ^ cible_est_morte() ^ pénalités(100 * k )

    at(x,y,o) ^ ¬cible(x,y) ^ cible_est_morte() ^ pénalités(100 * (z + k))


#### **Action(neutraliser())**

    PRECOND:

    orientation(N) ^ at(x,y,N)  ^ garde(x,y+1,E)
    orientation(N) ^ at(x,y,N)  ^ garde(x,y+1,S)
    orientation(N) ^ at(x,y,N)  ^ garde(x,y+1,W)
    orientation(N) ^ at(x,y,N)  ^ invité(x,y+1,E)
    orientation(N) ^ at(x,y,N)  ^ invité(x,y+1,S)
    orientation(N) ^ at(x,y,N)  ^ invité(x,y+1,W)

    orientation(E) ^ at(x,y,E)  ^ garde(x+1,y,S)
    orientation(E) ^ at(x,y,E)  ^ garde(x+1,y,W)
    orientation(E) ^ at(x,y,E)  ^ garde(x+1,y,N)
    orientation(E) ^ at(x,y,E)  ^ invité(x+1,y,S)
    orientation(E) ^ at(x,y,E)  ^ invité(x+1,y,W)
    orientation(E) ^ at(x,y,E)  ^ invité(x+1,y,N)

    orientation(S) ^ at(x,y,S)  ^ garde(x-1,y,W)
    orientation(S) ^ at(x,y,S)  ^ garde(x-1,y,E)
    orientation(S) ^ at(x,y,S)  ^ garde(x-1,y,N)
    orientation(S) ^ at(x,y,S)  ^ invité(x-1,y,W)
    orientation(S) ^ at(x,y,S)  ^ invité(x-1,y,E)
    orientation(S) ^ at(x,y,S)  ^ invité(x-1,y,N)

    orientation(W) ^ at(x,y,W)   ^ garde(x,y-1,E)
    orientation(W) ^ at(x,y,W)   ^ garde(x,y-1,S)
    orientation(W) ^ at(x,y,W)   ^ garde(x,y-1,N)
    orientation(W) ^ at(x,y,W)   ^ invité(x,y-1,E)
    orientation(W) ^ at(x,y,W)   ^ invité(x,y-1,S)
    orientation(W) ^ at(x,y,W)   ^ invité(x,y-1,N)


    orientation(N) ^ at(x,y,N)  ^ garde(x,y+1,E) ^ est_dans_le_champ_de_vision_garde(z) 
    ........................
    
    orientation(N) ^ at(x,y,N)  ^ garde(x,y+1,E) ^ est_dans_le_champ_de_vision_invité(k) 
    .............................

    orientation(N) ^ at(x,y,N)  ^ garde(x,y+1,E) ^ est_dans_le_champ_de_vision_garde(z) ^ est_dans_le_champ_de_vision_invité(k) 
    ...............
        
    EFFECT: 

    orientation(N) ^ at(x,y,N)  ^ ¬garde(x,y+1,E) ^ garde_est_mort() ^ penalités(20)
    orientation(N) ^ at(x,y,N)  ^ ¬garde(x,y+1,S) ^ garde_est_mort() ^ penalités(20)
    orientation(N) ^ at(x,y,N)  ^ ¬garde(x,y+1,W) ^ garde_est_mort() ^ penalités(20)
    orientation(N) ^ at(x,y,N)  ^ ¬invité(x,y+1,E)  ^ invité_est_mort() ^ penalités(20)
    orientation(N) ^ at(x,y,N)  ^ ¬invité(x,y+1,S) ^ invité_est_mort() ^ penalités(20)
    orientation(N) ^ at(x,y,N)  ^ ¬invité(x,y+1,W) ^ invité_est_mort() ^ penalités(20)

    orientation(E) ^ at(x,y,E)  ^ ¬garde(x+1,y,S) ^ garde_est_mort() ^ penalités(20)
    orientation(E) ^ at(x,y,E)  ^ ¬garde(x+1,y,W) ^ garde_est_mort() ^ penalités(20)
    orientation(E) ^ at(x,y,E)  ^ ¬garde(x+1,y,N) ^ garde_est_mort() ^ penalités(20)
    orientation(E) ^ at(x,y,E)  ^ ¬invité(x+1,y,S) ^ invité_est_mort() ^ penalités(20)
    orientation(E) ^ at(x,y,E)  ^ ¬invité(x+1,y,W) ^ invité_est_mort() ^ penalités(20)
    orientation(E) ^ at(x,y,E)  ^ ¬invité(x+1,y,N) ^ invité_est_mort() ^ penalités(20)


    orientation(S) ^ at(x,y,S)  ^ ¬garde(x-1,y,W) ^ garde_est_mort() ^ penalités(20)
    orientation(S) ^ at(x,y,S)  ^ ¬garde(x-1,y,E) ^ garde_est_mort() ^ penalités(20)
    orientation(S) ^ at(x,y,S)  ^ ¬garde(x-1,y,N) ^ garde_est_mort() ^ penalités(20)
    orientation(S) ^ at(x,y,S)  ^ ¬invité(x-1,y,W) ^ invité_est_mort() ^ penalités(20)
    orientation(S) ^ at(x,y,S)  ^ ¬invité(x-1,y,E) ^ invité_est_mort() ^ penalités(20)
    orientation(S) ^ at(x,y,S)  ^ ¬invité(x-1,y,N) ^ invité_est_mort() ^ penalités(20)

    orientation(W) ^ at(x,y,W)   ^ ¬garde(x,y-1,E) ^ garde_est_mort() ^ penalités(20)
    orientation(W) ^ at(x,y,W)   ^ ¬garde(x,y-1,S) ^ garde_est_mort() ^ penalités(20)
    orientation(W) ^ at(x,y,W)   ^ ¬garde(x,y-1,N) ^ garde_est_mort() ^ penalités(20)
    orientation(W) ^ at(x,y,W)   ^ ¬invité(x,y-1,E) ^ invité_est_mort() ^ penalités(20)
    orientation(W) ^ at(x,y,W)   ^ ¬invité(x,y-1,S) ^ invité_est_mort() ^ penalités(20)
    orientation(W) ^ at(x,y,W)   ^ ¬invité(x,y-1,N)  ^ invité_est_mort() ^ penalités(20)

    orientation(N) ^ at(x,y,N)  ^ ¬garde(x,y+1,E) ^ garde_est_mort() ^ penalités(100 * z)
    .......................

    orientation(N) ^ at(x,y,N)  ^ ¬garde(x,y+1,E) ^ garde_est_mort() ^ penalités(100 * k)
    .......................

    orientation(N) ^ at(x,y,N)  ^ ¬garde(x,y+1,E) ^ garde_est_mort() ^ penalités(100 * (k+z))
    ........................


    

#### **Action(mettre_costume())**

    PRECOND:

    possède_costume()

    possède_costume() ^ est_dans_le_champ_de_vision_garde(z)

    possède_costume() ^ est_dans_le_champ_de_vision_invité(k)

    possède_costume() ^ est_dans_le_champ_de_vision_garde(x,y)
        
    EFFECT:

    porte_le_costume() ^ penalités(1)

    porte_le_costume() ^ penalités(1 + 100 * z )

    porte_le_costume() ^ penalités(1 + 100 * k)

    porte_le_costume() ^ penalités(1 + 100 * (z + k))
   

#### **Action(prendre_costume())**

    PRECOND: 
    at(x,y,o) ^ costume(x,y) 

    at(x,y,o) ^ costume(x,y) ^ est_dans_le_champ_de_vision_garde(z)
        
    EFFECT:

    at(x,y,o) ^ ¬costume(x,y) ^ possède_costume() ^ penalités(1)

    at(x,y,o) ^ ¬costume(x,y) ^ possède_costume() ^ penalités(5*z)
   
#### **Action(prendre_arme())**

    PRECOND: 

    at(x,y,o) ^ corde(x,y)

    at(x,y,o) ^ corde(x,y) ^ est_dans_le_champ_de_vision_garde(z)
        
    EFFECT:

    at(x,y,o) ^ ¬corde(x,y) ^ penalités(1)

    at(x,y,o) ^ ¬corde(x,y) ^ penalités(5*z)

  

## **2. Programme en Python phase 2**

  

Pour le fonctionnement du programme de la phase2, nous avons utilisé un algorithme A*. La fonction prend en entrée un monde représenté par un dictionnaire monde, les coordonnées de départ start, une référence à un objet referee de type HitmanReferee et un objectif goal de type HC.

  

Nous avons choisi de créer une class Node avec comme attribut :

Un nœud de départ start_node est créé avec la position start. La fonction détermine la position de l'objectif en fonction de la valeur de goal en utilisant des méthodes comme rechercher_cible, rechercher_corde_piano, rechercher_sortie.

  
  

**Heuristique :**

Notre heuristique est basé sur un calcul de coût différent, le premier est basé sur la distance de Manhattan et la deuxième sur le calcul de pénalité.

  

Dans la fonction calculer_penalite, la pénalité est calculée en fonction de la position actuelle et de l'action envisagée. La fonction prend en compte plusieurs facteurs pour déterminer la pénalité :

  

  - La présence de gardes dans la zone de vision : Si la position actuelle est visible par des gardes, cela peut entraîner un risque accru. La pénalité est donc proportionnelle au nombre de gardes qui peuvent voir la position.

  

   - La présence de civils dans la zone de vision : De la même manière, si la position actuelle est visible par des civils, cela peut également représenter un risque. La pénalité est proportionnelle au nombre de civils qui peuvent voir la position.

  

Le type d'action effectuée :
- Différentes actions peuvent entraîner des pénalités différentes. Par exemple, neutraliser un garde peut entraîner une pénalité plus élevée que simplement se déplacer ou prendre un costume.

  

En combinant ces facteurs, la fonction calculer_penalite calcule une pénalité spécifique pour chaque nœud en fonction de sa position et de l'action envisagée. Cette pénalité est ensuite ajoutée au coût heuristique (h_score) pour obtenir un coût mis à jour (updated_h_score) pour le nœud.

  
  

**Phase2 :**

  

Pour appliquer notre phase2 à Hitman on a programmé une fonction convert_action_to_hitman qui prend en entré le chemin optimal renvoyé par A* et qui adapte ce chemin en mouvement d'Hitman. Cetta partie nous a posé de nombreux soucis car la carte sous forme de dictionnaire possède des coordonnées non identiques comparé à la carte sous forme de tableau.
  
  

**Forces du programme :**

  

Les forces du programme sont : 
Hitman choisit le chemin le plus court ,neutralise un garde si besoin fonctionne bien et le temps d'exécution est presque instantané.

  
  

**Faiblesses du programme :**

  

La faiblesse du programme est que tous ce qui touche au costume ne fonctionne pas. Nous avons commencé à travailler à l'implémentation du costume dans notre heuristique mais cette implémentation augmentait notre nombre de pénalités. C'est pourquoi par manque de temps pour corriger l'implémentation du costume, nous avons décidé de l'enlever.
  
  

**Comment faire fonctionner le programme :**

  

Il vous sufit d'exécuter le fichier phase2.py . Ensuite pour changer de map il faut modifier ligne 416 la map par celle que vous souhaitez :

  

map = complete_map_example

  
  
  

## **4. Conclusion**
Pour ce projet, nous avons réussi à rendre la phase2 fonctionnelle sur tout type de cartes et nous nous avons réussi à  renvoyer un dictionnaire qui correspond en grande partie à la carte sur laquelle se trouve Hitman. Malheureusement, nous avons manqué de temps pour garantir une phase1 parfaitement fonctionnelle et l'implémentation des déductions du SAT dans notre parcours d'exploration.

Ce projet nous a permis de constater les difficultés liées à la gestion d’un projet conséquent, ainsi que de la difficulté de programmation d'une intelligence artificielle pouvant parcourir un monde qu'elle ne connait pas à l'avance. Malgré les difficultés rencontrés, ce projet nous a permet d'acquérir de nombres connaissances dans la programmation d'un algorithme de recherche et dans la modélisation d'un problème en logique propositionnelle. 



