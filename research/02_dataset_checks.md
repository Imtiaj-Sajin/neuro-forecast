# Dataset checks

## BrainBench test cases (Hugging Face, BrainGPT organisation)

- BrainBench_Human_v0.1.csv: 200 rows, columns doi, journal_section, original_abstract, incorrect_abstract; licence Apache-2.0 on the dataset card.
- BrainBench_GPT-4_v0.1.csv: 100 rows, same columns; no licence stated on the dataset card.

## Statistics of the human-written test set

Computed from `data/swap_human_abstracts.json` in braingpt-lovelab/brainbench_experiments (result sentences of each item), saved in `outputs/test_set_statistics.json`.

| Section | Items |
|---|---|
| Behavioral/Cognitive | 75 |
| Systems/Circuits | 51 |
| Neurobiology of Disease | 25 |
| Development/Plasticity/Repair | 24 |
| Cellular/Molecular | 25 |

Changed sentences per item: 1 (45 items), 2 (77), 3 (41), 4 (24), 5 (8), 6 (5). Result span: mean 64.6 words, range 13-163.

Example changes (original to altered): anterior to posterior; reduces to increases; short-term to long-term; phasic to tonic; knocking down to overexpressing.

## Abstract file used in the initial proposal

`data/j_of_neuro_abstracts_2017_2022.json` in brainbench_experiments: 3,451 Journal of Neuroscience abstracts, mean 320 words, produced by `compile_j_of_neuro.py` from the training split of `BrainGPT/train_valid_split_pmc_neuroscience_2002-2022_filtered_subset`. It contains text only, without PubMed IDs or dates, so it was replaced by a PubMed download for the final proposal.

## Code licences

braingpt-lovelab/brainbench and brainbench_experiments: Apache-2.0.

## Released model results

`model_results/<model>/human_abstracts/PPL_A_and_B.npy` and `labels.npy` in brainbench_experiments give whole-abstract perplexities for both versions. `released_baselines.py` turns them into accuracies (see `outputs/released_baselines.csv`). The published BrainGPT corresponds to `lora_r256_a512_finetune_mistral_7b_v01`, a LoRA adapter on Mistral-7B-v0.1.
