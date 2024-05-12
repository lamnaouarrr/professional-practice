import heapq

def find_kth_largest(arr, k):
    return heapq.nlargest(k, arr)[-1]

if __name__ == '__main__':
    arr1 = [3, 2, 1, 5, 6, 4]
    k1 = 2
    arr2 = [3, 2, 3, 1, 2, 4, 5, 5, 6]
    k2 = 4
    print(find_kth_largest(arr1, k1))
    print(find_kth_largest(arr2, k2))