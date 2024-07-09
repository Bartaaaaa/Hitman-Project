from itertools import product
from typing import List, Tuple, Union, Any,Dict
import subprocess  # pour gophersat
from hitman import HC, HitmanReferee, complete_map_example
from itertools import combinations
from pprint import pprint
import random
from queue import PriorityQueue

# alias de types
Map = List[List[HC]]
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]

gophersat = "/mnt/c/Users/Grzadziel Bartlomiej/Desktop/UTC/phase1/gophersat.exe"
#"C:/Users/Ines ABBACHE/Documents/gophersat"
#gophersat = "gophersat.exe"
def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(
        filename: str, cmd: str = gophersat, encoding: str = "utf8") -> Tuple[bool, List[List[int]]]:
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    models = []
    # for line in lines[2:]:
    line = lines[2]
    if line.startswith("v"):
        model = line[2:-2].split(" ")
        # models.append([int(x) for x in model])
        models = [int(x) for x in model]

    return True, models

'''
def run_gophersat(filename):
    try:
        gophersat_path = "C:/Users/Ines ABBACHE/Documents/gophersat"
        output = subprocess.check_output(['gophersat', filename], universal_newlines=True)
        f = open("gophersat_results.txt", "w")
        f.write(output)
        f.close()
        return output
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de gophersat : {e}")
        return None
'''

def generate_map(m, n,
                 referee: HitmanReferee):  # qui va generer la map en fct de m et n qui sont dans la classe hitman referee
    status_phase1 = referee.start_phase1()
    referee.m = m
    referee.n = n
    referee.world = [None] * m
    for k in range(m):
        referee.world[k] = [None] * n
    # pprint(referee.world)


