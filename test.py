import sys

dict1={1:3,2:5,3:6}

def foo(name,/,**kwargs):
    print(kwargs)

lis=[1,2,3]
lis.extend(range(5))
def req():
    match sys.argv[1]:
        case 1:
            print(sys.argv[-1])
req()