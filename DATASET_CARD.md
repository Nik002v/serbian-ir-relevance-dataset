# Dataset Card: Serbian Passage Retrieval Relevance

## Summary

This dataset turns a question-answering collection into a passage-retrieval evaluation resource: 20 candidate passages are judged for relevance to each retained question. It was created for the master's thesis *Evaluacija sistema za dohvatanje informacija na srpskom jeziku* (*Evaluation of Information Retrieval Systems in Serbian*; Nikola Zlatanović, 2026). Questions, titles, and passages are in Serbian, primarily in Latin script, with some original names and terms.

## Source and construction

The starting point was te-sla's SQuAD-sr-md, a manually corrected subset of Serbian SQuAD. Questions that could be understood without their original passage context were retained. Candidate passages were assembled using retrieval channels and reranking methods described in the thesis. The final dataset contains 20 judged candidates for each retained question. An LLM annotator and human review contributed to the relevance labels; the full protocol and its limitations are described in the thesis and the accompanying prompt. This release does not include original source identifiers, intermediate artifacts, or retrieval-model scores.

Upstream dataset card: <https://huggingface.co/datasets/te-sla/QuestionAnswering>. Original English dataset: [SQuAD 1.1](https://rajpurkar.github.io/SQuAD-explorer/).

## Structure and size

All data files are UTF-8 CSV files with headers. The `id`, `qid`, and `pid` fields are decimal local identifiers; reading them as strings is safe when joining files.

| File | Rows | Fields | Description |
| --- | ---: | --- | --- |
| `data/questions.csv` | 6,477 | `id,text` | Questions included in evaluation |
| `data/dropped_questions.csv` | 1,007 | `id,text` | Questions excluded before evaluation; a separate local ID namespace |
| `data/passages.csv` | 1,739 | `id,title,text` | Passage corpus |
| `data/annotations.csv` | 129,540 | `qid,pid,annotation` | Binary judgments for 20 pairs per retained question |

Labels: `1` means the title and/or passage provides a concrete answer to the question; `0` means the candidate does not provide the requested answer. There are 7,878 positive and 121,662 negative judgments. For 179 questions, none of the 20 judged candidates is positive. This **does not establish** that no relevant passage exists among all 1,739 passages.

`qid` refers only to `questions.id`, while `pid` refers to `passages.id`. Identifiers in `dropped_questions.csv` are not judgment `qid` values, even if their numeric values overlap.

## Intended uses

- Evaluation and analysis of rerankers on **judged** pairs; evaluation of full rankings only with an explicitly documented policy for unjudged candidates.
- Analysis of positive examples and hard negatives in Serbian.
- Study alongside the candidate-pool construction described in the master's thesis.

The release has no official train/development/test split. A random split by pair can leak information about the same questions and passages across splits. For model development, split at least by question and document the procedure.

## Limitations and risks

- Only 20 selected candidates per question were judged, not all 1,739 passages. An unjudged pair is **not** a negative example.
- Candidates were selected by retrieval systems, so metrics on this pool reflect selection bias.
- LLM-assisted annotation and human review do not guarantee that every judgment is error-free.
- Questions and passages inherit linguistic, topical, and possible factual errors from the source QA/Wikipedia material.
- The original encyclopedic text has not been further anonymized; sensitive uses require an independent review.

## License and attribution

The upstream [te-sla/QuestionAnswering](https://huggingface.co/datasets/te-sla/QuestionAnswering) dataset card specifies **CC BY-SA 4.0**. The text data under `data/` is released here under the same terms, with attribution to the original authors and notice that this is a derived/adapted dataset. See [LICENSE.md](LICENSE.md) for the scope of licensing for the other files. The upstream license is reported as stated in its dataset card; users should independently check that their intended use has all necessary permissions.

## Citation

Zlatanović, Nikola. *Evaluacija sistema za dohvatanje informacija na srpskom jeziku* (*Evaluation of Information Retrieval Systems in Serbian*). Master's thesis, School of Electrical Engineering, University of Belgrade, 2026. For machine-readable citation metadata, see [CITATION.cff](CITATION.cff).

Please also cite SQuAD-sr-md: Rađenović, Jovana; Kitanović, Olivera; Stanković, Ranka; Škorić, Mihailo, *Development of Serbian QA Datasets through Prompt-Based Generation and Human Validation* (as listed in the upstream dataset card). For SQuAD: Rajpurkar, Pranav; Zhang, Jian; Lopyrev, Konstantin; Liang, Percy, *SQuAD: 100,000+ Questions for Machine Comprehension of Text*, 2016.
