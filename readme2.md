# Implementačná dokumentácia k 2. úlohe IPP 2019/2020 
## Meno a priezvisko: Šimon Galba
## Login: xgalba03
&nbsp;
###  Interpret v jazyku python
  - Interpret spracováva vstupné dáta pomocou kombinácie funkcií na úprav reťazcov a 
  regulárnych výrazov
  - Výraznú úlohu pri spracovávaní inštrukcií zohráva knižnica xml.etree.ElementTree
  - Jednotlivé inštrukcie sú pomocou tejto knižnice "rozdelené" a podľa ich atribútov následne vykonávané
  - Pomocou rozdeľovacej funkcie if-then-else je vykonanie každej inštrukcie odovzdané vlastnej funkcii, zvyšuje sa tak prehľadnosť a uľahčuje oprava chýb
  - V každej z týchto "vykonávacích funkcií" sa kontrolujú potrebné atribúty inštrukcie, správnosti typov premenných, rozmedzie hodnôt, existencie náveští či samotných premenných
  - Samostatná funkcia 'exit()' bola vytvorená len pre prehľadnosť a ukončuje interpret s požadovanou hláškou a návratovým kódom

### Jednotlivé kontroly 
  - Pomocou knižnice xml.etree.ElementTree je prístup ku parametrom inštrukcie skutočne jednoduchý
  - Jednoduchou funkciou porovnávania reťazcov som skontroloval správnosť názvov argumentov ako aj samotných "tagov" inštrukcií
  - V každej "vykonávajúcej funkcii" sa v prípade narazenie na chybu volala funkcia exit()
  - V skripte sa nachádza mierna redundancia zdrojového kódu kvôli zlému pôvodnému návrhu a nedostatku času na opravu. Kvôli tejto redundancii môže byť čítanie kódu ťažšie, znížila sa tým aj funkčnosť interpretu
  


### Spustenie

- Preklad: keďže je skript vytvorený v jazyku python, nie je potrebný makefile
- Skript je kompatibilný s python verzie 3.8
- Spustenie:  
```sh
python3.8 interpret.py --'iné voliteľné parametre' 
```
--pre zobrazenie všetkých parametrov spustite s parametrom '--help' 


### Testovací skript v jazyku PHP
  - Tento skript má za úlohu porovnať jemu zadané výstupné súbory a návratové kódy s tými ktoré vráti skript interpretu či parseru
  - Pred spustením samotných testov sa v zdrojovom kóde overuje správnosť všetkých argumentov, teda voliteľných parametrov testovacieho skriptu
  - Ak sú všetky parametre v poriadku, prechádza sa k testovaniu, ak nie, užívateľ má možnosť použiť parameter '--help' pre zobrazenie nápovede

### Princíp testovania
  - Pomocou rekurzívneho alebo jednotného prechádzanie súboru (či súborou), si testovací skript vyhľadá všetky súbory potrebné na zistenie správnej funkčnosti inrepretu či parseru. Jedná sa hlavne o súbory typu .src .out
  - Pomocou príkazu exec() spustí testovací skript interpret alebo parser a ako vstup mu poskytne pripravený test
  - Výsledky potom porovná, u skriptu parser pomocou funkcionality nástroja 'jexamxml', v prípade intepretu jednoduchým príkazom diff

### Prehľadnosť
  - Pre jednoduché výsledky testov je výstup vo formáte HTML
  - Na začiatku skriptu sa vytvorí hlavička a štýlový predpis dokumentu
  - Potom sa vytvorí začiatok tabuľky (v tejto sa zobrazujú výsledky testov)
  - Po každom vykonanom teste sa potom do tohto HTML súboru pridá jeden riadok, jeho štýl závisí od výsledku testu
  - Pre väčšiu prehľadnosť sú poskytnuté štatistiky percentuálnej úspešnosti vzhľadom na množstvo zadaných testov 

### Spustenie
  - Preklad: keďže je skript vytvorený v jazyku php, nie je potrebný makefile
  - Skript je kompatibilný s php verzie 7.4
  - Spustenie:  kde $src je vstupný zdrojový kód jazyka IPPcode20
  ```sh
  php7.4 test.php --'iné voliteľné parametre' 
  ```
  --pre zobrazenie všetkých parametrov spustite s parametrom '--help'
