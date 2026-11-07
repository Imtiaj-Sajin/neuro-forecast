"""
Data preparation for CSC5515 G24 project
Time-Restricted Evidence Retrieval for Predicting Neuroscience Experimental Results with LLMs

Steps
  1. tests   Clean the BrainBench test cases, mark the result span (sentences that differ
             between the original and altered abstract) and print statistics.
  2. corpus  Download Journal of Neuroscience abstracts (PubMed, 2010-2024) with PMID,
             DOI and publication date through NCBI E-utilities.
  3. refs    Map each test DOI to its PMID and download its cited references
             (relevance labels for Recall@k and MRR).

Usage
  python prepare_data.py tests  --human BrainBench_Human_v0.1.csv --gpt4 BrainBench_GPT-4_v0.1.csv
  python prepare_data.py corpus --start 2010 --end 2024
  python prepare_data.py refs

The BrainBench CSV files are downloaded from huggingface.co/datasets/BrainGPT.
Set NCBI_API_KEY (optional) to raise the E-utilities rate limit. Output goes to data/processed.
"""
import argparse
import difflib
import json
import os
import re
import statistics
import time
import xml.etree.ElementTree as ET

OUT = os.path.join("data", "processed")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[])")


# ---------- 1. test cases ----------

def clean(text):
    text = str(text).replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text):
    return [s for s in SENT_SPLIT.split(clean(text)) if s]


def result_span(original, altered):
    """Return the sentence lists and the indices of sentences that differ."""
    so, sa = split_sentences(original), split_sentences(altered)
    changed_o, changed_a = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, so, sa).get_opcodes():
        if tag != "equal":
            changed_o += list(range(i1, i2))
            changed_a += list(range(j1, j2))
    return so, sa, changed_o, changed_a


def prepare_tests(path, split):
    import pandas as pd
    df = pd.read_csv(path)
    rows, dropped = [], 0
    for i, r in df.iterrows():
        so, sa, co, ca = result_span(r["original_abstract"], r["incorrect_abstract"])
        if not co or not ca:
            dropped += 1
            continue
        rows.append({
            "id": f"{split}-{i}",
            "doi": clean(r["doi"]),
            "section": clean(r["journal_section"]),
            "original_sents": so,
            "altered_sents": sa,
            "result_idx_original": co,
            "result_idx_altered": ca,
            # sentences before the first result sentence (query variant Q1)
            "background": " ".join(so[:min(co)]),
            # all sentences that are identical in both versions (query variant Q2)
            "context": " ".join(s for k, s in enumerate(so) if k not in co),
        })
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/{split}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    words = [sum(len(r["original_sents"][k].split()) for k in r["result_idx_original"]) for r in rows]
    nchg = [len(r["result_idx_original"]) for r in rows]
    sections = {}
    for r in rows:
        sections[r["section"]] = sections.get(r["section"], 0) + 1
    print(f"[{split}] items kept {len(rows)}, dropped {dropped}")
    print(f"[{split}] items per section {sections}")
    print(f"[{split}] changed sentences per item {dict(sorted({n: nchg.count(n) for n in set(nchg)}.items()))}")
    print(f"[{split}] result-span words mean {statistics.mean(words):.1f}, min {min(words)}, max {max(words)}")


# ---------- 2. PubMed corpus ----------

def eutils(endpoint, **params):
    import requests
    if os.environ.get("NCBI_API_KEY"):
        params["api_key"] = os.environ["NCBI_API_KEY"]
    for attempt in range(5):
        resp = requests.get(EUTILS + endpoint, params=params, timeout=60)
        if resp.status_code == 200:
            time.sleep(0.12 if "api_key" in params else 0.4)
            return resp.text
        time.sleep(2 ** attempt)
    resp.raise_for_status()


MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]


def to_month(value):
    if not value:
        return 1
    if value.isdigit():
        return int(value)
    return MONTHS.index(value[:3].lower()) + 1 if value[:3].lower() in MONTHS else 1


