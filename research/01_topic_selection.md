# Topic selection notes (4 November 2026)

Requirements for the topic: an LLM method project (not a measurement study) with a clear gap, feasible on one 16 GB GPU with public data in about six weeks, and extendable to a journal paper after the course.

## Directions considered and rejected

| Direction | Reason for rejection |
|---|---|
| Bangla smishing / scam detection | Very common in university projects |
| Bangla text simplification | Bangla topics ruled out for this project |
| Dual-adapter LoRA against fine-tuning hallucination | Close to recent work (KnownPatch; self-distillation by Kaplan, Gekhman et al., 2026) |
| Single-pass knowledge-conflict detection in RAG | Already done by hidden-state probing (2024) and CLEAR (2025) |
| Brain-inspired memory consolidation for LLMs | Crowded in 2026 (sleep-style consolidation papers and products) |
| LLM agents for neuroscience or EEG data analysis | SeekBrain, NeuroClaw, EEG Agent (AAAI 2026), NeuroWeaver, EEGAgentBench |
| Constrained JSON decoding versus reasoning | CRANE and recent analyses |
| Self-consistency early stopping | CGES (NeurIPS 2025 workshop), DeepConf |
| LoRA adapter merging; adaptive thinking budgets | Many 2026 methods |
| Knowledge conflicts in diffusion LLMs | Fast-moving area (SPREAD, Sardi); slow inference |
| Least-privilege tool policies from a small local model | Narrow gap; heavy AgentDojo engineering |
| Organoid / biocomputing experiments | Needs access to external labs (kept as a future idea) |

## Chosen direction

Evidence retrieval for BrainBench. Luo et al. (2025) proposed retrieval over the scientific literature as a next step; no follow-up applying it to BrainBench was found. The closest related work, BackTrend (arXiv:2609.24921, 2026), uses date-filtered retrieval for AI/ML research trends, which is a different domain and task. The time restriction is needed so that the model predicts from prior evidence rather than finding the published result.
