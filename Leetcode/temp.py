from typing import List

def try_annotation(x:str)->str:
    return(x)

def try_annotation_with_ok_return(x:str)-> List[int]:
    return [1]

def try_annotation_with_wrong_return(x:str)-> List[int]:
    y = (1,)
    return y

print(try_annotation("nothing"))
print(try_annotation_with_ok_return("ok"))
print(try_annotation_with_wrong_return([1,2,3]))



