from PathFinding.Maze.maze import Game  # if executing from directory root
#from maze import Game  # if executing from current directory


def generate_path_bfs(board, start_pos, target):
    # Set up variables for algorithm
    open_list = [start_pos]
    closed_set = set()
    prev_dict = {start_pos: start_pos}

    temp_pos = open_list.pop(0)
    while temp_pos[1] != target:
        # Generate open neighbors
        neighbors = []
        coordinates = [
            (temp_pos[0] - 1, temp_pos[1]), (temp_pos[0] + 1, temp_pos[1]),
            (temp_pos[0], temp_pos[1] - 1), (temp_pos[0], temp_pos[1] + 1)
        ]

        for c in coordinates:
            if 0 <= c[0] < len(board) and 0 <= c[1] <= target \
                    and board[c[0]][c[1]] == 0 and c not in closed_set:
                neighbors.append(c)

        for neighbor in neighbors:
            if neighbor not in prev_dict:
                prev_dict[neighbor] = temp_pos

        closed_set.add(temp_pos)

        # Generate path from start to current position
        while temp_pos in closed_set:
            open_list += neighbors
            temp_pos = open_list.pop(0)

            temp_path = []
            trace = temp_pos
            while trace != start_pos:
                temp_path.append(trace)
                trace = prev_dict[trace]
            temp_path.append(start_pos)

            yield list(reversed(temp_path))


if __name__ == '__main__':
    game = Game(input_='input/small.txt', auto=generate_path_bfs)
    #game = Game(input_='input/small.txt', auto=generate_path_dfs)
    game.run()
