import numpy as np

def recursive(write):
    print("input is {0}".format(write))
    write = input("input something")
    if write == 'stop':
        return
    else:
        recursive(write)




# x = list(range(-100,100))
# y = [1/(1+np.exp(-i)) for i in x]
# print(y)
# write = 0
# recursive(write)


s = 'a1'
print(s[0])


string = input('string:').upper()
print(string)




value = ['K','b']
if value == ['K','b']:
    print("Y")
else:
    print("N")