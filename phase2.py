from typing import List, Tuple, Dict
from hitman import HC, HitmanReferee, complete_map_example

from queue import PriorityQueue


class Node:
    def __init__(self, position, parent=None, g=0, h=0, penalty=0, action = "",costume_worn = False, has_suit = False,orientation = HC.N):
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.penalty = penalty
        self.action = action
        self.costume_worn = costume_worn
        self.has_suit = has_suit
        self.orientation = orientation
        self.f = self.calculate_f()

    def calculate_f(self):
        return self.g + self.h + self.penalty

    def __lt__(self, other):
        return self.f < other.f


    def rechercher_cible(self, world : Dict[Tuple[int, int], HC]):
        for clef,valeur in world.items():
            if valeur == HC.TARGET:
                return clef
        return None

    def rechercher_corde_piano(self, world : Dict[Tuple[int, int], HC]):
        for clef,valeur in world.items():
            if valeur == HC.PIANO_WIRE:
                return clef
        return None

    def rechercher_sortie(self, world : Dict[Tuple[int, int], HC]):
        return (0,0)

    def recherche_costume(self, world: Dict[Tuple[int, int], HC]):
        for clef, valeur in world.items():
            if valeur == HC.SUIT:
                return clef
        return None



def astar(monde: Dict[Tuple[int, int], HC], start: Tuple[int, int], referee : HitmanReferee, goal: HC) -> List[Tuple[int, int]]:
    start_node = Node(start)

    if goal == HC.TARGET:
        goal_position = start_node.rechercher_cible(monde)
    elif goal == HC.PIANO_WIRE:
        goal_position = start_node.rechercher_corde_piano(monde)
    elif goal == HC.EMPTY:
        goal_position = start_node.rechercher_sortie(monde)
    else:
        return []

    if goal_position is None:
        return []
    moves = {
        HC.N: [(0, 1), (0, 0), (0, 0)],
        HC.E: [(1, 0), (0, 0), (0, 0)],
        HC.W: [(-1, 0), (0, 0), (0, 0)],
        HC.S: [(0, -1), (0, 0), (0, 0)],
    }

    neutralized_guards = []

    def is_valid_position(position):
        return position in monde and monde[position] != HC.WALL

    def manhattan_distance(position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

    def get_world_size(monde):
        m = max(coord[0] for coord in monde.keys())
        n = max(coord[1] for coord in monde.keys())
        return m, n

    m,n = get_world_size(monde)

    def get_world_content(monde, guard_x, guard_y):
        if (guard_x, guard_y) in monde:
            return monde[(guard_x, guard_y)]
        else:
            return None

    def get_guard_offset(guard):
        if guard == HC.GUARD_N:
            offset = 0, 1
        elif guard == HC.GUARD_E:
            offset = 1, 0
        elif guard == HC.GUARD_S:
            offset = 0, -1
        elif guard == HC.GUARD_W:
            offset = -1, 0

    def get_guard_vision(monde, guard_x, guard_y):
        guard = get_world_content(monde,guard_x, guard_y)
        offset_x, offset_y = get_guard_offset(guard)
        pos = (guard_x, guard_y)
        x, y = pos
        vision = [(pos, get_world_content(monde,x, y))]

        pos = x + offset_x, y + offset_y
        x, y = pos
        if n > x >= 0 and m > y >= 0:
            vision.append((pos, get_world_content(monde,x, y)))
        return vision

    def compute_guards(
        monde,
    ) -> Dict[Tuple[int, int], List[Tuple[Tuple[int, int], HC]]]:
        locations = {}
        for l_index, l in enumerate(monde):
            for c_index, c in enumerate(l):
                if (
                    c == HC.GUARD_N
                    or c == HC.GUARD_W
                    or c == HC.GUARD_E
                    or c == HC.GUARD_S
                ):
                    guard_x, guard_y = (c_index, m - l_index - 1)
                    locations[(guard_x, guard_y)] = get_guard_vision(
                        guard_x, guard_y
                    )
        return locations

    guards = compute_guards(monde)
    is_in_guard_range = False

    def is_obstacle_in_path(position1, position2):
        x1, y1 = position1
        x2, y2 = position2

        # Vérification des obstacles horizontaux (même ligne)
        if y1 == y2:
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            for x in range(min_x, max_x + 1):
                if get_world_content(monde, x, y1) == HC.WALL:
                    return True

        # Vérification des obstacles verticaux (même colonne)
        if x1 == x2:
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            for y in range(min_y, max_y + 1):
                if get_world_content(monde, x1, y) == HC.WALL:
                    return True

        # Pas d'obstacle trouvé
        return False

    def seen_by_guard_num(position, guards) -> int:
        count = 0
        x, y = position
        if get_world_content(monde, x, y) not in [HC.CIVIL_N, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W]:
            for guard_positions in guards.values():
                for (l, c), guard_type in guard_positions:
                    if guard_type in [HC.GUARD_N, HC.GUARD_E, HC.GUARD_S, HC.GUARD_W]:
                        if guard_type == HC.GUARD_N:
                            if x == l and y > c and not is_obstacle_in_path(position, (l, c)):
                                count += 1
                        elif guard_type == HC.GUARD_E:
                            if y == c and x > l and not is_obstacle_in_path(position, (l, c)):
                                count += 1
                        elif guard_type == HC.GUARD_S:
                            if x == l and y < c and not is_obstacle_in_path(position, (l, c)):
                                count += 1
                        elif guard_type == HC.GUARD_W:
                            if y == c and x < l and not is_obstacle_in_path(position, (l, c)):
                                count += 1
        return count

    def get_civil_offset(civil):
        if civil == HC.CIVIL_N:
            offset = 0, 1
        elif civil == HC.CIVIL_E:
            offset = 1, 0
        elif civil == HC.CIVIL_W:
            offset = 0, -1
        elif civil == HC.CIVIL_S:
            offset = -1, 0

    def get_civil_vision(monde, civil_x, civil_y):
        civil = get_world_content(monde,civil_x, civil_y)
        offset_x, offset_y = get_civil_offset(civil)
        pos = (civil_x, civil_y)
        x, y = pos
        vision = [(pos, get_world_content(monde,x, y))]

        pos = x + offset_x, y + offset_y
        x, y = pos
        if n > x >= 0 and m > y >= 0:
            vision.append((pos, get_world_content(monde,x, y)))
        return vision

    def compute_civils(
        monde,
    ) -> Dict[Tuple[int, int], List[Tuple[Tuple[int, int], HC]]]:
        locations = {}
        for l_index, l in enumerate(monde):
            for c_index, c in enumerate(l):
                if (
                    c == HC.CIVIL_N
                    or c == HC.CIVIL_E
                    or c == HC.CIVIL_S
                    or c == HC.CIVIL_W
                ):

                    civil_x, civil_y = (c_index, m - l_index - 1)
                    locations[(civil_x, civil_y)] = get_civil_vision(
                        civil_x, civil_y
                    )
        return locations

    civils = compute_civils(monde)
    is_in_civil_range = False

    def seen_by_civil_num(position,civils) -> int:
        count = 0
        x, y = position
        if get_world_content(monde, x, y) not in [HC.CIVIL_N, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W]:
            for civils_positions in civils.values():
                for (l, c), civil_type in civils_positions:
                    if civil_type in [HC.CIVIL_N, HC.CIVIL_E, HC.CIVIL_S, HC.CIVIL_W]:
                        if civil_type == HC.CIVIL_N:
                            if x == l and y > c and not is_obstacle_in_path(position, (l, c)):
                                count += 1
                        elif civil_type == HC.CIVIL_E:
                            if y == c and x > l and not is_obstacle_in_path(position, (l, c)):
                                count += 1
                        elif civil_type == HC.CIVIL_S:
                            if x == l and y < c and not is_obstacle_in_path(position, (l, c)):
                                count += 1
                        elif civil_type == HC.CIVIL_W:
                            if y == c and x < l and not is_obstacle_in_path(position, (l, c)):
                                count += 1
        return count


    def get_offset(orientation):
        if orientation in [HC.GUARD_N,HC.CIVIL_N]:
            offset = 0, 1
        elif orientation in [HC.GUARD_E,HC.CIVIL_E]:
            offset = 1, 0
        elif orientation in [HC.GUARD_S,HC.CIVIL_S]:
            offset = 0, -1
        elif orientation in [HC.GUARD_W,HC.CIVIL_W]:
            offset = -1, 0

        return offset

    def update_world_content(monde, x: int, y: int, new_content: HC):
        monde[m - y - 1][x] = new_content
        # comme un objet bloquant la vue peut être retiré, il faut update les visions
        #civils = compute_civils()
        guards = compute_guards()

    def neutralize_guard(position):
        offset_x, offset_y = get_offset(monde[position])
        x, y = position

        if get_world_content(monde,x + offset_x, y + offset_y) not in [
            HC.GUARD_N,
            HC.GUARD_E,
            HC.GUARD_S,
            HC.GUARD_W,
        ] or (x, y) in [
            position for (position, _) in guards[(x + offset_x, y + offset_y)]
        ]:
            return ValueError("Err: invalid move")

        update_world_content(monde,x + offset_x, y + offset_y, HC.EMPTY)

    has_suit = False

    def take_suit(position):
        x, y = position
        if get_world_content(monde, x, y) != HC.SUIT:
            return ValueError("Err: invalid move")
        monde[(x, y)] = HC.EMPTY
        has_suit = True

    costume_worn = False

    def put_on_suit(position):
        if not has_suit:
            return ValueError("Err: invalid move")
        costume_worn = True

    def calculer_penalite(position, action, costume_worn, has_suit):
        is_in_civil_range = False
        is_in_guard_range = False
        penalty = 0
        count_G = seen_by_guard_num(position, guards)
        count_C = seen_by_civil_num(position, civils)
        if count_G > 0:
            is_in_guard_range = True
        if count_C > 0:
            is_in_civil_range = True

        if is_valid_position(position):
            if action == "neutraliser":
                if is_in_guard_range or is_in_civil_range:
                    if costume_worn:
                        penalty += 0
                    else:
                        penalty += 100 * (count_G + count_C)
                else:
                    penalty += 20
            elif action == "mouvement":
                if is_in_guard_range:
                    if not costume_worn:
                        penalty += count_G * 5
                    else:
                        penalty += 1
                else:
                    penalty += 1
            elif action == "prendre_costume":
                take_suit(position)
                if is_in_guard_range:
                    if not costume_worn:
                        penalty += count_G * 5
                    else:
                        penalty += 1
                else:
                    penalty += 1
            elif action == "mettre_costume":
                if not has_suit:
                    ValueError("On ne peu pas porter le costume si on ne l'a pas encore mis")
                else:
                    put_on_suit(position)
                    if is_in_guard_range:
                        penalty += count_G * 5
                    elif is_in_guard_range or is_in_civil_range:
                        penalty += 100 * (count_G + count_C)
                    else:
                        penalty += 1
        return penalty

    def astar_(monde, start_node, goal_position):
        open_set = PriorityQueue()
        open_set.put(start_node)
        closed_set = set()

        while not open_set.empty():
            current_node = open_set.get()

            if current_node.position == goal_position:
                path = []
                while current_node.parent:
                    if  path != [] and monde.get(path[-1]) in [HC.GUARD_N, HC.GUARD_W, HC.GUARD_S, HC.GUARD_E]:
                        neutralized_guards.append(path[-1])
                        neutralize_guard(path[-1])
                    path.append(current_node.position)
                    current_node = current_node.parent
                path.append(start)
                path.reverse()
                return path, neutralized_guards

            closed_set.add(current_node.position)

            for move_direction in moves:
                move = moves[move_direction]
                new_position = (
                    current_node.position[0] + move[0][0],
                    current_node.position[1] + move[0][1]
                )

                if is_valid_position(new_position) and new_position not in closed_set:
                    g_score = current_node.g + 1
                    h_score = manhattan_distance(new_position, goal_position)

                    costume_worn_ = current_node.costume_worn
                    new_penalty1 = calculer_penalite(new_position, "neutraliser", costume_worn_, current_node.has_suit)
                    new_penalty2 = calculer_penalite(new_position, "mouvement", costume_worn_, current_node.has_suit)
                    new_penalty3 = calculer_penalite(new_position, "prendre_costume", costume_worn_,
                                                     current_node.has_suit)
                    new_penalty4 = calculer_penalite(new_position, "mettre_costume", costume_worn_,
                                                     current_node.has_suit)

                    new_penalty = new_penalty1 + new_penalty2 + new_penalty3 + new_penalty4

                    updated_h_score = h_score + new_penalty

                    new_node = Node(
                        new_position,
                        parent=current_node,
                        g=g_score,
                        h=updated_h_score,
                        penalty=new_penalty,
                        action = None
                    )
                    if new_node not in open_set.queue:
                        open_set.put(new_node)
                    elif g_score < new_node.g:
                        open_set.queue.remove(new_node)
                        open_set.put(new_node)

        return [], []

    return astar_(monde, start_node, goal_position)


#Utilisation

hr = HitmanReferee()
start_position = (0,0)

map = complete_map_example

chemin_optimal1, neutralized_guards1 = astar(map, start_position,hr, HC.PIANO_WIRE)


if chemin_optimal1:
    last_position1 = chemin_optimal1[-1]
    chemin_optimal2, neutralized_guards2 = astar(map, last_position1,hr, HC.TARGET)


    if chemin_optimal2:
        last_position2 = chemin_optimal2[-1]
        chemin_optimal3, neutralized_guards3 = astar(map, last_position2,hr, HC.EMPTY)

# Éliminer les doublons de la liste neutralized_guardsF
unique_neutralized_guards1 = set(neutralized_guards1)
unique_neutralized_guards2 = set(neutralized_guards2).difference(unique_neutralized_guards1)
unique_neutralized_guards3 = set(neutralized_guards3).difference(unique_neutralized_guards2)

# Convertir les ensembles en listes
neutralized_guards1 = list(unique_neutralized_guards1)
neutralized_guards2 = list(unique_neutralized_guards2)
neutralized_guards3 = list(unique_neutralized_guards3)

print("Voici le chemin final :")
print("neutralized_guards1 :", neutralized_guards1)
print("neutralized_guards2 :", neutralized_guards2)
print("neutralized_guards3 :", neutralized_guards3)
def convert_chemin_to_action(chemin :List[Tuple[int, int]],chemin2 :List[Tuple[int, int]],chemin3 :List[Tuple[int, int]],neutralized_guards1 :List[Tuple[int, int]],neutralized_guards2 :List[Tuple[int, int]],neutralized_guards3 :List[Tuple[int, int]] , hr: HitmanReferee):
    status = hr.start_phase2()
    print(status)
    orientation = status["orientation"]
    for i in range(len(chemin) - 1):
        pos1 = chemin[i]
        pos2 = chemin[i + 1]
        for i in range(len(neutralized_guards1)):
            if pos2 == neutralized_guards1[i]:
                if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
                    if orientation == HC.N:
                        pass
                    elif orientation == HC.S:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.N
                    elif orientation == HC.E:
                        hr.turn_anti_clockwise()
                        orientation = HC.N
                    elif orientation == HC.W:
                        hr.turn_clockwise()
                        orientation = HC.N
                    hr.neutralize_guard()
                elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:
                    if orientation == HC.N:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.S
                    elif orientation == HC.S:
                        pass
                    elif orientation == HC.E:
                        hr.turn_clockwise()
                        orientation = HC.S
                    elif orientation == HC.W:
                        hr.turn_anti_clockwise()
                        orientation = HC.S
                    hr.neutralize_guard()
                elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:
                    if orientation == HC.N:
                        hr.turn_clockwise()
                        orientation = HC.E
                    elif orientation == HC.S:
                        hr.turn_anti_clockwise()
                        orientation = HC.E
                    elif orientation == HC.E:
                        pass
                    elif orientation == HC.W:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.E
                    hr.neutralize_guard()
                elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
                    if orientation == HC.N:
                        hr.turn_anti_clockwise()
                        orientation = HC.W
                    elif orientation == HC.S:
                        hr.turn_clockwise()
                        orientation = HC.W
                    elif orientation == HC.E:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.W
                    elif orientation == HC.W:
                        pass
                    hr.neutralize_guard()
        print()
        print("Hitman regarder vers :", orientation)
        print("Hitman se trouve sur la case :", pos1)
        if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
            print("Hitman se deplace vers le haut 1 :  ", pos2)
            if orientation == HC.E:
                print("hitman tourne puis avance droit")
                hr.turn_anti_clockwise()
                hr.move()
                orientation = HC.N
            elif orientation == HC.N:
                print("hitman  avance")
                print(hr.move())
                orientation = HC.N
            elif orientation == HC.S:
                print("hitman tourne a gauche puis avance")
                hr.turn_anti_clockwise()
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.N
            elif orientation == HC.W:
                print("hitman fait demi tour puis avance")
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.N
        elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:
            print("Hitman se deplace vers le bas: 2", pos2)
            if orientation == HC.E:
                print("hitman fait demi tour puis avance")
                hr.turn_clockwise()

                print(hr.move())
                orientation = HC.S
            elif orientation == HC.N:
                print("hitman tourne a gauche puis avance")
                hr.turn_anti_clockwise()
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.S
            elif orientation == HC.S:
                print("hitman tourne a droite puis avance")

                print(hr.move())
                orientation = HC.S
            elif orientation == HC.W:
                print("hitman avance droit")
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.S
        elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:
            print("Hitman se deplace vers la droite 3: ", pos2)
            if orientation == HC.E:
                print("hitman tourne a gauche puis avance")

                print(hr.move())
                orientation = HC.E
            elif orientation == HC.N:
                print("hitman tourne puis avance droit")
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.E
            elif orientation == HC.S:
                print("hitman fait demi tour puis avance")
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.E
            elif orientation == HC.W:
                print("hitman tourne a droite puis avance")
                hr.turn_anti_clockwise()
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.E
        elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
            print("Hitman se deplace vers la gauche 4: ", pos2)
            if orientation == HC.E:
                print("hitman tourne a droite puis avance")
                hr.turn_clockwise()
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.W
            elif orientation == HC.N:
                print("hitman fait demi tour puis avance")
                hr.turn_anti_clockwise()

                print(hr.move())
                orientation = HC.W
            elif orientation == HC.S:
                print("hitman avance droit")
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.W
            elif orientation == HC.W:
                print("hitman tourne a gauche puis avance")
                print(hr.move())
                orientation = HC.W
    print("Hitman est sur la case de la corde ")
    print(hr.take_weapon())

    print("Hitman ramasse la corde")
    print()
    for i in range(len(chemin2) - 1):
        pos1 = chemin2[i]
        pos2 = chemin2[i + 1]
        for i in range(len(neutralized_guards2)):
            if pos2 == neutralized_guards2[i]:
                if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
                    if orientation == HC.N:
                        pass
                    elif orientation == HC.S:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.N
                    elif orientation == HC.E:
                        hr.turn_anti_clockwise()
                        orientation = HC.N
                    elif orientation == HC.W:
                        hr.turn_clockwise()
                        orientation = HC.N
                    hr.neutralize_guard()
                elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:
                    if orientation == HC.N:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.S
                    elif orientation == HC.S:
                        pass
                    elif orientation == HC.E:
                        hr.turn_clockwise()
                        orientation = HC.S
                    elif orientation == HC.W:
                        hr.turn_anti_clockwise()
                        orientation = HC.S
                    hr.neutralize_guard()
                elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:
                    if orientation == HC.N:
                        hr.turn_clockwise()
                        orientation = HC.E
                    elif orientation == HC.S:
                        hr.turn_anti_clockwise()
                        orientation = HC.E
                    elif orientation == HC.E:
                        pass
                    elif orientation == HC.W:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.E
                    hr.neutralize_guard()
                elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
                    if orientation == HC.N:
                        hr.turn_anti_clockwise()
                        orientation = HC.W
                    elif orientation == HC.S:
                        hr.turn_clockwise()
                        orientation = HC.W
                    elif orientation == HC.E:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.W
                    elif orientation == HC.W:
                        pass
                    hr.neutralize_guard()
        print("Hitman regarder vers :", orientation)
        print("Hitman se trouve sur la case :", pos1)
        if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
            print("Hitman se deplace vers le haut 1 :  ", pos2)
            if orientation == HC.E:
                print("hitman tourne puis avance droit")
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.N
            elif orientation == HC.N:
                print("hitman  avance")
                print(hr.move())
                orientation = HC.N
            elif orientation == HC.S:
                print("hitman tourne a gauche puis avance")
                hr.turn_anti_clockwise()
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.N
            elif orientation == HC.W:
                print("hitman fait demi tour puis avance")
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.N
        elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:
            print("Hitman se deplace vers le bas: 2", pos2)
            if orientation == HC.E:
                print("hitman fait demi tour puis avance")
                hr.turn_clockwise()

                print(hr.move())
                orientation = HC.S
            elif orientation == HC.N:
                print("hitman tourne a gauche puis avance")
                hr.turn_anti_clockwise()
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.S
            elif orientation == HC.S:
                print("hitman tourne a droite puis avance")

                print(hr.move())
                orientation = HC.S
            elif orientation == HC.W:
                print("hitman avance droit")
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.S
        elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:
            print("Hitman se deplace vers la droite 3: ", pos2)
            if orientation == HC.E:
                print("hitman tourne a gauche puis avance")

                print(hr.move())
                orientation = HC.E
            elif orientation == HC.N:
                print("hitman tourne puis avance droit")
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.E
            elif orientation == HC.S:
                print("hitman fait demi tour puis avance")
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.E
            elif orientation == HC.W:
                print("hitman tourne a droite puis avance")
                hr.turn_anti_clockwise()
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.E
        elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
            print("Hitman se deplace vers la gauche 4: ", pos2)
            if orientation == HC.E:
                print("hitman tourne a droite puis avance")
                hr.turn_clockwise()
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.W
            elif orientation == HC.N:
                print("hitman fait demi tour puis avance")
                hr.turn_anti_clockwise()

                print(hr.move())
                orientation = HC.W
            elif orientation == HC.S:
                print("hitman avance droit")
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.W
            elif orientation == HC.W:
                print("hitman tourne a gauche puis avance")
                print(hr.move())
                orientation = HC.W
    print("Hitman est sur la case de la cible ")
    print(hr.kill_target())

    for i in range(len(chemin3) - 1):

        pos1 = chemin3[i]
        pos2 = chemin3[i + 1]
        for i in range(len(neutralized_guards3)):
            if pos2 == neutralized_guards3[i]:
                if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
                    if orientation == HC.N:
                        pass
                    elif orientation == HC.S:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.N
                    elif orientation == HC.E:
                        hr.turn_anti_clockwise()
                        orientation = HC.N
                    elif orientation == HC.W:
                        hr.turn_clockwise()
                        orientation = HC.N
                    hr.neutralize_guard()
                elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:
                    if orientation == HC.N:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.S
                    elif orientation == HC.S:
                        pass
                    elif orientation == HC.E:
                        hr.turn_clockwise()
                        orientation = HC.S
                    elif orientation == HC.W:
                        hr.turn_anti_clockwise()
                        orientation = HC.S
                    hr.neutralize_guard()
                elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:
                    if orientation == HC.N:
                        hr.turn_clockwise()
                        orientation = HC.E
                    elif orientation == HC.S:
                        hr.turn_anti_clockwise()
                        orientation = HC.E
                    elif orientation == HC.E:
                        pass
                    elif orientation == HC.W:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.E
                    hr.neutralize_guard()
                elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
                    if orientation == HC.N:
                        hr.turn_anti_clockwise()
                        orientation = HC.W
                    elif orientation == HC.S:
                        hr.turn_clockwise()
                        orientation = HC.W
                    elif orientation == HC.E:
                        hr.turn_anti_clockwise()
                        hr.turn_anti_clockwise()
                        orientation = HC.W
                    elif orientation == HC.W:
                        pass
                    hr.neutralize_guard()
        print()
        # print(f"Hitman a pris  {malus} de penlaitee")
        print("Hitman regarde dans la direction : ", orientation)
        pos = hr
        print("Hitman se trouve sur la case :", pos1)

        if pos1[0] == pos2[0] and pos1[1] + 1 == pos2[1]:
            print("Hitman se deplace vers le haut 1 :  ", pos2)
            if orientation == HC.E:
                print("hitman tourne puis avance droit")
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.N
            elif orientation == HC.N:
                print("hitman  avance")
                print(hr.move())
                orientation = HC.N
            elif orientation == HC.S:
                print("hitman tourne a gauche puis avance")
                hr.turn_anti_clockwise()
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.N
            elif orientation == HC.W:
                print("hitman fait demi tour puis avance")
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.N
        elif pos1[0] == pos2[0] and pos1[1] - 1 == pos2[1]:
            print("Hitman se deplace vers le bas: 2", pos2)
            if orientation == HC.E:
                print("hitman fait demi tour puis avance")
                hr.turn_clockwise()

                print(hr.move())
                orientation = HC.S
            elif orientation == HC.N:
                print("hitman tourne a gauche puis avance")
                hr.turn_anti_clockwise()
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.S
            elif orientation == HC.S:
                print("hitman tourne a droite puis avance")

                print(hr.move())
                orientation = HC.S
            elif orientation == HC.W:
                print("hitman avance droit")
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.S
        elif pos1[0] + 1 == pos2[0] and pos1[1] == pos2[1]:
            print("Hitman se deplace vers la droite 3: ", pos2)
            if orientation == HC.E:
                print("hitman tourne a gauche puis avance")

                print(hr.move())
                orientation = HC.E
            elif orientation == HC.N:
                print("hitman tourne puis avance droit")
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.E
            elif orientation == HC.S:
                print("hitman fait demi tour puis avance")
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.E
            elif orientation == HC.W:
                print("hitman tourne a droite puis avance")
                hr.turn_anti_clockwise()
                hr.turn_anti_clockwise()
                print(hr.move())
                orientation = HC.E
        elif pos1[0] - 1 == pos2[0] and pos1[1] == pos2[1]:
            print("Hitman se deplace vers la gauche 4: ", pos2)
            if orientation == HC.E:
                print("hitman tourne a droite puis avance")
                hr.turn_clockwise()
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.W
            elif orientation == HC.N:
                print("hitman fait demi tour puis avance")
                hr.turn_anti_clockwise()

                print(hr.move())
                orientation = HC.W
            elif orientation == HC.S:
                print("hitman avance droit")
                hr.turn_clockwise()
                print(hr.move())
                orientation = HC.W
            elif orientation == HC.W:
                print("hitman tourne a gauche puis avance")
                print(hr.move())
                orientation = HC.W

    print(hr.end_phase2())


def inverser_tuples(liste):
    resultat = []
    for tuple_ in liste:
        nouvel_tuple = (tuple_[1], tuple_[0])
        resultat.append(nouvel_tuple)
    return resultat


def main():
    hr = HitmanReferee()
    print(f"liste renvoye par a* {chemin_optimal1}")
    print(f"liste neutraliser garde {neutralized_guards1}")
    print(f"liste renvoye par a* 2 {chemin_optimal2}")
    print(f"liste neutraliser garde 2 {neutralized_guards2}")
    print(f"liste renvoye par a* 3 {chemin_optimal3}")
    print(f"liste neutraliser garde 3 {neutralized_guards3}")
    convert_chemin_to_action(chemin_optimal1, chemin_optimal2, chemin_optimal3,neutralized_guards1,neutralized_guards2,neutralized_guards3, hr)

if __name__ == "__main__":
    main()
