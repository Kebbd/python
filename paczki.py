
ilosc = int(input("Ile rzeczy chcesz wyslac?: "))

# ile paczek

puste_kg = []
laczna_waga = 0
paczki = 0
licznik = 0

for i in range(ilosc):
    waga = float(input("Podaj wage elementu(1-10kg): "))

    if waga > 10 or waga < 1:
        if laczna_waga + waga > 20:
            puste_kg.append(20 - laczna_waga)
            puste_kg.append(20 - waga)
            paczki += laczna_waga
            paczki += waga
            laczna_waga = 0
            break
        else:
            laczna_waga += waga
            break



# waga paczek

    if laczna_waga + waga <= 20:
        laczna_waga += waga

    else:
        paczki += laczna_waga
        puste_kg.append(20 - laczna_waga)
        laczna_waga = 0 + waga

if laczna_waga > 0 < 20:
    paczki += laczna_waga
    puste_kg.append(20 - laczna_waga)

# puste_kg
if len(puste_kg) :
    licznik = puste_kg.index(max(puste_kg))
    licznik += 1


print(f"Wyslano {len(puste_kg)} paczek, o lacznej wadze {paczki}. Suma pustych kg to {sum(puste_kg)}")
print(f"Najwiecej pustych kg miala paczka {licznik}, bylo to {max(puste_kg)}kg")
print(puste_kg)