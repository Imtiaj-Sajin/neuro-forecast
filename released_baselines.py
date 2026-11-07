"""
Zero-shot BrainBench accuracy computed from the perplexities released by the BrainBench authors.

The original rule picks the abstract version with the lower perplexity over the whole abstract,
without retrieval. This script reads the released results and reports accuracy and error counts
on the 200 human-written test items (Table 3 of the final proposal).

Usage
  git clone --depth 1 https://github.com/braingpt-lovelab/brainbench_experiments
  python released_baselines.py --brainbench_dir brainbench_experiments --out outputs/released_baselines.csv
"""
import argparse
import csv
import os

import numpy as np

MODELS = {
    "meta-llama--Llama-2-7b-hf": ("Llama-2-7B", False),
    "facebook--galactica-6.7b": ("Galactica-6.7B", False),
    "mistralai--Mistral-7B-v0.1": ("Mistral-7B-v0.1", True),
    "lora_r256_a512_finetune_mistral_7b_v01": ("BrainGPT (Mistral-7B-v0.1 with LoRA)", True),
}


def main(brainbench_dir, out):
    rows = []
    for folder, (name, contaminated) in MODELS.items():
        path = os.path.join(brainbench_dir, "model_results", folder, "human_abstracts")
        ppl = np.load(os.path.join(path, "PPL_A_and_B.npy"))
        labels = np.load(os.path.join(path, "labels.npy"))
        correct = np.argmin(ppl, axis=1) == labels
        rows.append({
            "model": name,
            "possibly_contaminated": contaminated,
            "items": len(labels),
            "accuracy_percent": round(100 * correct.mean(), 1),
            "errors": int((~correct).sum()),
        })
        print(f"{name:40s} accuracy {100 * correct.mean():5.1f}%  errors {(~correct).sum()}")

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--brainbench_dir", default="brainbench_experiments")
    ap.add_argument("--out", default="outputs/released_baselines.csv")
    a = ap.parse_args()
    main(a.brainbench_dir, a.out)
