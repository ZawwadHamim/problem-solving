def findMin(nums):
    lo, hi = 0, len(nums)-1,
    x = hi
    while lo<hi:
        mid = (lo+hi)//2
        if nums[x]<nums[mid]:
            lo = mid+1
        else:
            hi = mid

    return nums[hi]

nums=[11,13,15,17]
print(findMin(nums))