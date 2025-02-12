from typing import List, Tuple, Set

def parse_map(map_lines: List[str]) -> Tuple[Set[Tuple[int, int]], Tuple[int, int], Set[Tuple[int, int]]]:
    boxes = set()
    walls = set()
    robot = (0, 0)
    for row_idx, line in enumerate(map_lines):
        for col_idx, char in enumerate(line):
            if char == '#':
                walls.add((row_idx, col_idx))
            elif char == 'O':
                boxes.add((row_idx, col_idx))
            elif char == '@':
                robot = (row_idx, col_idx)
            # '.' represents empty space; no action needed
    return boxes, robot, walls

def parse_moves(moves_str: str) -> List[str]:
    return list(moves_str.replace('\n', '').strip())

def move_robot(boxes: Set[Tuple[int, int]], robot: Tuple[int, int], walls: Set[Tuple[int, int]], moves: List[str]) -> Tuple[Set[Tuple[int, int]], Tuple[int, int]]:
    # Direction deltas
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    for move in moves:
        if move not in directions:
            continue  # Ignore invalid characters
        delta = directions[move]
        target = (robot[0] + delta[0], robot[1] + delta[1])

        if target in walls:
            # Move blocked by wall
            continue
        elif target in boxes:
            # Attempt to push the box
            new_box = (target[0] + delta[0], target[1] + delta[1])
            if new_box in walls or new_box in boxes:
                # Cannot push the box
                continue
            else:
                # Push the box
                boxes.remove(target)
                boxes.add(new_box)
                # Move the robot
                robot = target
        else:
            # Move the robot into empty space
            robot = target

    return boxes, robot

def calculate_gps_sum(boxes: Set[Tuple[int, int]]) -> int:
    gps_sum = 0
    for (row, col) in boxes:
        gps = 100 * row + col
        gps_sum += gps
    return gps_sum

def main():
    # Input Map
    map_input = [
        "##########",
        "#..O..O.O#",
        "#......O.#",
        "#.OO..O.O#",
        "#..O@..O.#",
        "#O#..O...#",
        "#O..O..O.#",
        "#.OO.O.OO#",
        "#....O...#",
        "##########"
    ]

    # Input Moves
    moves_input = """
<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()

    # Parse the map
    boxes, robot, walls = parse_map(map_input)

    # Parse the moves
    moves = parse_moves(moves_input)

    # Simulate the moves
    final_boxes, final_robot = move_robot(boxes, robot, walls, moves)

    # Calculate the sum of GPS coordinates
    gps_sum = calculate_gps_sum(final_boxes)

    print(f"Sum of all boxes' GPS coordinates: {gps_sum}")

if __name__ == "__main__":
    main()
