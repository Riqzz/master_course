def fun(x):
    return (2*x+1)**0.5

def dfun(x):
    return 1/(2*x+1)**0.5

def dy(x, y):
    return y - 2*x/y


xn = 0
yn = fun(xn)

h = 0.1
xn1 = xn + h

yn1 = yn + h * dy(xn, yn)
print('yn+1\'', yn1)

for i in range(20):
    yn1 = yn + h * dy(xn1, yn1)
    print('yn+1', yn1)

print('y(xn+1)', fun(xn1))