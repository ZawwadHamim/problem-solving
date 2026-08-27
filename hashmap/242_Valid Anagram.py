def isAnagram(s ,t):
    if len(s) != len(t):
        return False
    dics = {}
    dics2 = {}
    unique = ""
    for c in s:
        if c not in dics:
            dics[c] = 1
            unique += c
        else:
            dics[c] += 1
    for c in t:
        if c not in unique:
            return False
        elif c not in dics2:
            dics2[c] = 1
        else:
            dics2[c] += 1
    for c in unique:
        if dics[c] != dics2[c]:
            return False
        else:
            continue
    return True

s = "anagram"
t = "nagaram"
print(isAnagram(s,t))

