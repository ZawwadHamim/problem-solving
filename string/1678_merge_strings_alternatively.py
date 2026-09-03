def mergeAlternately(word1, word2):
    def mergedArray(shorter, longer):
        merged = ''

        for i in range(len(shorter)):
            merged += word1[i]
            merged += word2[i]

        for i in range(len(shorter), len(longer)):
            merged += longer[i]
        return merged
        

    if len(word1) < len(word2):
        return mergedArray(word1, word2)
    else:
        return mergedArray(word2, word1)


word1 = "abcd"
word2 = "pq"

print(mergeAlternately(word1, word2))