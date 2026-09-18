# Serbian Passage Retrieval Relevance Dataset

A dataset for evaluating passage retrieval in Serbian, developed as part of Nikola Zlatanović's master's thesis, *Evaluacija sistema za dohvatanje informacija na srpskom jeziku* (*Evaluation of Information Retrieval Systems in Serbian*; School of Electrical Engineering, University of Belgrade, 2026).

This repository contains the [master's thesis](thesis/MASTER_RAD_Nikola_Zlatanovic_FINAL.docx), the [final instructions for binary relevance assessment](prompts/KONACNO_UPUTSTVO_ZA_PROCENU_RELEVANTNOSTI.md), and the [CSV dataset](data/). See the [dataset card](DATASET_CARD.md) for provenance, field definitions, and limitations. The thesis and annotation instructions are in Serbian.

| Contents | Count |
| --- | ---: |
| Retained questions | 6,477 |
| Excluded questions (separate list) | 1,007 |
| Unique passages | 1,739 |
| Judged question–passage pairs | 129,540 |
| Judged pairs per retained question | 20 |
| Positive / negative judgments | 7,878 / 121,662 |

## Files and identifiers

- `data/questions.csv`: `id,text` — retained questions.
- `data/dropped_questions.csv`: `id,text` — excluded questions. Its `id` values are local to that file and are not used in the judgments.
- `data/passages.csv`: `id,title,text` — passages.
- `data/annotations.csv`: `qid,pid,annotation` — references to `questions.id` and `passages.id`; `annotation` is `1` if the candidate answers the question and `0` otherwise.

Identifiers are local to this release, not the original SQuAD-sr-md identifiers. **Pairs absent from `annotations.csv` are unjudged; do not automatically treat them as negative.** A question with no positive judgment among its 20 assessed candidates may still have a relevant passage elsewhere in the corpus.

## Quick start

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

To check referential integrity and the expected counts:

```bash
python scripts/validate_dataset.py
```

## Provenance, limitations, and citation

The text originates from [SQuAD-sr-md](https://huggingface.co/datasets/te-sla/QuestionAnswering), which was derived from Serbian SQuAD. The accompanying thesis describes question selection, construction of the top-20 candidate pools, annotation, and review. This is **not** an exhaustively judged Cartesian product of all questions and passages: candidates were selected by retrieval systems, introducing selection bias. Interpret the labels in the context of the annotation and audit procedure described in the thesis, not as infallible ground truth for every possible pair.

To cite this release, use [CITATION.cff](CITATION.cff). Please also cite the authors of SQuAD-sr-md and the original SQuAD (see the [dataset card](DATASET_CARD.md)). See [LICENSE.md](LICENSE.md) for the scope of the licenses.
