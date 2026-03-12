import os
from collections import defaultdict
import json

input_files = "./lemmas"

index = defaultdict(list)

for filename in os.listdir(input_files):
    with open(os.path.join(input_files, filename), "r", encoding="utf-8") as f:
        for line in f:
            lemma, tokens = line.strip().split(" ", 1)
            # print(f"{lemma}: {tokens}")

            if lemma not in index:
                index[lemma] = []

            index[lemma].append(filename.lower().lstrip("lemmas_"))

print(index)

with open("index.json", "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=4)
