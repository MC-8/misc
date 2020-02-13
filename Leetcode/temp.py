class Solution:
    def decodeString(self, s: str) -> str:
        # Number k, append k times what comes next until the bracket closing bracket
        i = 0
        
        # initial append
        tmp_str = ''
        while 'a' <= s[i] <= 'z':
            tmp_str += s[i]
            i       += 1
        
        num = ''
        
        while ('0' <= s[i] <= '9'):
            num += s[i]
            i   += 1
        
        repeats = int(num)

        substr = ''
        if s[i]=='[':
            counter = 1
            i+=1
            while s[i] != ']' and counter !=0:
                if s[i]=='[': 
                    counter +=  1
                if s[i] == ']':
                    counter -= 1
                substr += s[i]
                i+=1
            substr += s[i]
            
        print(substr)
        
        return tmp_str + self.decodeString(substr)*repeats

X = Solution()

print(X.decodeString("3[abcs3[asd]]2[bc]"))



    
    
