import heapq

def ultimate_path(backyard):
    """
    Optimized A* search solution to generate the shortest path to cut all 
    long grass ('+') in the backyard, starting and ending at (0, 0).
    
    Args:
        backyard (list of list of str): A 2D list representing the backyard.
        
    Returns:
        path (list of tuple): The path that cuts all grass and 
        returns to (0, 0).
    """
    row_dim = len(backyard)
    col_dim = len(backyard[0])
    
    # Directions for movement: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Find all positions with long grass ('+')
    grass_positions = set(
        (r, c) for r in range(row_dim) for c in range(col_dim) 
        if backyard[r][c] == '+'
    )
    
    if not grass_positions:
        return [(0, 0)]  # If no grass, return to start

    total_grass = len(grass_positions)
    
    # Helper function to check if a move is valid
    def is_valid(x, y):
        return 0 <= x < row_dim and 0 <= y < col_dim
    
    # Manhattan distance as the heuristic (to the nearest grass)
    def heuristic(x, y):
        return min(abs(x - gx) + abs(y - gy) for gx, gy in grass_positions)
    
    # A* search algorithm implementation
    def a_star_search(start):
        queue = []
        heapq.heappush(
            queue, 
            (0, start, [(0, 0)], set([(0, 0)]), 0)
        )  # (priority, current_node, path, visited_set, grass_cut)
        
        while queue:
            priority, (x, y), current_path, visited, grass_cut = heapq.heappop(queue)
            
            # If all grass is cut and we return to start, return the path
            if grass_cut == total_grass and (x, y) == (0, 0):
                return current_path
            
            # Explore each direction
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if is_valid(nx, ny) and (nx, ny) not in visited:
                    new_visited = visited.copy()
                    new_visited.add((nx, ny))
                    
                    # Update path and grass cut count
                    new_path = current_path + [(nx, ny)]
                    new_grass_cut = grass_cut
                    
                    if backyard[nx][ny] == '+':
                        new_grass_cut += 1  # We've cut new grass
                        grass_positions.discard((nx, ny))  
                        # Remove from future consideration
                    
                    # Compute cost: distance + heuristic 
                    # Manhattan distance to closest grass
                    new_priority = len(new_path) + heuristic(nx, ny)
                    heapq.heappush(
                        queue, 
                        (new_priority, (nx, ny), new_path, new_visited, \
                         new_grass_cut)
                    )
        
        return [(0, 0)]  # Fallback: No valid path found
    
    # Start the A* search from (0, 0)
    return a_star_search((0, 0))


