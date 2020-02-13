class Shark:
    fish_type = "Shark"
    counter = 0
    
    def __init__(self) -> None:
        type(self).counter += 1
    
    def __del__(self) -> None:
        type(self).counter -= 1


S1 = Shark()
S2 = Shark()

print(S1.fish_type)

S1.fish_type = "Goldfish"

print(S1.fish_type)
print(S2.fish_type)
print(Shark.fish_type)

print(S1.counter)
print(S2.counter)
print(Shark.counter)