def variable_to_cell(var: PropositionnalVariable, referee: HitmanReferee) -> Tuple[int, int, int]:
    status_phase1 = referee.start_phase1()
    n = status_phase1["n"]
    var = var - 1
    ligne = var // (13 * n)
    colonne = (var // 13) % n
    valeur = var % 13 + 1
    return ligne, colonne, valeur


def variable_to_HC(referee: HitmanReferee, var: PropositionnalVariable) -> HC:
    nom_attribut = None
    ligne, colonne, valeur = variable_to_cell(var, referee)
    for attribut in HC:
        if attribut.value == valeur:
            # nom_attribut = attribut.name
            return attribut
            break
    # print(nom_attribut.value)
    return nom_attribut


def model_to_map(model: Model,referee: HitmanReferee, nb_vals: int = 13) -> Map:
    status_phase1 = referee.start_phase1()
    n = status_phase1["n"]
    m = status_phase1["m"]
    map = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(510+1):
        for var in model:
            if var > 0:
                # ligne, colonne, valeur = variable_to_cell(var)
                ligne, colonne, valeur = variable_to_cell(var, referee)
                attribut = variable_to_HC(referee, var)
                map[ligne][colonne] = attribut.name
    return map



def cell_to_variable_map(i: int, j: int, val: int,
                         referee: HitmanReferee) -> PropositionnalVariable:  # i = , j = , val =
    status_phase1 = referee.start_phase1()
    n = status_phase1["n"]
    m = status_phase1["m"]
    return i * (13 * n) + j * n + (val)
    #return i * m + j * n + val + 1
    #return i * n * 13 + j * 13 + val + 1


def cell_to_variable_zone_ecoute_HC(k: int, l: int, val: int, referee: HitmanReferee) -> PropositionnalVariable:
    status_phase1 = referee.start_phase1()
    clauses = []
    dist = 2
    m = status_phase1["m"]
    n = status_phase1["n"]
    pos = status_phase1["position"]
    possible_offset = range(-dist, dist + 1)
    offsets = product(possible_offset, repeat=2)
    x, y = pos
    zone_size = 5  # Taille de la zone d'écoute (25 cases)
    zone_x_start = x - zone_size // 2  # Coordonnée x du coin supérieur gauche de la zone
    zone_y_start = y - zone_size // 2  # Coordonnée y du coin supérieur gauche de la zone
    zone_x_end = zone_x_start + zone_size  # Coordonnée x du coin inférieur droit de la zone
    zone_y_end = zone_y_start + zone_size  # Coordonnée y du coin inférieur droit de la zone

    # Vérifier si les coordonnées (k, l) se trouvent dans la zone des 25 cases
    if k < zone_x_start or k >= zone_x_end or l < zone_y_start or l >= zone_y_end:
        raise ValueError("Les coordonnées (k, l) ne sont pas dans la zone des 25 cases")

    for i, j in offsets:
        pos_x, pos_y = x + i, y + j
        if pos_x >= n or pos_y >= m or pos_x < 0 or pos_y < 0 or k >= n or l >= m or k < 0 or l < 0:
            continue
        if pos_x == k and pos_y == l:
            #return pos_x * (13 * n) + (pos_y * n) + val
            if val > 13 :
                raise ValueError("val doit etre compris entre 1 et 13")
            return (n * pos_x * 13) + (pos_y * 13) + val

def cell_to_variable_zone_vision_HC(k: int, l: int, val: int, referee: HitmanReferee) -> PropositionnalVariable:
    status_phase1 = referee.start_phase1()
    clauses = []
    dist = 3
    m = status_phase1["m"]
    n = status_phase1["n"]
    pos = status_phase1["position"]
    possible_offset = range(-dist, dist + 1)
    offsets = product(possible_offset, repeat=2)
    x, y = pos
    zone_size = 5  # Taille de la zone d'écoute (25 cases)
    zone_x_start = x - zone_size // 2  # Coordonnee x du coin supérieur gauche de la zone
    zone_y_start = y - zone_size // 2  # Coordonnee y
    zone_x_end = zone_x_start + zone_size  # Coordonnee x du coin inférieur droit de la zone
    zone_y_end = zone_y_start + zone_size  # Coordonnee y

    # Vérifier si les coordonnées (k, l) se trouvent dans la zone des 25 cases
    if k < zone_x_start or k >= zone_x_end or l < zone_y_start or l >= zone_y_end:
        raise ValueError("Les coordonnées (k, l) ne sont pas dans la zone des 25 cases")

    for i, j in offsets:
        pos_x, pos_y = x + i, y + j
        if pos_x >= n or pos_y >= m or pos_x < 0 or pos_y < 0 or k >= n or l >= m or k < 0 or l < 0:
            continue
        if pos_x == k and pos_y == l:
            #return pos_x * (13 * n) + (pos_y * n) + val
            if val > 13 :
                raise ValueError("val doit etre compris entre 1 et 13")
            return (n * pos_x * 13) + (pos_y * 13) + val


def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    clauses = [variables]
    if isinstance(variables, list):
        for combination in combinations(variables, 2):
            clauses.append([-x for x in combination])
    return clauses


#Transformer en sorte que ça s'applique seulement au 25 cases autour mais que pour les personne
def rule1_box_constraints(referee: HitmanReferee) -> ClauseBase:
    status_phase1 = referee.start_phase1()
    clauses = []
    dist = 2
    m = status_phase1["m"]
    n = status_phase1["n"]
    for ligne in range(m):
        for colonne in range(n):
            box = [cell_to_variable_map(ligne, colonne, k,referee)for k in range(1,14)]
            clauses += unique(box)
    return clauses


def rule2_object_map_constraints(referee: HitmanReferee) -> ClauseBase:
    status_phase1 = referee.start_phase1()
    clause_corde = []
    clause_cible = []
    clause_costume = []
    final = []
    m = status_phase1["m"]
    n = status_phase1["n"]
    for ligne in range(m):
        for colonne in range(n):
            clause_corde += [cell_to_variable_map(ligne, colonne,  13, referee) ]
            clause_costume += [cell_to_variable_map(ligne, colonne, 12, referee)]
            clause_cible += [cell_to_variable_map(ligne, colonne, 11, referee)]
    final+=unique(clause_corde)
    final+=unique(clause_costume)
    final+=unique(clause_cible)
    return final




# récupérer ce que nous renvoie la vision d'hitman , traiter le cas en fonction de la longueur de la vision
# transformer en clauses avec la position puis la valeur de l'objet vu
def rule3_vision_gain(referee: HitmanReferee) -> ClauseBase:
    status_phase1 = referee.start_phase1()
    clauses = []
    vision = status_phase1["vision"]
    for element in vision:
        coord, objet = element
        i = coord[0]
        j = coord[1]
        valeur = objet.value
        clauses.append(cell_to_variable_zone_vision_HC(i, j, valeur, referee))  # Wrap the integer in a list
    return clauses


#procédure :  on récupère le nombre d'invité que nous renvoie l'arbitre et on compte le nombre d'invités qu'on a vu jusqu'ici,
#si le chiffre est égal alors on sait que les personnes restantes sont des gardes
def rule4_number_civils(referee: HitmanReferee, map: Dict[Tuple[int, int], HC]) -> ClauseBase:  # règle qui nous dit si on a trouvé tous les invités
    status_phase1 = referee.start_phase1()
    clauses = []
    nb_civils = status_phase1["civil_count"]
    m = status_phase1["m"]
    n = status_phase1["n"]

    nombre_civils = sum(1 for valeur in map.values() if valeur == HC.CIVIL_N or valeur == HC.CIVIL_E or valeur == HC.CIVIL_S or  valeur == HC.CIVIL_W )
    if nb_civils == nombre_civils :
        for ligne in range(m):
            for colonne in range(n):
                    clauses.append([-cell_to_variable_map(ligne, colonne, k, referee) for k in range(7,11)])
    return clauses

#à revoir inversement
def rule5_number_gards(referee: HitmanReferee, map: Dict[Tuple[int, int], HC]) -> ClauseBase:  # règle qui nous dit si on a trouvé tous les gardes
    status_phase1 = referee.start_phase1()
    clauses = []
    nb_gardes = status_phase1["guard_count"]
    m = status_phase1["m"]
    n = status_phase1["n"]

    nombre_guardes= sum(1 for valeur in map.values() if valeur == HC.GUARD_E or valeur == HC.GUARD_N or valeur == HC.GUARD_S or valeur == HC.GUARD_W)
    if nb_gardes == nombre_guardes:
        for ligne in range(m):
            for colonne in range(n):
                clauses.append([-cell_to_variable_map(ligne, colonne, k, referee) for k in range(3, 7)])
    return clauses


# si il ya personne(on entend 0pers) on rajoute dans les 25 case la negation de tous les gardes + invités
# si tu vois la personne + tu entend 1 pers dans les 25 cases alors tu la trouvé + le reste des cases sont sans personne ie la negation de tous les gardes + invités
def regle_ecoute(referee: HitmanReferee):
    status_phase1 = referee.start_phase1()
    clauses = []
    hear = status_phase1["hear"]
    vision = status_phase1["vision"]
    dist = 2
    m = status_phase1["m"]
    n = status_phase1["n"]
    pos = status_phase1["position"]
    possible_offset = range(-dist, dist + 1)
    offsets = product(possible_offset, repeat=2)
    x, y = pos
    for i, j in offsets:
        pos_x, pos_y = x + i, y + j
        if pos_x >= n or pos_y >= m or pos_x < 0 or pos_y < 0:
            continue
        # il entend 0  personne dans sa zone
        if hear == 0:
            clauses.append([-cell_to_variable_map(pos_x, pos_y, k, referee) for k in range(3, 12)])
        # il entend 1,2,3 ou 4  personne dans sa zone
        if hear==1 or hear==2 or hear==3 or hear==4:
                clauses.append([cell_to_variable_map(pos_x, pos_y, k, referee) for k in range(3, 12)])
        # il entend 1 personne et voit une seule personne
        for element in vision:
            coord, objet = element
            i = coord[0]
            j = coord[1]
            valeur = objet.value
            for k in range(13):
                 if hear == 1 and k != valeur :
                     clauses.append(-cell_to_variable_map(pos_x, pos_y, k, referee))
    return clauses


def ajout_base_de_connaissance(
                               referee: HitmanReferee) -> ClauseBase:  # répertorie toutes les clauses et les met dans la base de connaissance
    clauses = []
    clauses += rule1_box_constraints(referee)
    clauses += rule2_object_map_constraints(referee)
    clauses += rule3_vision_gain(referee)
    clauses += rule4_number_civils(referee,complete_map_example1)
    clauses += rule5_number_gards(referee,complete_map_example1)
    clauses += regle_ecoute(referee)

    return clauses

def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    s = f"p cnf {nb_vars} {len(clauses)}\n"
    for clause in clauses:
        if not isinstance(clause, list):
            clause = [clause]  # Si la clause n'est pas une liste, l'envelopper dans une liste
        for literal in clause:
            s += f"{literal} "
        s += "0\n"
    return s

def resolve_phase1(map: Map, hr: HitmanReferee) -> Model:
    clauses = ajout_base_de_connaissance(hr)
    filename = "hitman.cnf"

    status_phase1 = hr.start_phase1()
    # print(status_phase1)
    m = status_phase1["m"]
    n = status_phase1["n"]

    write_dimacs_file(clauses_to_dimacs(clauses, m*n*13), filename)
    result = exec_gophersat(filename)

    if result[0]:
        return result[1]
    else:
        return []


#  si le sat ne nous renvoi pas un unique modèle c qu'il faut continuer à lui donner de l'information
# apparement il y a une fct qui permet de recup le nombre de chose que renvoi gophersat
def analyse_SAT():  # traduit ce que renvoie le sat
    pass


def show_resolution(map: Map, hr: HitmanReferee):
    pprint(model_to_map(resolve_phase1(map,hr),hr))
    return


def add_clauses_to_dimacs(file_path: str, clauses: ClauseBase):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    nb_vars, nb_clauses = map(int, lines[0].split()[2:])  # Récupérer le nombre de variables et de clauses
    nb_clauses += len(clauses)  # Mettre à jour le nombre de clauses

    with open(file_path, 'w') as file:
        file.write(f"p cnf {nb_vars} {nb_clauses}\n")  # Écrire la nouvelle ligne d'en-tête

        for line in lines[1:]:
            file.write(line)  # Copier les lignes existantes

        for clause in clauses:
            for literal in clause:
                file.write(f"{literal} ")
            file.write("0\n")


class Node:
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

    def f(self):
        return self.g + self.h

# Fonction A* pour trouver le chemin optimal
# Fonction A* pour trouver le chemin optimal
def algo_recherche( start: Tuple[int, int], referee: HitmanReferee,
          goal_position: Tuple[int, int]) -> List[Tuple[int, int]]:
    status_phase1 = referee.start_phase1()
    n = status_phase1["n"]
    m = status_phase1["m"]

    # Instanciation de l'objet Node avec la position initiale
    start_node = Node(start)

    # Définition des mouvements possibles (haut, bas, gauche, droite )
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Vérification si une position est valide dans la carte


    # Calcul de la distance heuristique entre deux positions
    def heuristic(position1, position2):
        x1, y1 = position1
        x2, y2 = position2
        return abs(x1 - x2) + abs(y1 - y2)

    # Initialisation des nœuds de départ et d'arrivée
    start_node = Node(start)
    goal_node = Node(goal_position)

    # Initialisation de la file de priorité pour les nœuds à explorer
    open_list = PriorityQueue()
    open_list.put((0, start_node))  # Utilise un tuple (f, node) pour la priorité

    # Initialisation des ensembles pour les nœuds déjà visités
    closed_set = set()
 
    # Recherche du chemin optimal
    while not open_list.empty():
        _, current_node = open_list.get()

        # Vérification si le nœud actuel est le nœud objectif
        if current_node.position == goal_node.position:
            path = []
            node = current_node
            while node is not None:
                path.append(node.position)
                node = node.parent
            return path[::-1]
        # Ajout du nœud actuel à l'ensemble des nœuds visités
        closed_set.add(current_node.position)

        # Génération des voisins du nœud actuel
        for move in moves:
            new_position = (
                current_node.position[0] + move[0],
                current_node.position[1] + move[1]
            )
            # Vérification si la nouvelle position est valide
            if new_position[0] < 0 or new_position[0] >= m or new_position[1] < 0 or new_position[1] >= n:
                continue
            # Vérification si la nouvelle position a déjà été visitée
            if new_position in closed_set:
                continue

            # Calcul du coût pour atteindre la nouvelle position depuis le nœud actuel
            new_g = current_node.g + 1

            # Calcul du coût heuristique pour atteindre le nœud objectif depuis la nouvelle position
            new_h = heuristic(new_position, goal_node.position)

            # Création du nœud voisin
            new_node = Node(
                position=new_position,
                parent=current_node,
                g=new_g,
                h=new_h
            )

            # Ajout du nœud voisin à la file de priorité
            open_list.put((new_node.f, new_node))

    # Si aucun chemin n'a été trouvé, retourner une liste vide
    return []


def get_status_after_move(dictionnaire):
    vision = dictionnaire['vision']
    position = dictionnaire['position']
    orientation = dictionnaire['orientation']
    hear = dictionnaire['hear']
    penalties = dictionnaire['penalties']
    is_in_guard_range = dictionnaire['is_in_guard_range']
    status = dictionnaire['status']
    guard_count = dictionnaire['guard_count']
    civil_count = dictionnaire['civil_count']
    m = dictionnaire['m']
    n = dictionnaire['n']
    etat = {
        'status': status,
        'guard_count': guard_count,
        'civil_count': civil_count,
        'm': m,
        'n': n,
        'position': position,
        'orientation': orientation,
        'vision': vision,
        'hear': hear,
        'penalties': penalties,
        'is_in_guard_range': is_in_guard_range
    }
    return etat

def phase1():
    hr = HitmanReferee()
    dic = hr.start_phase1()
    status = get_status_after_move(dic)
    ligne = status["m"]
    colonne = status["n"]
    case_aleatoire = (random.randint(0, ligne-1), random.randint(0, colonne+1))
    L = {(0, 0): HC.EMPTY}
    vision = status["vision"]
    for cord,element in vision:
        L[cord]=element
    orientation = HC.N
    #On va dans les 3 coins de la carte avant de voyager à l'improviste :
    case_haut_gauche = (0,colonne+1)
    chemin_haut_gauche = algo_recherche( (0,0), hr, case_haut_gauche)

    for i in range(len(chemin_haut_gauche) - 1):
        pos1 = chemin_haut_gauche[i]
        pos2 = chemin_haut_gauche[i + 1]
        if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
            if orientation == HC.E:
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
            elif orientation == HC.N:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
            elif orientation == HC.S:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
            elif orientation == HC.W:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
        elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:

            if orientation == HC.E:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.S

            elif orientation == HC.N:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                orientation = HC.S

            elif orientation == HC.S:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.S

            elif orientation == HC.W:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element


                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.S
        elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:


            if orientation == HC.E:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                orientation = HC.E
            elif orientation == HC.N:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.E
            elif orientation == HC.S:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.E
            elif orientation == HC.W:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.E
        elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
            if orientation == HC.E:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
            elif orientation == HC.N:
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
            elif orientation == HC.S:
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
            elif orientation == HC.W:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
        status = get_status_after_move(dic)
    position = status["position"]
    case_haut_droite = (ligne - 3, colonne +1)
    chemin_haut_droite = algo_recherche( position, hr, case_haut_droite)
    # Déplacement vers le coin bas droit
    for i in range(len(chemin_haut_droite) - 1):
        pos1 = chemin_haut_droite[i]
        pos2 = chemin_haut_droite[i + 1]


        if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
            if orientation == HC.E:
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
            elif orientation == HC.N:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
            elif orientation == HC.S:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
            elif orientation == HC.W:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
        elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:

            if orientation == HC.E:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.S

            elif orientation == HC.N:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                orientation = HC.S

            elif orientation == HC.S:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.S

            elif orientation == HC.W:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element


                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.S
        elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:

            if orientation == HC.E:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                orientation = HC.E
            elif orientation == HC.N:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.E
            elif orientation == HC.S:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.E
            elif orientation == HC.W:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.E
        elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
            if orientation == HC.E:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
            elif orientation == HC.N:
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
            elif orientation == HC.S:
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
            elif orientation == HC.W:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
        status = get_status_after_move(dic)
    position = status["position"]
    case_bas_droite = (ligne-3, 0)
    chemin_bas_droite = algo_recherche( position, hr, case_bas_droite)
    for i in range(len(chemin_bas_droite) - 1):
        pos1 = chemin_bas_droite[i]
        pos2 = chemin_bas_droite[i + 1]

        if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
            if orientation == HC.E:
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
            elif orientation == HC.N:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
            elif orientation == HC.S:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
            elif orientation == HC.W:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.N
        elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:

            if orientation == HC.E:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.S

            elif orientation == HC.N:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                orientation = HC.S

            elif orientation == HC.S:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.S

            elif orientation == HC.W:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element


                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element


                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.S
        elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:

            if orientation == HC.E:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                orientation = HC.E
            elif orientation == HC.N:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.E
            elif orientation == HC.S:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.E
            elif orientation == HC.W:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.E
        elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
            if orientation == HC.E:

                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
            elif orientation == HC.N:
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
            elif orientation == HC.S:
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.turn_anti_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
            elif orientation == HC.W:

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element

                dic = hr.turn_clockwise()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                hr.turn_clockwise()
                dic = hr.move()
                status = get_status_after_move(dic)
                vision = status["vision"]
                for cord, element in vision:
                    L[cord] = element
                orientation = HC.W
        status = get_status_after_move(dic)
    position = status["position"]
    chemin = algo_recherche( position, hr, case_aleatoire)
    for i in range(7):
        for i in range(len(chemin) - 1):
            pos1 = chemin[i]
            pos2 = chemin[i + 1]
            if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
                if orientation == HC.E:
                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.N
                elif orientation == HC.N:

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    hr.turn_clockwise()
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.N
                elif orientation == HC.S:

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.N
                elif orientation == HC.W:

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.N
            elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:

                if orientation == HC.E:

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.S

                elif orientation == HC.N:


                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    orientation = HC.S

                elif orientation == HC.S:

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    hr.turn_clockwise()
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.S

                elif orientation == HC.W:

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element


                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.S
            elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:

                if orientation == HC.E:

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    hr.turn_clockwise()
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    orientation = HC.E
                elif orientation == HC.N:

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.E
                elif orientation == HC.S:

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.E
                elif orientation == HC.W:

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.E
            elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
                if orientation == HC.E:

                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.W
                elif orientation == HC.N:
                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.W
                elif orientation == HC.S:
                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.turn_anti_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.W
                elif orientation == HC.W:

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element

                    dic = hr.turn_clockwise()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    hr.turn_clockwise()
                    dic = hr.move()
                    status = get_status_after_move(dic)
                    vision = status["vision"]
                    for cord, element in vision:
                        L[cord] = element
                    orientation = HC.W
        status = get_status_after_move(dic)
        position = status['position']
        case_aleatoire = (random.randint(0, ligne-1), random.randint(0, colonne-1))
        while case_aleatoire in L:
            case_aleatoire = (random.randint(0, ligne-1), random.randint(0, colonne-1))
        chemin = algo_recherche(position, hr, case_aleatoire)
    coord_found = []
    for coord, element in L.items():
        coord_found.append(coord)
    for coord,element in L.items() :
        coordlignemax= 0
        coordcolonnemax= 0
        if coord[0]>coordlignemax :
            coordlignemax = coord[0]
        if coord[1]>coordcolonnemax :
            coordcolonnemax = coord[1]
    combinations_dict = {(x, y): HC.EMPTY for x in range(coordlignemax) for y in range(coordcolonnemax)}
    for coord in combinations_dict:
        if coord not in coord_found:
            L[coord] = HC.EMPTY
    print("VOICI LA CARTE DECOUVERTE PAR HITMAN :")
    pprint(L)
    print("VOICI L ETAT DE HITMAN ")
    print(status)
    print("HITMAN A T IL REUSSI A DECOUVRIR TOUTE LA CARTE ? :")
    print(hr.send_content(L))
    print(hr.end_phase1())


def main():
        hr = HitmanReferee()
        hr.start_phase1()
        phase1()


if __name__ == "__main__":
    main()

















