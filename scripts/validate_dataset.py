"""Check the released CSV files without installing third-party packages."""

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "data"


def load(name, columns):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        assert reader.fieldnames == columns, (name, reader.fieldnames)
        return list(reader)


questions = load("questions.csv", ["id", "text"])
dropped = load("dropped_questions.csv", ["id", "text"])
passages = load("passages.csv", ["id", "title", "text"])
annotations = load("annotations.csv", ["qid", "pid", "annotation"])

assert len(questions) == 6477
assert len(dropped) == 1007
assert len(passages) == 1739
assert len(annotations) == 129540

qids = {row["id"] for row in questions}
pids = {row["id"] for row in passages}
assert len(qids) == len(questions)
assert len(pids) == len(passages)
assert all(row["text"].strip() for row in questions)
assert all(row["title"].strip() and row["text"].strip() for row in passages)

pairs = set()
counts = Counter()
labels = Counter()
for row in annotations:
    assert row["qid"] in qids, row
    assert row["pid"] in pids, row
    assert row["annotation"] in {"0", "1"}, row
    pair = (row["qid"], row["pid"])
    assert pair not in pairs, pair
    pairs.add(pair)
    counts[row["qid"]] += 1
    labels[row["annotation"]] += 1

assert set(counts) == qids
assert set(counts.values()) == {20}
assert labels == Counter({"0": 121662, "1": 7878}), labels
print(f"OK: {len(questions)} questions, {len(passages)} passages, "
      f"{len(annotations)} judged pairs, labels {dict(labels)}")
