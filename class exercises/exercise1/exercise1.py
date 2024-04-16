def max_nums(nums):
    return max(sum(1 for i in nums if i > 0), sum(1 for i in nums if i < 0))

if __name__ == '__main__':
    example1 = [-2, -1, -1, 1, 2, 3]
    example2 = [-3, -2, -1, 0, 0, 1, 2]
    example3 = [5, 20, 66, 1314]
    print(max_nums(example1))
    print(max_nums(example2))
    print(max_nums(example3))