
ilosc = int(input("Ile rzeczy chcesz wyslac?: "))

# ile paczek

puste_kg = []
laczna_waga = 0
paczki = 0

for i in range(ilosc):
    waga = float(input("Podaj wage elementu(1-10kg): "))

    if waga > 10 or waga < 1:
        break

# waga paczek

    if laczna_waga + waga <= 20:
        laczna_waga += waga

    else:
        paczki += laczna_waga
        puste_kg.append(20 - laczna_waga)
        laczna_waga = 0 + waga

if laczna_waga > 0:
    paczki += laczna_waga
    puste_kg.append(20 - laczna_waga)

# puste_kg

rekord = None
licznik = 0
for wartosc in puste_kg:
    licznik += 1
    if rekord is None or wartosc > rekord:
        rekord = wartosc


print(f"Wyslano {len(puste_kg)} paczek, o lacznej wadze {paczki}. Suma pustych kg to {sum(puste_kg)}")
print(f"Najwiecej pustych kg miala paczka {licznik}, bylo to {max(puste_kg)}kg")
print(puste_kg)