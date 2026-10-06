def searchMatrix(matrix,target):
    def findNum(x):
        lo,hi = 0, len(matrix[0])-1

        while lo<=hi:
            mid = (lo+hi)//2
            num= matrix[x][mid]
            if num==target:
                return True
            elif num>target:
                hi = mid -1
            else:
                lo = mid +1
        return False


    def find():
        lo, hi = 0, len(matrix)-1
        x = len(matrix[0])-1
        while lo <= hi:
            mid = (lo+hi)//2
            if matrix[mid][x]==target:
                return True
            elif matrix[mid][x] > target:
                hi = mid -1
            else:
                lo = mid +1
        return lo
    res = find()
    if isinstance(res, bool):
        return True
    if res == len(matrix):     #mistook here
        return False
    return findNum(res)
    







matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
t = 13
res = searchMatrix(matrix,t)

print(res)