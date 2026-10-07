def search( nums, target):
    def findFirst():
        lo,hi = 0, len(nums)-1
        x = hi
        while lo<hi:
            mid = (lo+hi)//2
            if nums[x]< nums[mid]:
                lo = mid +1
            else:
                hi = mid
        return hi
    def BS(lo,hi):
        while lo<=hi:
            mid = (lo+hi)//2
            if nums[mid]==target:
                return mid
            elif nums[mid]>target:
                hi = mid - 1
            else:
                lo = mid + 1

        return -1
    n = len(nums)
    first = findFirst()
    if first==0:
        return BS(0,n-1)
    else:
        if target>=nums[0]:
            return BS(0,first-1)
        elif target<nums[0]:
            return BS(first,n-1)
        else:
            return -1


nums = [4,5,6,7,0,1,2]
for t in [4, 5, 6, 7, 0, 1, 2, 3, 8, -1]:
    print(t, search(nums, t))

print(search([1], 1))           # expect 0
print(search([1, 3], 3))        # expect 1 (not rotated)
print(search([3, 1], 1))        # expect 1 (rotated)