def searchRange(nums, target):
    lo,hi= 0, len(nums)
    while lo<hi:
        mid = lo + (hi-lo)//2
        if nums[mid]>target:
            hi = mid - 1
        else:
            lo = mid+1

    return lo-1




nums = [5,7,7,8,8,10,12,12,12]
target = 12

print(searchRange(nums,target))