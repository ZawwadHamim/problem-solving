def maxSubArray(nums):
    n = len(nums)
    i = 0
    sum = float("-inf")
    total = 0
    for j in range(n):
        while total<0:
            total -= nums[i]
            i += 1
            
        total += nums[j]
        sum = max(total,sum)
    return sum

nums = [-2,1,-3,4,-1,2,1,-5,4]
print(maxSubArray(nums))