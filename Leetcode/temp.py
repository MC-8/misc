def myf(a:int, b:int) -> int:
    assert isinstance(a, myf.__annotations__['a'])
    return a+b

print(myf(2,3))
print(myf('2',3))

