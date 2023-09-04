inflacja = [1.592824484,
-0.453509101,
2.324671717,
1.261254407,
1.782526286,
2.329384541,
1.502229842,
1.782526286,
2.328848994,
0.616921348,
2.352295886,
0.337779545,
1.577035247,
-0.292781443,
2.48619659,
0.267110318,
1.417952672,
1.054243267,
1.480520104,
1.577035247,
-0.07742069,
1.165733399,
-0.404186718,
1.499708521,
] 



kredyt = int(input("Podaj wysokosc kredytu: "))
opr = int(input("Podaj oprocentowanie w %: ")) #oprocentowanie
rata = int(input("Podaj wysokosc raty: "))


for i in inflacja:
    kredyt1 = kredyt #wartosc poprzedniego cyklu/misiaca
    
    kredyt = (1 + (i + opr)/kredyt/10)*kredyt - rata
    kredyt = round(kredyt, 2)
    
    if kredyt > 0:
        print("Twoja pozostala kwota kredytu to", kredyt, end=",")
        print(" to",round((kredyt1-kredyt), 2), "mniej niz w poprzednim miesiacu.")
    elif kredyt < 0:
        print("Kredyt został spłacony")
        break
    