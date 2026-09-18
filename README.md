# Serbian passage retrieval relevance dataset

Skup podataka za evaluaciju dohvatanja pasusa na srpskom jeziku, nastao u okviru master rada Nikole Zlatanovića, *Evaluacija sistema za dohvatanje informacija na srpskom jeziku* (Elektrotehnički fakultet, Univerzitet u Beogradu, 2026).

U repozitorijumu su [master rad](thesis/MASTER_RAD_Nikola_Zlatanovic_FINAL.docx), [konačno uputstvo za binarnu procenu relevantnosti](prompts/KONACNO_UPUTSTVO_ZA_PROCENU_RELEVANTNOSTI.md) i [CSV podaci](data/). Detalji o poreklu, poljima i ograničenjima su u [dataset cardu](DATASET_CARD.md).

| Sadržaj | Broj |
| --- | ---: |
| Zadržana pitanja | 6.477 |
| Odbačena pitanja (zasebna lista) | 1.007 |
| Jedinstveni pasusi | 1.739 |
| Anotirani parovi | 129.540 |
| Parova po zadržanom pitanju | 20 |
| Pozitivne / negativne oznake | 7.878 / 121.662 |

## Fajlovi i identifikatori

- `data/questions.csv`: `id,text` — zadržana pitanja.
- `data/dropped_questions.csv`: `id,text` — odbačena pitanja; njihovi `id` su lokalni za ovaj fajl i nisu deo anotacija.
- `data/passages.csv`: `id,title,text` — pasusi.
- `data/annotations.csv`: `qid,pid,annotation` — veze ka `questions.id` i `passages.id`; `annotation` je `1` ako kandidat odgovara na pitanje, inače `0`.

Identifikatori su lokalni za ovu objavu, ne izvorni ID-jevi iz SQuAD-sr-md. **Parovi koji nisu u `annotations.csv` nisu ocenjeni; ne tretirati ih automatski kao negativne.** Pitanje bez pozitivnog para među 20 ocenjenih kandidata ne znači da nema relevantnog pasusa u celom korpusu.

## Brza upotreba

```python
import csv

with open("data/questions.csv", encoding="utf-8-sig", newline="") as f:
    questions = {row["id"]: row["text"] for row in csv.DictReader(f)}

with open("data/passages.csv", encoding="utf-8-sig", newline="") as f:
    passages = {row["id"]: row for row in csv.DictReader(f)}

with open("data/annotations.csv", encoding="utf-8-sig", newline="") as f:
    judgments = list(csv.DictReader(f))

example = judgments[0]
print(questions[example["qid"]])
print(passages[example["pid"]]["title"], passages[example["pid"]]["text"])
print(example["annotation"])
```

Provera referencijalnog integriteta i očekivanih brojeva:

```powershell
python scripts/validate_dataset.py
```

## Poreklo, ograničenja i citiranje

Tekstovi potiču iz [SQuAD-sr-md skupa](https://huggingface.co/datasets/te-sla/QuestionAnswering), koji je izveden iz srpskog SQuAD skupa. Postupak odabira pitanja, formiranja top-20 kandidata, anotiranja i provere opisan je u priloženom master radu. Ovo **nije** iscrpno ocenjen kartezijanski proizvod svih pitanja i pasusa; kandidati su odabrani retrieval postupkom, što stvara selekcioni bias. Oznake treba čitati u kontekstu opisanog anotacionog i audit postupka, ne kao nepogrešiv gold za svaki mogući par.

Za citiranje ovog izdanja upotrebite podatke iz [CITATION.cff](CITATION.cff), a za izvorni tekst citirajte autore SQuAD-sr-md i izvornog SQuAD-a (videti [DATASET_CARD.md](DATASET_CARD.md)). Za opseg licenci videti [LICENSE.md](LICENSE.md).
