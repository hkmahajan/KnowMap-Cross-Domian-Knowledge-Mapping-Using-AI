import os
import pandas as pd
import spacy

# Load spaCy once
nlp = spacy.load("en_core_web_sm")

def extract_triples_from_sentence(sentence):
    """
    Extract triples (subject, relation, object) from a single sentence
    using spaCy dependency parsing.
    Returns list of (subj, rel, obj, confidence)
    """
    doc = nlp(sentence)
    triples = []

    for token in doc:
        # Look for verbs
        if token.pos_ == "VERB":
            subj = None
            obj = None

            # Find nominal subject (nsubj)
            for child in token.children:
                if "subj" in child.dep_:
                    subj = child.text
                    # Include compound names like "Apple Inc"
                    subj = " ".join([tok.text for tok in child.subtree])
                    break

            # Find direct object (dobj)
            for child in token.children:
                if "obj" in child.dep_:
                    obj = child.text
                    obj = " ".join([tok.text for tok in child.subtree])
                    break

            if subj and obj:
                triples.append((subj, token.lemma_, obj, 0.9))

    return triples

def extract_triples_from_text(text):
    """
    Extract triples from full text.
    """
    triples = []
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    for s in sentences:
        triples.extend(extract_triples_from_sentence(s))

    # Remove duplicates
    triples = list({(sub, rel, obj): (sub, rel, obj, conf) 
                    for sub, rel, obj, conf in triples}.values())
    return triples

def extract_triples_from_file(path: str):
    """
    Extract triples from CSV/Excel file containing text in any column.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    ext = os.path.splitext(path)[1].lower()
    if ext in [".csv", ".txt"]:
        df = pd.read_csv(path, encoding='utf-8', dtype=str, keep_default_na=False)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(path, dtype=str)
    else:
        raise ValueError("Unsupported file type: " + ext)

    triples = []
    for col in df.columns:
        for v in df[col].astype(str).tolist():
            triples.extend(extract_triples_from_text(v))
    return triples

def save_triples_to_csv(triples, out="data/triples.csv"):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df = pd.DataFrame(triples, columns=["subject", "relation", "object", "confidence"])
    df["confidence"] = df["confidence"].astype(float)
    df.to_csv(out, index=False)
    return out

# Demo run
if __name__ == "__main__":
    demo = ("Apple Inc designs innovative consumer electronics and develops the iPhone which revolutionized mobile communication. "
            "Ada Lovelace developed early algorithms for Charles Babbage's Analytical Engine, influencing modern computing.")
    t = extract_triples_from_text(demo)
    save_triples_to_csv(t)
    print("Saved demo triples:", t)
