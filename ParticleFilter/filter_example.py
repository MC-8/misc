# Our numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# Function that filters out all numbers which are odd


def filter_less_than(num, val):

    if num < val:
        return True
    else:
        return False

D = {}
D[2] = 'a'
D[6] = 'b'

# filtered_numbers = filter(lambda x: filter_less_than(x, 5), numbers)
filtered_numbers = filter(lambda x: filter_less_than(x, 5), D)

# print(list(filtered_numbers))

myset = {1,5,2,6,29,66,7,3,2,36,7,99,21,11}
smyset = sorted(myset,reverse=True)
print(smyset)
# for i in myset:
#     print (i)
# print('-'*20)
# for i in iter(myset):
#     print (i)
# for i,d in filtered_numbers:
#     print(i)
# filtered_numbers = [2, 4, 6, 8, 10, 12, 14]