def parse_articles(xml_text):
    docs = []
    for art in ET.fromstring(xml_text).findall(".//PubmedArticle"):
        pmid = art.findtext(".//MedlineCitation/PMID")
        abstract = " ".join("".join(a.itertext()) for a in art.findall(".//Abstract/AbstractText"))
        if not abstract.strip():
            continue
        date = art.find(".//ArticleDate")
        if date is None:
            date = art.find(".//JournalIssue/PubDate")
        year = date.findtext("Year") if date is not None else None
        month = to_month(date.findtext("Month") if date is not None else None)
        doi = next((i.text for i in art.findall(".//ArticleIdList/ArticleId") if i.get("IdType") == "doi"), None)
        docs.append({
            "pmid": pmid,
            "doi": doi,
            "date": f"{year}-{int(month):02d}" if year else None,
            "title": clean("".join(art.find(".//ArticleTitle").itertext())),
            "abstract": clean(abstract),
        })
    return docs


def prepare_corpus(start, end, journal):
    os.makedirs(OUT, exist_ok=True)
    n = 0
    with open(f"{OUT}/corpus.jsonl", "w") as f:
        for year in range(start, end + 1):
            term = f'"{journal}"[ta] AND {year}[dp] AND hasabstract'
            res = json.loads(eutils("esearch.fcgi", db="pubmed", term=term, retmode="json",
                                    usehistory="y", retmax=0))["esearchresult"]
            count = int(res["count"])
            for retstart in range(0, count, 200):
                xml_text = eutils("efetch.fcgi", db="pubmed", query_key=res["querykey"],
                                  WebEnv=res["webenv"], retstart=retstart, retmax=200, retmode="xml")
                for d in parse_articles(xml_text):
                    f.write(json.dumps(d) + "\n")
                    n += 1
            print(f"{year}: {count} records")
    print(f"corpus documents written: {n}")


# ---------- 3. cited references ----------

def prepare_refs():
    labels = {}
    for split in ("test", "dev"):
        if not os.path.exists(f"{OUT}/{split}.jsonl"):
            continue
        for line in open(f"{OUT}/{split}.jsonl"):
            item = json.loads(line)
            res = json.loads(eutils("esearch.fcgi", db="pubmed", term=f'{item["doi"]}[aid]',
                                    retmode="json"))["esearchresult"]["idlist"]
            if not res:
                labels[item["id"]] = {"pmid": None, "refs": []}
                continue
            links = json.loads(eutils("elink.fcgi", dbfrom="pubmed", db="pubmed", id=res[0],
                                      linkname="pubmed_pubmed_refs", retmode="json"))
            refs = [l for ls in links["linksets"] for db in ls.get("linksetdbs", []) for l in db["links"]]
            labels[item["id"]] = {"pmid": res[0], "refs": refs}
    corpus = {json.loads(l)["pmid"] for l in open(f"{OUT}/corpus.jsonl")} if os.path.exists(
        f"{OUT}/corpus.jsonl") else set()
    for v in labels.values():
        v["refs_in_corpus"] = [p for p in v["refs"] if p in corpus]
    json.dump(labels, open(f"{OUT}/relevance.json", "w"), indent=1)
    with_refs = sum(1 for v in labels.values() if v["refs_in_corpus"])
    print(f"items with PMID {sum(1 for v in labels.values() if v['pmid'])} / {len(labels)}; "
          f"items with at least one cited reference in corpus {with_refs}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["tests", "corpus", "refs"])
    ap.add_argument("--human", default="BrainBench_Human_v0.1.csv")
    ap.add_argument("--gpt4", default="BrainBench_GPT-4_v0.1.csv")
    ap.add_argument("--start", type=int, default=2010)
    ap.add_argument("--end", type=int, default=2024)
    ap.add_argument("--journal", default="J Neurosci")
    a = ap.parse_args()
    if a.step == "tests":
        prepare_tests(a.human, "test")
        prepare_tests(a.gpt4, "dev")
    elif a.step == "corpus":
        prepare_corpus(a.start, a.end, a.journal)
    else:
        prepare_refs()
