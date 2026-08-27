nums = [1,2,3,4]
n = len(nums)
pre, suf = [1]*n, [1] * n
sum = pre[0]

for i in range(0,len(nums)):
    pre[i] = sum
    sum *= nums[i]

sum = 1
for i in range(len(nums)-1,0,-1):
    sum *= nums[i]
    suf[i-1] = sum
     

for i in range(len(nums)):
    nums[i] = pre[i] * suf[i]

print(nums)
    