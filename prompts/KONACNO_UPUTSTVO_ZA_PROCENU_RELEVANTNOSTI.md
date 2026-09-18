# Baseline prompt za binarnu relevantnost para pitanje–pasus

## Zadatak

Za svaki ulazni par nezavisno proceni da li kandidatski pasus daje odgovor na
pitanje.

Ulaz sadrži:

- `question_id`;
- `candidate_passage_id`;
- pitanje;
- tekst kandidatskog pasusa;
- opciono naslov pasusa.

Ako je naslov dostupan, smatraj ga delom kandidata: naslov može razjasniti o
kom entitetu pasus govori. Ne koristi nikakve druge podatke.

Vrati jednu binarnu ocenu:

- **`1` — ANSWERS:** iz naslova i teksta kandidata može se izvući **konkretan
  odgovor** na ono što pitanje traži;
- **`0` — DOES_NOT_ANSWER:** kandidat ne daje odgovor na ono što pitanje
  traži, čak i ako govori o istoj temi, događaju ili entitetu.

Ovo je namerno jednostavan baseline. Ne uvodi međuocene i ne pravi posebnu
analizu granularnosti, modalnosti, vrsta prideva ili drugih finih kategorija.


## Najvažnija kontrola pre ocene `1`

Pre nego što dodeliš `1`, interno uradi sledeće:

1. identifikuj šta je **answer slot** pitanja;
2. formuliši **konkretan kandidat-odgovor** koji pasus daje;
3. proveri da pasus taj odgovor zaista vezuje za tačno traženi entitet, događaj,
   relaciju ili svojstvo.

Ako ne možeš da formulišeš konkretan kandidat-odgovor samo iz trenutnog
kandidata, dodeli `0`.

Drugim rečima:

> **Ista tema nije odgovor. Isti događaj nije odgovor. Isti entitet nije odgovor.
> Pasus mora da popuni answer slot.**

Primer:

- pitanje: `„Kada je Tesla otišao u SAD?”`
- kandidat: `„Tesla je otišao u SAD i tamo radio za Edisona.”`
- ocena: `0`

Kandidat potvrđuje događaj, ali ne daje traženo vreme.

Još jedan primer:

- pitanje: `„Kada je klub osnovan?”`
- kandidat: `„Klub je osvojio prvenstvo 1994. godine.”`
- ocena: `0`

Godina odgovarajućeg tipa postoji u pasusu, ali nije vezana za traženu relaciju
osnivanja.

I:

- pitanje: `„Koji klubovi su propustili takmičenje?”`
- kandidat: `„Vrhunski klubovi retko propuštaju takmičenje.”`
- ocena: `0`

Pasus govori o pravoj temi, ali ne imenuje klubove koji su propustili
takmičenje.

## Kada dodeliti `1`

Dodeli `1` kada razuman čitalac, koristeći samo pitanje, naslov i tekst tog
kandidata, može da odgovori na pitanje.

Odgovor:

- ne mora biti ista reč ili ista formulacija kao u pitanju;
- može biti jasna parafraza;
- može slediti jednostavnim lokalnim zaključkom iz onoga što kandidat
  eksplicitno kaže;
- može biti potvrda, negacija ili direktna ispravka pretpostavke iz pitanja;
- mora biti vezan za pravi entitet i baš onu relaciju ili svojstvo koje se
  pita.

Kod pitanja sa ponuđenim izborom nije neophodno da pasus razmatra svaku opciju
pojedinačno. Dovoljno je da jasno podrži odgovor. Na primer, za pitanje
`„Šta meri potencijalni razvoj, HDI ili IHDI?”`, kandidat `„Potencijalni razvoj
meri HDI.”` dobija `1` iako ne govori posebno o IHDI-ju.

## Kada dodeliti `0`

Dodeli `0` kada kandidat:

- govori samo o istoj temi ili pominje isti entitet, ali ne daje traženi
  odgovor;
- daje drugo svojstvo, drugu radnju ili odgovor na drugo pitanje;
- obrće smer relacije ili meša uloge subjekta i objekta;
- pominje traženi događaj, ali daje mesto kada se pita vreme, uzrok kada se
  pita posledica, učesnika kada se pita datum i slično;
- govori o drugom entitetu ili drugom događaju;
- zahteva spoljašnju činjenicu da bi se iz njega dobio odgovor;
- daje samo nepovezanu pozadinu ili trag za dalju pretragu;
- odgovara samo na deo pitanja koje izričito zahteva više obaveznih delova.

Najkraći test je:

> Mogu li sada, samo iz ovog kandidata, izgovoriti odgovor na ovo pitanje?

Ako možeš — `1`. Ako kandidat samo pomaže da se tema prepozna ili bi trebalo
potražiti još jedan pasus — `0`.

## Obavezna opšta pravila

### Svaki par je nezavisan

Ocenjuj svaki par pitanje–pasus kao da je jedini kandidat koji postoji. Na
ocenu ne sme uticati sadržaj, odgovor, skor, rang ili ocena bilo kog drugog
pasusa. Ne spajaj informacije iz više kandidata.

### Ne radi fact-check

Ne proveravaj da li je tvrdnja pasusa istorijski ili stvarno tačna. Privremeno
prihvati ono što kandidat tvrdi.

Primer:

- pitanje: `„Kada je počeo Prvi svetski rat?”`;
- pasus: `„Prvi svetski rat počeo je 102. godine.”`;
- ocena: `1`.

Ocena znači da pasus daje odgovor, a ne da je odgovor istinit u stvarnom
svetu.

