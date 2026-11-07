# Processed data

Created by prepare_data.py. These files are not committed.

| File | Created by | Content |
|---|---|---|
| test.jsonl | `python prepare_data.py tests` | 200 human-written test items with sentence lists and the result-span indices |
| dev.jsonl | `python prepare_data.py tests` | 100 GPT-4 development items in the same format |
| corpus.jsonl | `python prepare_data.py corpus` | Journal of Neuroscience PubMed records 2010-2024 (PMID, DOI, date, title, abstract) |
| relevance.json | `python prepare_data.py refs` | PubMed ID of each test article, its cited references, and the references present in the corpus |
