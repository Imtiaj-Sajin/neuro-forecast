# Time-Restricted Evidence Retrieval for Predicting Neuroscience Experimental Results with LLMs

CSC5515 Natural Language Processing, Fall 2026-27, American International University-Bangladesh
Group G24 (individual project) · Md. Imtiaj Alam Sajin (26-94090-2) · Project type C (retrieval-augmented generation)

## Overview

BrainBench gives a language model two versions of a 2023 *Journal of Neuroscience* abstract that differ only in their results, and asks it to identify the published one. Existing models decide from parametric knowledge alone. This project adds retrieval of prior literature, restricted to papers published before each test article, and scores only the result-sentence tokens conditioned on the retrieved abstracts and the background text.

Research questions:

1. Does conditioning on time-restricted prior abstracts improve accuracy compared with scoring without retrieval?
2. How does the effect depend on the retriever, the number of retrieved abstracts and the retrieval quality?
3. How much would accuracy be inflated if the time restriction were removed, and how much of this comes from retrieving the test article itself?

The full plan is in `docs/proposal/CSC5515_G24_Proposal.pdf`.

## Repository structure

```
prepare_data.py          data cleaning, PubMed corpus download, cited-reference download
released_baselines.py    zero-shot accuracy from the released BrainBench perplexities
requirements.txt
data/raw/                BrainBench CSV files (downloaded, not committed)
data/processed/          cleaned test/dev sets, corpus, relevance labels (generated, not committed)
outputs/                 results tables and statistics
docs/proposal/           initial and final proposal (PDF and LaTeX)
docs/feedback/           instructor feedback on the proposals
research/                topic selection, dataset checks, related work and design notes
```

## Setup

```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Optional: set `NCBI_API_KEY` as an environment variable to raise the PubMed rate limit. Keys are never written into the code.

## Data preparation

1. Download the two BrainBench CSV files into `data/raw/` (see `data/raw/README.md`).
2. Run:

```
python prepare_data.py tests  --human data/raw/BrainBench_Human_v0.1.csv --gpt4 data/raw/BrainBench_GPT-4_v0.1.csv
python prepare_data.py corpus --start 2010 --end 2024
python prepare_data.py refs
```

Outputs are written to `data/processed/`.

## Released baselines

```
git clone --depth 1 https://github.com/braingpt-lovelab/brainbench_experiments
python released_baselines.py --brainbench_dir brainbench_experiments
```

| Model | Accuracy (%) | Errors |
|---|---|---|
| Llama-2-7B | 81.5 | 37 |
| Galactica-6.7B | 83.0 | 34 |
| Mistral-7B-v0.1 (possibly contaminated) | 83.0 | 34 |
| BrainGPT, Mistral-7B-v0.1 with LoRA (possibly contaminated) | 86.0 | 28 |

## Progress

| Week | Task | Status |
|---|---|---|
| 4 | Initial proposal | Submitted 4 Nov; topic approved |
| 6 | Final proposal; data cleaning script; released baselines | Done |
| 6 | PubMed corpus and cited-reference download | In progress |
| 7 | BM25 and MedCPT indexes with date filtering; zero-shot and BM25 baselines on the development set | Planned |
| 8 | Result-token scoring with retrieved context; choice of k on the development set | Planned |
| 9-10 | Test runs, query variants, leakage conditions, ablations, retrieval quality, calibration | Planned |
| 11 | Hand-judged relevance; error analysis; code package | Planned |
| 12 | Final report | Planned |

## Licences

Code in this repository: MIT. BrainBench test cases: Apache-2.0 (human-written set). PubMed abstracts are downloaded by the scripts and not redistributed.
