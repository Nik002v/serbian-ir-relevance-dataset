# Dataset card: Serbian passage retrieval relevance

## Sažetak

Ovaj skup prevodi zadatak odgovaranja na pitanja u zadatak dohvatanja pasusa: za svako zadržano pitanje ocenjuje se relevantnost 20 kandidatskih pasusa. Nastao je za master rad *Evaluacija sistema za dohvatanje informacija na srpskom jeziku* (Nikola Zlatanović, 2026). Jezik pitanja, naslova i pasusa je srpski; podaci su zapisani latinicom, uz poneke izvorne nazive i termine.

## Poreklo i izgradnja

Polazni skup je SQuAD-sr-md organizacije te-sla, ručno korigovan podskup srpskog SQuAD-a. Iz njega su izdvojena pitanja koja se mogu razumeti bez izvornog konteksta. Kandidatski pasusi formirani su kombinacijom retrieval kanala i prerangiranja opisanih u master radu. Konačni skup sadrži po 20 ocenjenih kandidata za svako zadržano pitanje. U nastanku oznaka učestvovali su LLM anotator i ljudska provera; detaljan protokol i ograničenja navedeni su u master radu i priloženom promptu. Ova objava ne sadrži izvorne identifikatore, međukorake ni skorove retrieval modela.

Izvorna kartica skupa: <https://huggingface.co/datasets/te-sla/QuestionAnswering>. Originalni engleski skup: [SQuAD 1.1](https://rajpurkar.github.io/SQuAD-explorer/).

## Struktura i obim

Svi fajlovi su UTF-8 CSV sa zaglavljem. Polja `id`, `qid` i `pid` su decimalni lokalni identifikatori; pri spajanju ih je bezbedno čitati kao stringove.

| Fajl | Redova | Polja | Značenje |
| --- | ---: | --- | --- |
| `data/questions.csv` | 6.477 | `id,text` | Pitanja uključena u evaluaciju |
| `data/dropped_questions.csv` | 1.007 | `id,text` | Pitanja odbačena pre evaluacije; poseban prostor lokalnih ID-jeva |
| `data/passages.csv` | 1.739 | `id,title,text` | Korpus pasusa |
| `data/annotations.csv` | 129.540 | `qid,pid,annotation` | Binarne oznake za 20 parova po zadržanom pitanju |

Oznake: `1` = naslov i/ili pasus daju konkretan odgovor na pitanje; `0` = kandidat ne daje traženi odgovor. Ukupno: 7.878 pozitivnih i 121.662 negativnih oznaka. Za 179 pitanja nema pozitivne oznake među ocenjenih 20 kandidata. To **ne dokazuje** odsustvo relevantnog pasusa među svih 1.739.

`qid` referencira isključivo `questions.id`, a `pid` referencira `passages.id`. ID-jevi iz `dropped_questions.csv` nisu `qid` iz anotacija, iako se numerički mogu poklapati.

## Preporučena upotreba

- Evaluacija i analiza rerankera na **ocenjenim** parovima; testiranje kvaliteta rangiranja uz jasno navedeno postupanje s neocenjenim kandidatima.
- Analiza pozitivnih i teških negativnih primera na srpskom jeziku.
- Čitanje uz opis formiranja kandidatskog pool-a u master radu.

Podaci ne sadrže zvaničan train/dev/test split. Nasumična podela po parovima može procuriti informacije o istim pitanjima i pasusima između skupova. Ako pravite split za modeliranje, delite najmanje po pitanju i dokumentujte pravilo.

## Ograničenja i rizici

- Označeno je samo 20 selektovanih kandidata po pitanju, ne svih 1.739 pasusa. Neocenjeni par **nije** negativan primer.
- Kandidati potiču iz retrieval sistema; metrike nad njima odražavaju i selekcioni bias.
- Automatski/LLM potpomognute oznake i ljudska provera nisu garancija da je svaka oznaka bez greške.
- Pitanja i pasusi nasleđuju jezičke, tematske i potencijalne faktografske greške iz izvornog QA/Wikipedia materijala.
- Nema dodatne anonimizacije izvornog enciklopedijskog teksta; pre upotrebe za osetljive svrhe potreban je sopstveni pregled.

## Licenca i atribucija

Kartica izvornog [te-sla/QuestionAnswering](https://huggingface.co/datasets/te-sla/QuestionAnswering) navodi **CC BY-SA 4.0**. Za tekstualne podatke u `data/` ova objava koristi isti režim uz obaveznu atribuciju izvornim autorima i oznaku da je skup izveden/prerađen. Detalji o ostalim fajlovima su u [LICENSE.md](LICENSE.md). Objavljena licenca izvora navedena je prema kartici izvornog skupa; korisnici treba sami da provere da li imaju sve potrebne dozvole za planiranu upotrebu.

## Citiranje

Zlatanović, Nikola. *Evaluacija sistema za dohvatanje informacija na srpskom jeziku*. Master rad, Elektrotehnički fakultet Univerziteta u Beogradu, 2026. Za mašinski čitljivo citiranje videti [CITATION.cff](CITATION.cff).

Takođe citirati izvorni SQuAD-sr-md: Rađenović, Jovana; Kitanović, Olivera; Stanković, Ranka; Škorić, Mihailo, *Development of Serbian QA Datasets through Prompt-Based Generation and Human Validation* (navedeno u kartici izvornog skupa). Za SQuAD: Rajpurkar, Pranav; Zhang, Jian; Lopyrev, Konstantin; Liang, Percy, *SQuAD: 100,000+ Questions for Machine Comprehension of Text*, 2016.
