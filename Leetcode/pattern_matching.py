def match_pattern(string, pattern):
    iP = [0,0,0,0]#len(pattern) # pattern index
    matching = [False, False, False, False]
    for iM in range(len(string)): # Master index scrolls once
        for i in range(len(pattern)):
            if string[iM]==pattern[iP[i]]:
                if iP[i] == len(pattern)-1:
                    print(f"Pattern found at index {iM-iP[i]}")
                    iP[i] = 0
                    matching[i] = False
                else:
                    iP[i] += 1
                    matching[i] = True
            else:
                iP[i] = 0

print("1st")
match_pattern("THIS IS A TEST TEXT", "TEST")
print("2nd")
match_pattern("AABAACAADAABAABA", "AABA")
print("3rd")
match_pattern("AAAABAACAADAABAABA", "ACAA")
            