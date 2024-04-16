def findK(arr, k):
    arr3 = list(range(1, 1001)) #generate numbers from 1 to 1000
    arr4 = [num for num in arr3 if num not in arr]
    return arr4[k-1]

# def findK(arr, k):
#    arr3 = list(range(1, 1001)) #generate numbers from 1 to 1000
#    arr4 = []
#    for num in arr3:
#        if num not in arr:
#            arr4.append(num)
#    return arr4[k-1]

if __name__ == '__main__':
    arr1 = [2, 3, 4, 7, 11]
    k1 = 5
    arr2 = [1, 2, 3, 4]
    k2 = 2
    print(findK(arr1, k1))
    print(findK(arr2, k2))