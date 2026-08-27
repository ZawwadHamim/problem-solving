def twoSum(nums, target):
    seen = {}
    for i in range(len(nums)):
        compliment = target - nums[i]
        if compliment in seen:
            return [seen[compliment],i]
        seen[nums[i]] = i

nums = [3,2,4] 
target = 6
print(twoSum(nums,target))