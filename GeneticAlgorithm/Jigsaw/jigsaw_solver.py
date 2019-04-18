from GeneticAlgorithm.Jigsaw.jigsaw import Game  # if executing from directory root
# from jigsaw import Game  # if executing from current directory

import numpy as np
import math
import random; random.seed(4)


class Solver:
    def __init__(self, pieces, viz_func,
                 pop_size=100, random_size=0.2, n_gens=10):

        self.threshold = self.generate_threshold(pieces, p=93)
        self.piece_edges = np.array([np.array([
            piece[0, :],
            piece[:, -1],
            piece[-1, :],
            piece[:, 0]
        ]) for piece in pieces])
        self.n_segments = int(math.sqrt(len(pieces)))

        self.viz_func = viz_func

        self.pop_size = pop_size
        self.random_size = random_size
        self.n_gens = n_gens

        self.prev_pop = None
        self.temp_pop = []

    def fitness(self, ind):
        """
        Return two 2d matrices of differences between adjacent pieces in an
        individual in a given population.
        The first matrix has `n_segments` rows and `n_segments - 1` columns,
        holding differences between horizontally adjacent pieces.
        The second matrix has `n_segments - 1` rows and `n_segments` columns,
        holding differences between vertically adjacent pieces.
        """

        def get_difference(edge1, edge2):
            """Return sum of squares of differences."""
            return np.sum((edge1 - edge2) ** 2)

        indices, orientations = ind  # chromosome

        # Convert chromosome to piece representation
        ind_piece_edges = []
        for row in range(self.n_segments):
            for col in range(self.n_segments):
                piece_id = indices[row, col]
                ind_piece_edges.append(np.roll(
                    self.piece_edges[piece_id],
                    orientations[piece_id],
                    axis=0
                ))

        ind_piece_edges = np.array(ind_piece_edges).reshape(
            (self.n_segments, self.n_segments, 4, -1))

        horizontal_fitness = np.zeros((self.n_segments, self.n_segments - 1))
        vertical_fitness = np.zeros((self.n_segments - 1, self.n_segments))

        for i in range(self.n_segments - 1):
            for j in range(self.n_segments):
                horizontal_fitness[j, i] = get_difference(
                    ind_piece_edges[j, i][1], ind_piece_edges[j, i + 1][3]
                )
                vertical_fitness[i, j] = get_difference(
                    ind_piece_edges[i, j][2], ind_piece_edges[i + 1, j][0]
                )

        return horizontal_fitness, vertical_fitness

    def get_ind_stats(self, ind):
        """
        Return various statistics inferred from the fitness matrix pair of a
        given individual.
            - Cluster matrix: adjacent matching pieces have the same index.
            - Cluster ID set: set of cluster IDs in the cluster matrix.
            - Cluster fitnesses: average of all differences in adjacent
            matching pieces in each cluster.
            - Dictionary mapping a cluster ID to a set of piece IDs in that
            cluster.
            - Match-orientation array: Each piece index maps to a 4-element
            array containing either `None` (if the specific side is not
            matched) or a tuple (ID of matching piece, fitness).
                - 1st element: match at top, 2nd: match on right, etc.
                - The orientations are individually specific, and don't
                correspond to the original orientations.
        """

        # Generate info on good matches
        horizontal_fitness, vertical_fitness = self.fitness(ind)
        match_horizontal = horizontal_fitness <= self.threshold
        match_vertical = vertical_fitness <= self.threshold

        # Initialize stats
        cluster_matrix = np.zeros(
            (self.n_segments, self.n_segments), dtype=int)

        piece_indices = ind[0]
        match_orientations = np.array([np.array([
            None for _ in range(4)
        ]) for __ in range(piece_indices.size)])

        cluster_id_set = set()
        temp_cluster_id = 1

        # Fill in values for the cluster matrix and match-orientation array
        for i in range(match_horizontal.shape[0]):
            for j in range(match_horizontal.shape[1]):
                if match_horizontal[i, j]:
                    # When both matching pieces don't have a cluster ID yet,
                    # we use the current ID and increment it afterwards.
                    if cluster_matrix[i, j] == cluster_matrix[i, j + 1] == 0:
                        cluster_matrix[i, j] = temp_cluster_id
                        cluster_matrix[i, j + 1] = temp_cluster_id
                        cluster_id_set.add(temp_cluster_id)
                        temp_cluster_id += 1
                    # When only one of the matching pieces has a cluster ID,
                    # we assign the ID to the other piece.
                    elif cluster_matrix[i, j] == 0 != cluster_matrix[i, j + 1]:
                        cluster_matrix[i, j] = cluster_matrix[i, j + 1]
                    elif cluster_matrix[i, j] != 0 == cluster_matrix[i, j + 1]:
                        cluster_matrix[i, j + 1] = cluster_matrix[i, j]
                    # When both match pieces already have a cluster ID,
                    # we change all IDs of the first piece to that of the other
                    # piece, and remove that ID from the cluster ID set.
                    elif cluster_matrix[i, j] != cluster_matrix[i, j + 1]:
                        cluster_id_set.remove(cluster_matrix[i, j])
                        cluster_matrix[
                            cluster_matrix == cluster_matrix[i, j]
                        ] = cluster_matrix[i, j + 1]

                    match_orientations[piece_indices[i, j]][1] = (
                        piece_indices[i, j + 1], horizontal_fitness[i, j]
                    )
                    match_orientations[piece_indices[i, j + 1]][3] = (
                        piece_indices[i, j], horizontal_fitness[i, j]
                    )

        for i in range(match_vertical.shape[0]):
            for j in range(match_vertical.shape[1]):
                if match_vertical[i, j]:
                    if cluster_matrix[i, j] == cluster_matrix[i + 1, j] == 0:
                        cluster_matrix[i, j] = temp_cluster_id
                        cluster_matrix[i + 1, j] = temp_cluster_id
                        cluster_id_set.add(temp_cluster_id)
                        temp_cluster_id += 1
                    elif cluster_matrix[i, j] == 0 != cluster_matrix[i + 1, j]:
                        cluster_matrix[i, j] = cluster_matrix[i + 1, j]
                    elif cluster_matrix[i, j] != 0 == cluster_matrix[i + 1, j]:
                        cluster_matrix[i + 1, j] = cluster_matrix[i, j]
                    elif cluster_matrix[i, j] != cluster_matrix[i + 1, j]:
                        cluster_id_set.remove(cluster_matrix[i, j])
                        cluster_matrix[
                            cluster_matrix == cluster_matrix[i, j]
                        ] = cluster_matrix[i + 1, j]

                    match_orientations[piece_indices[i, j]][2] = (
                        piece_indices[i + 1, j], vertical_fitness[i, j]
                    )
                    match_orientations[piece_indices[i + 1, j]][0] = (
                        piece_indices[i, j], vertical_fitness[i, j]
                    )

        # Calculate fitness for each cluster and generate the
        # cluster ID - piece set dictionary
        cluster_fitnesses = {}
        cluster_to_piece_set = {}
        for cluster_id in cluster_id_set:
            cluster_fitnesses[cluster_id] = [0, 0]
            cluster_to_piece_set[cluster_id] = set()

        for i in range(self.n_segments):
            for j in range(self.n_segments):
                temp_cluster_id = cluster_matrix[i, j]

                if temp_cluster_id:
                    cluster_to_piece_set[temp_cluster_id].add(
                        piece_indices[i, j])

                    for item in match_orientations[piece_indices[i, j]]:
                        if item is not None:
                            cluster_fitnesses[temp_cluster_id][0] += item[1]
                            cluster_fitnesses[temp_cluster_id][1] += 1

        for cluster_id in cluster_id_set:
            fitness_sum, fitness_count = cluster_fitnesses[cluster_id]
            if fitness_count == 0:
                del cluster_fitnesses[cluster_id]
            else:
                cluster_fitnesses[cluster_id] = fitness_sum / fitness_count

        return (cluster_matrix, cluster_id_set, cluster_fitnesses,
                cluster_to_piece_set, match_orientations)

    def crossover(self, parent1, parent2, tolerance=10):
        """
        Return a randomly generated child that preserves all good matches
        from both parents and attempts to merge all mergeable clusters.


        A low value of threshold can lead to clusters being too large to fit in
        a child, which would also make the function hang. This is addressed by
        `tolerance`: if the function doesn't return after a number of tries,
        then return -1.
        """
        def conflict_check(piece_set_intersection):
            """
            Precondition: intersection is not empty.
            Determine whether two clusters are mergeable.
            """
            for piece_id in piece_set_intersection:
                parent1_subjective_orientation = parent1_match_orientations[piece_id]
                parent2_subject_orientation = parent2_match_orientations[piece_id]

                parent1_objective_orientation = np.roll(
                    parent1_subjective_orientation,
                    - parent1_orientations[piece_id]
                )
                parent2_objective_orientation = np.roll(
                    parent2_subject_orientation,
                    - parent2_orientations[piece_id]
                )

                for i in range(4):
                    if parent1_objective_orientation[i] is not None\
                            and parent2_objective_orientation[i] is not None\
                            and parent1_objective_orientation[i] != parent2_objective_orientation[i]:

                        return True

            return False

        def remove_cluster(cluster_id, piece_indices, cluster_matrix,
                           cluster_id_set, cluster_fitnesses,
                           cluster_to_piece_set, match_orientations):
            """
            Remove information regarding a specific cluster ID from all
            individual stats.
            """

            for i in range(cluster_matrix.shape[0]):
                for j in range(cluster_matrix.shape[1]):
                    if cluster_matrix[i, j] == cluster_id:
                        match_orientations[piece_indices[i, j]] = np.array(
                            [None for _ in range(4)]
                        )

            cluster_matrix[cluster_matrix == cluster_id] = 0
            cluster_id_set.remove(cluster_id)
            del cluster_fitnesses[cluster_id]
            del cluster_to_piece_set[cluster_id]

        def generate_child(child_objective_match_orientations,
                           parent1_cluster_to_piece_set,
                           parent2_cluster_to_piece_set,
                           parent1_orientations, parent2_orientations):
            """
            Return a random child that preserves all good clusters from an
            objective match-orientation array.
            """

            indices = np.array([[None for _ in range(self.n_segments)]
                               for __ in range(self.n_segments)])

            remain_piece_set = set([i for i in range(self.n_segments ** 2)])

            def recur_shift_cluster(cluster_id, direction):
                """
                Try to shift all pieces in a cluster in the current solution in
                a direction. (0 --> up, 1--> right, etc.)
                Return `None` if successfully shifted, -1 if conflicting with
                bounds.
                """

                nonlocal indices

                row_change = 0
                col_change = 0
                if direction == 0:
                    row_change -= 1
                elif direction == 1:
                    col_change += 1
                elif direction == 2:
                    row_change += 1
                else:
                    col_change -= 1

                bound_conflict = False
                cluster_conflict = False
                conflicting_cluster_id_set = set()

                for row in range(self.n_segments):
                    if bound_conflict:
                        break

                    for col in range(self.n_segments):
                        if indices[row, col] in cluster_to_piece_set[cluster_id]:
                            new_row = row + row_change
                            new_col = col + col_change

                            if new_row < 0 or new_row >= self.n_segments:
                                bound_conflict = True
                                break
                            if new_col < 0 or new_col >= self.n_segments:
                                bound_conflict = True
                                break

                            if indices[new_row, new_col] is not None \
                                    and piece_cluster_id[indices[row, col]] \
                                    != piece_cluster_id[indices[new_row, new_col]]:

                                cluster_conflict = True
                                conflicting_cluster_id_set.add(
                                    piece_cluster_id[indices[new_row, new_col]]
                                )

                if bound_conflict:
                    return -1

                if cluster_conflict:
                    for conflicting_cluster_id in conflicting_cluster_id_set:
                        recur_shift_result = recur_shift_cluster(
                            conflicting_cluster_id, direction)
                        if recur_shift_result == -1:
                            return -1

                new_indices = np.copy(indices)
                for row in range(self.n_segments):
                    for col in range(self.n_segments):
                        if indices[row, col] in cluster_to_piece_set[cluster_id]:
                            new_row = row + row_change
                            new_col = col + col_change

                            new_indices[new_row, new_col] = indices[row, col]
                            if new_indices[row, col] == indices[row, col]:
                                new_indices[row, col] = None

                indices = new_indices

            def recur_insert_piece(piece_id, row, col, direction):
                """
                Put a piece in a specific location in the solution.
                Return `None` if successful.
                Return `(row_change, col_change)` if successful but shifted.
                Return -1 if the insertion is recursively impossible.
                """

                nonlocal indices

                if piece_id not in remain_piece_set:
                    return

                # If the location is out of bound
                if row < 0 or row >= self.n_segments \
                        or col < 0 or col >= self.n_segments:

                    recur_shift_result = recur_shift_cluster(
                        piece_cluster_id[piece_id],
                        (direction + 2) % 4
                    )

                    if recur_shift_result == -1:
                        return -1

                    overall_row_change = 0
                    overall_col_change = 0
                    if direction == 0:
                        overall_row_change += 1
                    elif direction == 1:
                        overall_col_change -= 1
                    elif direction == 2:
                        overall_row_change -= 1
                    else:
                        overall_col_change += 1

                    if direction == 0:
                        recur_insert_result = recur_insert_piece(
                            piece_id, row + 1, col, 0)
                    elif direction == 1:
                        recur_insert_result = recur_insert_piece(
                            piece_id, row, col - 1, 1)
                    elif direction == 2:
                        recur_insert_result = recur_insert_piece(
                            piece_id, row - 1, col, 2)
                    else:
                        recur_insert_result = recur_insert_piece(
                            piece_id, row, col + 1, 3)

                    if recur_insert_result == -1:
                        return -1

                    return (overall_row_change + recur_insert_result[0],
                            overall_col_change + recur_insert_result[1])

                # If the location is empty
                if indices[row, col] is None:
                    indices[row, col] = piece_id
                    remain_piece_set.remove(piece_id)

                    overall_row_change = 0
                    overall_col_change = 0
                    for i in range(4):
                        match_orientation = child_subjective_match_orientations[piece_id][i]
                        if match_orientation is not None:
                            match_piece_id, _ = match_orientation
                            if i == 0:
                                recur_insert_result = recur_insert_piece(
                                    match_piece_id, row - 1, col, 0)
                            elif i == 1:
                                recur_insert_result = recur_insert_piece(
                                    match_piece_id, row, col + 1, 1)
                            elif i == 2:
                                recur_insert_result = recur_insert_piece(
                                    match_piece_id, row + 1, col, 2)
                            else:
                                recur_insert_result = recur_insert_piece(
                                    match_piece_id, row, col - 1, 3)

                            if recur_insert_result == -1:
                                return -1

                            if recur_insert_result is not None:
                                row_change, col_change = recur_insert_result

                                overall_col_change += row_change
                                overall_col_change += col_change

                                row += row_change
                                col += col_change

                    return overall_row_change, overall_col_change

                # If there is a conflict with another cluster
                saved_indices = np.copy(indices)

                # Try shifting the conflicting cluster in the same direction
                recur_shift_result = recur_shift_cluster(
                    piece_cluster_id[indices[row, col]], direction)

                # If successful, try to insert the original piece again
                if recur_shift_result is None:
                    return recur_insert_piece(piece_id, row, col, direction)

                # If failed, try shifting the original cluster in the opposite
                # direction
                indices = saved_indices
                recur_shift_result = recur_shift_cluster(
                    piece_cluster_id[piece_id], (direction + 2) % 4)

                if recur_shift_result == -1:
                    return -1

                overall_row_change = 0
                overall_col_change = 0
                if direction == 0:
                    overall_row_change += 1
                elif direction == 1:
                    overall_col_change -= 1
                elif direction == 2:
                    overall_row_change -= 1
                else:
                    overall_col_change += 1

                # Attempt to insert the piece again after the shift
                if direction == 0:
                    recur_insert_result = recur_insert_piece(
                        piece_id, row + 1, col, 0)
                elif direction == 1:
                    recur_insert_result = recur_insert_piece(
                        piece_id, row, col - 1, 1)
                elif direction == 2:
                    recur_insert_result = recur_insert_piece(
                        piece_id, row - 1, col, 2)
                else:
                    recur_insert_result = recur_insert_piece(
                        piece_id, row, col + 1, 3)

                if recur_insert_result == -1:
                    return -1

                return (overall_row_change + recur_insert_result[0],
                        overall_col_change + recur_insert_result[1])

            def cluster_relative_orientation_check():
                for piece_id1 in range(self.n_segments ** 2 - 1):
                    for piece_id2 in range(piece_id1 + 1, self.n_segments ** 2):
                        child_orientation_d = (piece_orientation[piece_id1]
                                               - piece_orientation[piece_id2]) \
                                              % 4

                        if parent1_piece_to_cluster_id[piece_id1] != 0 \
                                and parent1_piece_to_cluster_id[piece_id2] != 0 \
                                and parent1_piece_to_cluster_id[piece_id1] == parent1_piece_to_cluster_id[piece_id2]:

                            parent1_orientation_d = (parent1_orientations[piece_id1]
                                                     - parent1_orientations[piece_id2]) \
                                                    % 4

                            if parent2_piece_to_cluster_id[piece_id1] != 0 \
                                    and parent2_piece_to_cluster_id[piece_id2] != 0 \
                                    and parent2_piece_to_cluster_id[piece_id1] \
                                    == parent2_piece_to_cluster_id[piece_id2]:

                                parent2_orientation_d = (parent2_orientations[piece_id1]
                                                         - parent2_orientations[piece_id2]) \
                                                        % 4

                                if parent1_orientation_d != parent2_orientation_d:
                                    return -1

                            if child_orientation_d != parent1_orientation_d:
                                # print(f'Conflict between {piece_id1} and {piece_id2} with parent1')
                                if not piece_check[piece_id2]:
                                    piece_orientation[piece_id2] = (piece_orientation[piece_id1]
                                                                    - parent1_orientation_d) \
                                                                   % 4
                                    piece_check[piece_id2] = True

                                elif not piece_check[piece_id1]:
                                    piece_orientation[piece_id1] = (piece_orientation[piece_id]
                                                                    + parent1_orientation_d) \
                                                                   % 4
                                    piece_check[piece_id1] = True

                                else:
                                    return -1

                                return False

                        if parent2_piece_to_cluster_id[piece_id1] != 0 \
                                and parent2_piece_to_cluster_id[piece_id2] != 0 \
                                and parent2_piece_to_cluster_id[piece_id1] == parent2_piece_to_cluster_id[piece_id2]:

                            parent2_orientation_d = (parent2_orientations[piece_id1]
                                                     - parent2_orientations[piece_id2]) \
                                                    % 4

                            if child_orientation_d != parent2_orientation_d:
                                # print(f'Conflict between {piece_id1} and {piece_id2} with parent2')
                                if not piece_check[piece_id2]:
                                    piece_orientation[piece_id2] = (piece_orientation[piece_id1]
                                                                    - parent2_orientation_d) \
                                                                   % 4
                                    piece_check[piece_id2] = True

                                elif not piece_check[piece_id1]:
                                    piece_orientation[piece_id1] = (piece_orientation[piece_id]
                                                                    + parent2_orientation_d) \
                                                                   % 4
                                    piece_check[piece_id1] = True

                                else:
                                    return -1

                                return False

                return True

            piece_cluster_id = np.zeros(
                (len(child_objective_match_orientations,)), dtype=int)

            temp_cluster_id = 1
            for piece_id in range(len(child_objective_match_orientations)):
                for item in child_objective_match_orientations[piece_id]:
                    if item is not None:
                        match_piece_id, _ = item

                        if piece_cluster_id[piece_id] == 0:
                            if piece_cluster_id[match_piece_id] == 0:
                                piece_cluster_id[piece_id] = temp_cluster_id
                                piece_cluster_id[match_piece_id] = temp_cluster_id
                                temp_cluster_id += 1
                            else:
                                piece_cluster_id[piece_id] = piece_cluster_id[match_piece_id]

                        elif piece_cluster_id[match_piece_id] == 0:
                            piece_cluster_id[match_piece_id] = piece_cluster_id[piece_id]

                        elif piece_cluster_id[piece_id] != piece_cluster_id[match_piece_id]:
                            for i in range(len(piece_cluster_id)):
                                if piece_cluster_id[i] == piece_cluster_id[match_piece_id]:
                                    piece_cluster_id[i] = piece_cluster_id[piece_id]

            cluster_id_set = set(piece_cluster_id)
            cluster_id_set.discard(0)  # remove 0 if exist

            cluster_to_piece_set = {}
            for piece_id in range(self.n_segments ** 2):
                temp_cluster_id = piece_cluster_id[piece_id]
                if temp_cluster_id != 0:
                    if temp_cluster_id not in cluster_to_piece_set:
                        cluster_to_piece_set[temp_cluster_id] = {piece_id}
                    else:
                        cluster_to_piece_set[temp_cluster_id].add(piece_id)

            cluster_to_orientation = {
                cluster_id: np.random.randint(0, 4)
                for cluster_id in cluster_id_set
            }
            piece_orientation = np.array([
                cluster_to_orientation[piece_cluster_id[piece_id]]
                if piece_cluster_id[piece_id] != 0
                else np.random.randint(0, 4)
                for piece_id in range(self.n_segments ** 2)
            ])

            parent1_piece_to_cluster_id = {}
            parent2_piece_to_cluster_id = {}
            for cluster_id, piece_set in parent1_cluster_to_piece_set.items():
                for piece_id in piece_set:
                    parent1_piece_to_cluster_id[piece_id] = cluster_id
            for cluster_id, piece_set in parent2_cluster_to_piece_set.items():
                for piece_id in piece_set:
                    parent2_piece_to_cluster_id[piece_id] = cluster_id
            for piece_id in range(self.n_segments ** 2):
                if piece_id not in parent1_piece_to_cluster_id:
                    parent1_piece_to_cluster_id[piece_id] = 0
                if piece_id not in parent2_piece_to_cluster_id:
                    parent2_piece_to_cluster_id[piece_id] = 0

            piece_check = [False for _ in range(self.n_segments ** 2)]
            while not cluster_relative_orientation_check():
                continue

            child_subjective_match_orientations = []
            for i, match_orientation in enumerate(child_objective_match_orientations):
                child_subjective_match_orientations.append(np.roll(
                    match_orientation, piece_orientation[i]
                ))

            child_subjective_match_orientations = np.array(child_subjective_match_orientations)

            for piece_id in range(self.n_segments ** 2):
                if piece_cluster_id[piece_id] != 0:
                    remain_locations = set(map(
                        tuple, np.argwhere(indices == None)))

                    recur_insert_result = -1
                    saved_indices = indices
                    saved_remain_piece_set = remain_piece_set

                    while remain_locations and recur_insert_result == -1:
                        location = random.sample(remain_locations, 1)[0]
                        remain_locations.remove(location)
                        row, col = location

                        indices = np.copy(saved_indices)
                        remain_piece_set = saved_remain_piece_set.copy()

                        recur_insert_result = recur_insert_piece(
                            piece_id, row, col, 0)

                    if recur_insert_result == -1:
                        return -1

            for piece_id in range(self.n_segments ** 2):
                if piece_cluster_id[piece_id] == 0:
                    remain_locations = set(map(
                        tuple, np.argwhere(indices == None)))

                    #print(remain_locations)

                    location = random.sample(remain_locations, 1)[0]
                    remain_locations.remove(location)
                    row, col = location

                    recur_insert_piece(piece_id, row, col, 0)

            return indices, piece_orientation

        parent1_piece_indices, parent1_orientations = parent1
        (
            parent1_cluster_matrix, parent1_cluster_id_set,
            parent1_cluster_fitnesses, parent1_cluster_to_piece_set,
            parent1_match_orientations
        ) = self.get_ind_stats(parent1)

        parent2_piece_indices, parent2_orientations = parent2
        (
            parent2_cluster_matrix, parent2_cluster_id_set,
            parent2_cluster_fitnesses, parent2_cluster_to_piece_set,
            parent2_match_orientations
        ) = self.get_ind_stats(parent2)

        conflicted_clusters = []
        for parent1_cluster_id in parent1_cluster_to_piece_set:
            for parent2_cluster_id in parent2_cluster_to_piece_set:
                intersect = parent1_cluster_to_piece_set[parent1_cluster_id].intersection(
                    parent2_cluster_to_piece_set[parent2_cluster_id])

                if intersect and conflict_check(intersect):
                    conflicted_clusters.append(
                        (parent1_cluster_id, parent2_cluster_id))

        parent1_clusters_to_remove = set()
        parent2_clusters_to_remove = set()
        for parent1_cluster_id, parent2_cluster_id in conflicted_clusters:
            if parent1_cluster_fitnesses[parent1_cluster_id] \
                    < parent2_cluster_fitnesses[parent2_cluster_id]:
                parent2_clusters_to_remove.add(parent2_cluster_id)
            else:
                parent1_clusters_to_remove.add(parent1_cluster_id)

        for cluster_id in parent1_clusters_to_remove:
            remove_cluster(cluster_id, parent1_piece_indices,
                           parent1_cluster_matrix, parent1_cluster_id_set,
                           parent1_cluster_fitnesses,
                           parent1_cluster_to_piece_set,
                           parent1_match_orientations)
        for cluster_id in parent2_clusters_to_remove:
            remove_cluster(cluster_id, parent2_piece_indices,
                           parent2_cluster_matrix, parent2_cluster_id_set,
                           parent2_cluster_fitnesses,
                           parent2_cluster_to_piece_set,
                           parent2_match_orientations)

        child_objective_match_orientations = np.array([
            np.array([None for _ in range(4)])
            for __ in range(self.n_segments ** 2)
        ])

        for piece_id in range(self.n_segments ** 2):
            parent1_subjective_orientation = parent1_match_orientations[piece_id]
            parent2_subjective_orientation = parent2_match_orientations[piece_id]

            parent1_objective_orientation = np.roll(
                parent1_subjective_orientation,
                - parent1_orientations[piece_id]
            )
            parent2_objective_orientation = np.roll(
                parent2_subjective_orientation,
                - parent2_orientations[piece_id]
            )

            for i in range(4):
                if parent1_objective_orientation[i] is not None:
                    child_objective_match_orientations[piece_id][i] \
                        = parent1_objective_orientation[i]

                if parent2_objective_orientation[i] is not None:
                    child_objective_match_orientations[piece_id][i] \
                        = parent2_objective_orientation[i]

        child_result = -1
        n_iters = 0

        while child_result == -1 and n_iters < tolerance:
            try:
                child_result = generate_child(
                    child_objective_match_orientations,
                    parent1_cluster_to_piece_set, parent2_cluster_to_piece_set,
                    parent1_orientations, parent2_orientations
                )
            except RecursionError:
                pass

            n_iters += 1

        return child_result

    def generate_random_pop(self, pop_size=100):
        indices = np.arange(self.n_segments ** 2)

        pop = []
        for i in range(pop_size):
            shuffled_indices = np.random.permutation(indices)

            orientations = []  # 0: not rotated, 1: 90-degree clock-wise, etc.
            for _ in shuffled_indices:
                orientation = np.random.randint(0, 4)
                orientations.append(orientation)

            # Create the orientation array
            sorted_orientation_indices = shuffled_indices.argsort()
            orientations = np.array(
                orientations
            ).flatten()[sorted_orientation_indices]

            # Reshape the indices
            shuffled_indices = shuffled_indices.reshape(
                (self.n_segments, self.n_segments))

            pop.append((shuffled_indices, orientations))

        return pop

    def generate_new_pop(self):
        # Fitness matrix pairs
        fitnesses = [self.fitness(ind) for ind in self.temp_pop]

        # Other relevant stats
        n_good_matches = [(fitness[0] <= self.threshold).sum()
                          + (fitness[1] <= self.threshold).sum()
                          for fitness in fitnesses]
        avg_fitnesses = [(fitness[0].mean() + fitness[1].mean()) / 2
                         for fitness in fitnesses]
        best_fitnesses = [min(fitness[0].min(), fitness[1].min())
                          for fitness in fitnesses]

        sorted_pop = [ind for n_matches, best_fitnesses, avg_fitness, ind in
                      sorted(zip(n_good_matches, best_fitnesses,
                                 avg_fitnesses, self.temp_pop
                                 ),
                             key=lambda x: (x[0], -x[1], -x[2])
                             )
                      ]

        id_cdf = [i for i in range(len(sorted_pop)) for _ in range(i)]

        new_pop = []
        for i in range(int(self.pop_size * (1 - self.random_size))):
            child = -1

            while child == -1:  # if tolerance is passed
                parent1_id = 0
                parent2_id = 0

                while parent1_id == parent2_id:
                    parent1_id, parent2_id = random.sample(id_cdf, 2)

                parent1 = sorted_pop[parent1_id]
                parent2 = sorted_pop[parent2_id]

                child = self.crossover(parent1, parent2)

            new_pop.append(child)

        new_pop += self.generate_random_pop(self.pop_size - len(new_pop))

        return new_pop, sorted_pop

    def run(self):
        self.temp_pop = self.generate_random_pop(self.pop_size)

        for i in range(self.n_gens):
            self.temp_pop, self.prev_pop = self.generate_new_pop()

            print('=' * 30)
            print(f'Current best individual of {i}-th generation:')
            self.viz_func(self.prev_pop[-1])

            best_fitness_matrix_pair = self.fitness(self.prev_pop[-1])
            print(best_fitness_matrix_pair[0])
            print(best_fitness_matrix_pair[1])
            print()

    @staticmethod
    def generate_threshold(pieces, p=100):
        """
        Used to define the threshold for good matches.
        Calculate all differences between the first and second layers of each
        piece and return the percentile of the difference population.
        """

        differences = []

        for piece in pieces:
            differences.append(np.sum((piece[0, :] - piece[1, :]) ** 2))
            differences.append(np.sum((piece[:, -1] - piece[:, -2]) ** 2))
            differences.append(np.sum((piece[-1, :] - piece[-2, :]) ** 2))
            differences.append(np.sum((piece[:, 0] - piece[:, 1]) ** 2))

        return np.percentile(differences, p)


if __name__ == '__main__':
    game = Game('input/michelangelo-creation-of-adam.jpg')
    pieces = game.pieces

    solver = Solver(pieces, game.visualize_solution)
    solver.run()
