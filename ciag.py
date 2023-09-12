x = int(input("Podaj x: "))

if 1 > x > 100:
    exit()

if x == 1:
    x = 3*x+1
    print(x)

while x != 1:
    if x % 2 == 0:
        x = x/2
    else:
        x= 3*x + 1
    print(int(x))