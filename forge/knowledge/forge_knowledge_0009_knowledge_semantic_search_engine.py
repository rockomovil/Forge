#!/usr/bin/env python3

from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[2]

CONCEPTS = json.loads(
    (ROOT / "runtime/knowledge/knowledge_concepts.json").read_text()
)

INDEX = json.loads(
    (ROOT / "runtime/knowledge/knowledge_index.json").read_text()
)

parser = argparse.ArgumentParser()

parser.add_argument(
    "--query",
    required=True
)

args = parser.parse_args()

query = args.query.lower()

modules = INDEX["indexes"]["by_module"]
concepts = CONCEPTS["concepts"]

scores = {}

#
# Concept matches
#

for concept, refs in concepts.items():

    score = 0

    if query == concept:
        score = 100
    elif query in concept:
        score = 75
    elif concept in query:
        score = 50

    if score == 0:
        continue

    for module in refs:
        scores[module] = max(scores.get(module, 0), score)

#
# Module name matches
#

for module in modules:

    score = scores.get(module, 0)

    if query == module.lower():
        score = max(score, 120)
    elif query in module.lower():
        score = max(score, 90)

    scores[module] = score

matches = [
    (m, s)
    for m, s in scores.items()
    if s > 0
]

matches.sort(
    key=lambda x: (-x[1], x[0])
)

print("=" * 60)
print("FORGE-KNOWLEDGE-0009")
print("Knowledge Semantic Search Engine")
print("=" * 60)
print("Query   :", query)
print("Matches :", len(matches))
print()

for module, score in matches[:100]:
    print(f"{score:3}  {module}")

print()
print("STATUS : PASS")