### Kontradikcije između pasusa su dozvoljene

Ako tri odvojena kandidata daju tri različita odgovora na isto pitanje, sva
tri mogu dobiti `1`. Ne biraj pobednika i ne usaglašavaj njihove tvrdnje.
Kontradikcija unutar jednog istog kandidata ipak može značiti da iz njega nije
moguće izvući jasan odgovor.

### Ne koristi skrivene ili spoljašnje informacije

Ne koristi gold odgovor, originalni pasus, ostatak članka, internet, lično
enciklopedijsko znanje niti drugi kandidat. Dozvoljeni su samo normalno
razumevanje jezika, jasna parafraza, lokalna koreferencija i jednostavno
zaključivanje iz rečenica trenutnog kandidata.

### Prati traženu relaciju

Isti entitet nije dovoljan. Na primer:

- pitanje `„Kada su A i B uspostavili odnose?”` + pasus `„A i B uspostavili su
  odnose u Parizu.”` → `0`, jer pasus daje mesto, a ne vreme;
- pitanje `„Ko je pobedio X?”` + pasus `„X je pobedio Z.”` → `0`, jer je smer
  pobede obrnut;
- pitanje `„Do pada čega je dovelo formiranje pomorskih puteva?”` + pasus
  `„Posle poraza X počeli su da se formiraju pomorski putevi.”` → `0`, jer
  pasus daje vremenski sled, a ne posledicu formiranja puteva.

### Neobično ili nepotpuno eksplicitno formulisano pitanje

Ako je pitanje gramatički neobično, primeni samo minimalnu, prirodnu ispravku
reda reči ili padeža. Ne izmišljaj novu relaciju.

Međutim, **ne zahtevaj da pitanje eksplicitno navede svaki mogući detalj** ako se
informaciona potreba dovoljno jasno može zaključiti iz ograničenja već prisutnih
u samom pitanju.

Dozvoljeno je koristiti:

- imenovani entitet;
- karakterističan datum ili period;
- stabilan naziv događaja, institucije ili objekta;
- odnos sa imenovanom osobom;
- kombinaciju više ograničenja iz samog pitanja.

Primeri pitanja koja se mogu normalno oceniti bez dopisivanja spoljašnjeg
konteksta:

- `„Kada je osnovao prvo Bugarsko carstvo?”`
- `„U januaru 2006. ko je odobrio novi program UNFPA za zemlje?”`
- `„Zajedno sa Vilijamom Džejmsom, ko je bio uticajan teoretik 19. veka?”`

Nemoj takva pitanja automatski tretirati kao neocenjiva samo zato što bi se mogla
još precizirati. Za relevance zadatak pitaj samo da li trenutni kandidat, uz
prirodno čitanje samog pitanja, daje traženi odgovor.

Ako pitanje ni posle minimalne prirodne interpretacije nema stabilno značenje,
dodeli `0`, daj nizak confidence i to konkretno navedi u rationale-u. Ne
preskači red.

## Rationale

Za svaki par napiši jednu kratku, konkretnu rečenicu, idealno do 30 reči.

- Za `1` obavezno navedi **konkretan odgovor** koji kandidat daje i kako ga
  vezuje za pitanje. Nemoj pisati samo „što daje traženi odgovor”.
- Za `0` navedi šta kandidat stvarno tvrdi i koji traženi odgovor ili relacija
  nedostaje.

Dobro:

- `Pasus navodi da je A osnovan 1994. godine, što direktno odgovara na pitanje
  kada je A osnovan.`
- `Pasus govori gde su A i B uspostavili odnose, dok pitanje traži vreme
  uspostavljanja.`

Loše:

- `Pasus je relevantan.`
- `Ne odgovara.`
- `Nema dovoljno informacija.`

## Confidence

`confidence` je ceo broj od 0 do 100 i izražava sigurnost u dodeljenu binarnu
ocenu, a ne stepen relevantnosti.

- `95–100`: odluka je direktna i praktično nedvosmislena;
- `80–94`: odluka je jasna, uz malu interpretativnu rezervu;
- `60–79`: postoji stvarna dvosmislenost ili zavisi od blage normalizacije;
- ispod `60`: pitanje ili kandidat su veoma nejasni, ali je red ipak ocenjen.

Nemoj koristiti nizak confidence kao zamenu za pažljivu odluku i nemoj svim
redovima rutinski davati istu vrednost.

## Izlazni format

Vrati isključivo UTF-8 CSV sa tačno ovim zaglavljem:

    question_id,candidate_passage_id,rationale,relevance,confidence

Pravila:

- jedan ulazni par mora dati tačno jedan izlazni red;
- ID-jeve prepiši doslovno i ne izmišljaj nove;
- `relevance` mora biti tačno `0` ili `1`;
- `confidence` mora biti ceo broj 0–100;
- `rationale` stavi između dvostrukih navodnika i pravilno escape-uj unutrašnje
  navodnike;
- ne dodaj kolone, Markdown ogradu, uvod niti tekst posle CSV-a;
- sačuvaj redosled ulaznih parova.

Pre završetka proveri da broj izlaznih redova odgovara broju ulaznih parova i
da je svaki par ocenjen potpuno nezavisno.


Za svaki red sa `relevance=1` uradi još jednu završnu proveru:

> **Mogu li iz rationale-a jasno da vidim koji je konkretan odgovor pasus dao?**

Ako ne možeš, ponovo proveri par. Ako pasus samo govori o istoj temi ili daje
trag, ali ne popunjava answer slot, ocena mora biti `0`.
