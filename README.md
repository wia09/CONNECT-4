# Connect-4 Variánsok – AI alapú elemzés és szimuláció

Ez a projekt „A Connect-4 Játék és Variánsainak Matematikai és Programozási Elemzése” című szakdolgozatomhoz készült kutatási célból.

A program célja a klasszikus Connect-4 játék három módosított szabályrendszer viselkedésének vizsgálata mesterséges intelligenciával, minimax kereséssel és szimulációs elemzéssel.


## Projekt áttekintése
A rendszer egy Python + Pygame alapú alkalmazás, amelyben:
- két mesterséges intelligencia játszik egymás ellen,
- a játék minden lépése vizuálisan megjelenik,
- a döntések minimax + alfa–béta metszés alapján történnek,
- lehetőség van több száz vagy több ezer szimuláció automatikus lefuttatására,
- a szimulációk eredményei logfájlokba kerülnek.

A projekt célja, hogy a különböző szabályváltozatok stratégiai viselkedése összehasonlítható legyen.


## A vizsgált variánsok
A Variant enum négy különböző szabályrendszert definiál:
- CLASSIC – Hagyományos Connect-4, normál győzelmi feltétel
- FAST – Felgyorsított játék: egy körben 2 korong helyezhető le
- REVERSE – Misère verzió: aki négyest alakít ki, veszít
- FAST_REVERSE – A két fenti szabály kombinációja

A variánsok mind az AI-értékelést, mind a körlogikát, mind a keresési heurisztikákat figyelembe veszik.


## Alkalmazott algoritmusok
- Minimax keresés: A játékos a következő lépést a várható eredmény maximalizálásával választja.
- Alfa–béta metszés: Jelentősen csökkenti a vizsgálandó állapotok számát.
- Heurisztikus értékelőfüggvények: Mindegyik variáns külön heurisztikát használ (klasszikus, gyorsított, fordított, kombinált).
- Transzpozíciós tábla: A már korábban kiértékelt állapotok gyors visszakeresésére.
- Sztochasztikus AI: A best_move_stochastic() TOP–K legjobb lépésből választ véletlenszerűen — szimulációkhoz ideális.


## Könyvtárszerkezet
```
├── ai.py         – Minimax, heurisztikák, transzpozíciós tábla
├── logic.py      – Játéklogika, állapotkezelés, variánsok
├── game.py       – Grafikai megjelenítés, játék futtatása
├── menu.py       – Főmenü, variáns választás
├── simulate.py   – Tömeges szimulációk futtatása, logolás
├── config.py     – Konstansok, színek, UI-méretek
├── assets/       – Klikk hang
└── logs/         – Szimulációs naplók (automatikusan jönnek létre)
```

## Futtatás és használat
1) Telepítési követelmények: Python 3.10+ Pygame: pip install pygame
2) Grafikus játék futtatása: python menu.py
3) A játék automatikusan fut. Mindkét játékos AI.
   - Vissza gomb és ESC billentyű – vissza a menübe
   - Kilépés gomb – játék bezárása


## Szimulációk futtatása
A projekt képes több száz vagy ezer játszmát automatikusan lefuttatni.

    python simulate.py

Az eredmények:
- győzelmi arányok
- döntetlenek
- kezdő és második játékos teljesítménye

logfájlba kerülnek a logs/ mappába, időbélyeggel.


## Szimulált játszmák számának módosítása:
A meccsek számát és a szimulálandó variánst a simulate.py fájl végén lehet beállítani.
Az alábbi négy sor közül bármelyik aktiválható kikommentezéssel:
```
#run_simulation_cli(Variant.CLASSIC, n_games=50)
#run_simulation_cli(Variant.FAST, n_games=200)
#run_simulation_cli(Variant.REVERSE, n_games=300)
run_simulation_cli(Variant.FAST_REVERSE, n_games=100)
```
Az n_games utáni szám módosításával elérhető akármennyi játszma szimulálása.


## Fejlesztési megjegyzések
- A játék logikája külön modulban van, a grafikai rész tisztán szeparált.
- A variánsok szabályai átjárhatók, könnyen bővíthetők.
- A heurisztikák paraméterezhetők, így további kutatási célokra ideálisak.
- A rendszer a szakdolgozat matematikai modelljeivel összhangban működik.



## Készítette
Vágási Vivien 

Szegedi Tudományegyetem Programtervező Informatikus nappali szakon végzős hallgató.

Neptun kód: H47UZG

2025