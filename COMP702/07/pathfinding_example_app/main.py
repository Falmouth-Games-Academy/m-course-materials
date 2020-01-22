import pygame
import time
import glob
import heapq

import map


def reconstruct_path(node):
    path = []
    while node is not None:
        path.insert(0, node)
        node = node.came_from
    return path


def traversal_search(the_map, screen, breadth_first):
    # Initialise the open and visited nodes
    open_nodes = [the_map.start]
    visited_nodes = set()

    while len(open_nodes) > 0:
        # Pop an open node and mark it as visited
        current_node = open_nodes.pop(0 if breadth_first else -1)
        visited_nodes.add(current_node)

        # If we have reached the goal, return the path
        if current_node is the_map.goal:
            return reconstruct_path(current_node)

        # Loop through the neighbours, adding unvisited neighbours to the open list
        for edge in current_node.edges:
            if edge.to_node not in open_nodes and edge.to_node not in visited_nodes:
                edge.to_node.came_from = current_node
                open_nodes.append(edge.to_node)

        # Redraw the map
        screen.fill((255, 255, 255))
        the_map.draw(screen)

        # Draw the open nodes in red
        for node in open_nodes:
            node.draw(screen, (255, 0, 0), 6)

        # Draw the current node in green
        current_node.draw(screen, (0, 255, 0), 12)

        # Flip the display and pause for 0.1 seconds
        pygame.display.flip()
        time.sleep(0.1)
        pygame.event.get()


def greedy_search(the_map, screen):
    queue = [(map.euclidean_distance(the_map.start.pos, the_map.goal.pos), the_map.start)]
    the_map.start.came_from = None
    visited = set()

    while len(queue) > 0:
        (distance, current_node) = heapq.heappop(queue)
        visited.add(current_node)

        if current_node is the_map.goal:
            return reconstruct_path(current_node)

        for edge in current_node.edges:
            if edge.to_node not in [n for (d,n) in queue] and edge.to_node not in visited:
                edge.to_node.came_from = current_node
                distance = map.euclidean_distance(edge.to_node.pos, the_map.goal.pos)
                heapq.heappush(queue, (distance, edge.to_node))

        screen.fill((255, 255, 255))
        the_map.draw(screen)

        for distance, node in queue:
            node.draw(screen, (255, 0, 0), 6)

        current_node.draw(screen, (0, 255, 0), 12)

        pygame.display.flip()
        time.sleep(0.1)
        pygame.event.get()


def a_star_search(the_map, screen, heuristic):
    queue = [(0 + heuristic(the_map.start.pos, the_map.goal.pos), the_map.start)]
    the_map.start.g = 0
    the_map.start.came_from = None
    visited = set()

    while len(queue) > 0:
        (distance, current_node) = heapq.heappop(queue)
        visited.add(current_node)

        if current_node is the_map.goal:
            return reconstruct_path(current_node)

        for edge in current_node.edges:
            if edge.to_node not in visited:
                distance_so_far = current_node.g + edge.length

                try:
                    current_g = edge.to_node.g
                except AttributeError:
                    current_g = 1000000

                if distance_so_far < current_g:
                    edge.to_node.came_from = current_node
                    distance_to_goal = heuristic(edge.to_node.pos, the_map.goal.pos)
                    edge.to_node.g = distance_so_far
                    heapq.heappush(queue, (distance_so_far + distance_to_goal, edge.to_node))

        screen.fill((255, 255, 255))
        the_map.draw(screen)

        for distance, node in queue:
            node.draw(screen, (255, 0, 0), 6)

        current_node.draw(screen, (0, 255, 0), 12)

        pygame.display.flip()
        time.sleep(0.1)
        pygame.event.get()


def string_pull(the_map, screen, path):
    while True:
        for i in range(1, len(path)-1):
            if the_map.is_unobstructed(path[i-1].pos, path[i+1].pos):
                del path[i]
                break  # out of the for loop
        else:
            break  # out of the while loop

        screen.fill((255, 255, 255))

        the_map.draw(screen)
        for i in range(1, len(path)):
            pygame.draw.line(screen, (0, 0, 0), path[i - 1].pos, path[i].pos, 6)

        for node in path:
            node.draw(screen, (0, 0, 0), 8)

        pygame.display.flip()
        time.sleep(0.1)
        pygame.event.get()


def main():
    tile_size = 50

    # Initialise PyGame
    pygame.init()
    clock = pygame.time.Clock()

    for map_name in sorted(glob.glob("*.txt")):
        the_map = map.Map(map_name, tile_size, include_diagonals=True)

        window_width = the_map.width * tile_size
        window_height = the_map.height * tile_size
        window_size = (window_width, window_height)

        # Create the screen
        screen = pygame.display.set_mode(window_size)

        # Depth first
        path = traversal_search(the_map, screen, False)

        # Breadth first
        #path = traversal_search(the_map, screen, True)

        # Greedy
        #path = greedy_search(the_map, screen)

        # Dijkstra
        #path = a_star_search(the_map, screen, lambda a,b: 0)

        # A*
        #path = a_star_search(the_map, screen, map.euclidean_distance)

        #screen.fill((255, 255, 255))

        #the_map.draw(screen)

        if path is not None:
            for i in range(1, len(path)):
                pygame.draw.line(screen, (0, 0, 0), path[i - 1].pos, path[i].pos, 6)

        pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                break

        do_string_pull = True
        if path is not None and do_string_pull:
            string_pull(the_map, screen, path)

            for i in range(1, len(path)):
                pygame.draw.line(screen, (0, 0, 0), path[i - 1].pos, path[i].pos, 6)

            for node in path:
                node.draw(screen, (0, 0, 0), 8)

            pygame.display.flip()

            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    break


if __name__ == '__main__':
    main()
