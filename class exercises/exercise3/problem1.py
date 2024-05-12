def findClosestPath(triangle):
    count = triangle[0][0]
    for row in range(1, len(triangle)):
        mid_index = len(triangle[row]) // 2
        count += triangle[row][mid_index if len(triangle[row]) % 2 == 1 else mid_index - 1]
    return count

#for row in range(1, len(triangle)):
#        mid_index = len(triangle[row]) // 2
#        if len(triangle[row]) % 2 == 1:
#            count += triangle[row][mid_index]
#        else:
#            count += triangle[row][mid_index - 1]


if __name__ == '__main__':
    triangle1 = [[2],[3,4],[6,5,7],[4,1,8,3]]
    triangle2 = [[-10]]

    print(findClosestPath(triangle1))
    print(findClosestPath(triangle2))