# Instructor feedback on the initial proposal

Received in MS Teams, 4 November 2026. Topic approved, minor-to-moderate revisions.

> An original, well-designed study with careful baselines, statistics and a clear contamination strategy. Note that it was submitted on 4 November, after the deadline. For the final proposal (due Sat 7 Nov):
>
> 1. Leakage test (RQ3): your corpus is entirely pre-2023, so turning the time filter off changes nothing. Add 2023+ PubMed abstracts, including the test articles themselves, so the filter-off condition can actually leak results.
> 2. Retrieval quality: measure it directly. A good option is to treat each test article's cited references (those present in your corpus) as relevant documents and report Recall@k/MRR, then relate retrieval quality to accuracy gains. Otherwise, hand-judge top-k relevance for about 50 queries.
> 3. Scoring: compute perplexity only over the result-sentence (or differing) tokens, conditioned on retrieved context plus background, so that the added context does not dominate the score.
> 4. Second model: Mistral-7B-v0.1 (released Sept 2023) may have seen the 2023 test abstracts. Use another model with a pre-2023 training cutoff, or label Mistral explicitly as a possibly contaminated comparison.
> 5. Data: state exactly where the 2017-2022 abstract corpus comes from (file/script), report the test-case licence, and confirm that the three query variants form your ≥3-run variance estimate.

## How each point was addressed

See Section 1 and Table 1 of `docs/proposal/CSC5515_G24_Proposal.pdf`.

| Point | Change |
|---|---|
| 1 | Corpus rebuilt from PubMed: Journal of Neuroscience 2010-2024, including the test articles. Three conditions: time-restricted, all except the test article, all documents. Self-retrieval rate reported. |
| 2 | Cited references (ELink `pubmed_pubmed_refs`) present in the corpus are the relevant documents; Recall@k and MRR related to per-item accuracy gains; 50 hand-judged queries for items without cited references in the corpus. |
| 3 | Score is the mean log-likelihood of the result-sentence tokens only, conditioned on retrieved abstracts and background. Differing-token and whole-abstract scoring are ablations. |
| 4 | Second model is Galactica-6.7B (November 2022). Mistral-7B-v0.1 and BrainGPT (built on Mistral) are labelled possibly contaminated. |
| 5 | Old corpus file and script named; new corpus described; human test set licence Apache-2.0; three query variants are the three runs. |
