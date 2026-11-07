# Method design notes

## Scoring

For version v with result tokens R_v and context C (retrieved abstracts, then the abstract text before each result sentence):

s(v) = (1/|R_v|) * sum over t in R_v of log p(x_t | x_<t, C)

The version with the higher s(v) is chosen. Context tokens are not scored. Confidence is |s(original) - s(altered)|.

## Retrieval

- Query built only from sentences identical in both versions.
- Query variants (the three runs): Q1 sentences before the first result sentence; Q2 all identical sentences; Q3 the 15 highest TF-IDF terms of Q2.
- Retrievers: BM25 and MedCPT. Each retrieved abstract truncated to 200 tokens so that k = 5 fits Galactica's 2,048-token context.
- Time restriction: only documents published before the month of the test article.

## Leakage conditions (RQ3)

1. Time-restricted. 2. All documents except the test article. 3. All documents. Report the self-retrieval rate.

## Retrieval quality

Relevant documents: cited references of each test article (ELink pubmed_pubmed_refs) that are in the corpus. Report Recall@k and MRR; compare per-item gains for items with and without a cited reference in the top k; logistic regression of correctness on Recall@k. Hand-judge top-5 relevance for 50 queries without cited references in the corpus.

## Ablations

k in {0, 1, 3, 5}; BM25 versus MedCPT; scoring span (result sentences, differing tokens, whole abstract); model.

## Error analysis

The released baselines leave 28-37 errors per model on the test set, so errors of the main method are pooled over the test and development sets and both models (each source reported separately) to reach at least 50. Categories: direction, brain region, cell or molecule type, time scale, other; and retrieval outcome (no relevant paper, supporting, conflicting).
