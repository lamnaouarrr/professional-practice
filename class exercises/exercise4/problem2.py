def dfs(grid, i, j):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == '0': #condition to stop recursion
        return
    
    grid[i][j] = '0' #mark the current cell as visited

    #recursively visit all neighboring cells (down, up, right, left)
    dfs(grid, i + 1, j) #down
    dfs(grid, i - 1, j) #up
    dfs(grid, i, j + 1) #right
    dfs(grid, i, j - 1) #left

def count_island(grid):
    if not grid:
        return 0
    
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':
                dfs(grid, i, j)
                count += 1
    
    return count


if __name__ == '__main__':
    grid1 = [["1","1","1","1","0"],
             ["1","1","0","1","0"],
             ["1","1","0","0","0"],
             ["0","0","0","0","0"]]
    
    grid2 = [["1","1","0","0","0"],
             ["1","1","0","0","0"],
             ["0","0","1","0","0"],
             ["0","0","0","1","1"]]

    print("There are ", count_island(grid1), " surrounded islands by water.")
    print("There are ", count_island(grid2), " surrounded islands by water.")