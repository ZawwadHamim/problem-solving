def searchRange(nums, target):
    def findFirst():
        lo,hi = 0, len(nums)
        while lo<hi:
            mid = (lo+hi)//2
            if nums[mid]<target:
                lo = mid+1
            else: #finding the first so eq goes to hi
                hi = mid
        return lo
    def find_last():
        lo,hi = 0, len(nums)
        while lo<hi:
            mid = (lo+hi)//2
            if nums[mid]<=target:
                lo = mid+1
            else:
                hi = mid
        return lo-1

    first = findFirst()
    last = find_last()
    if first == len(nums) or nums[first] != target:
        return [-1,-1]
    return [first,last]



nums = [5,7,7,8,8,10,12,12,12]
target = 7

print(searchRange(nums,target))