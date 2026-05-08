"""
Full NLP pipeline for Voice2Sign.

Converts an English sentence into a list of ISL gloss tokens mapped to
video assets or fingerspelling characters.

Pipeline stages:
1. Preprocess — lowercase, detect & merge multi-word phrases
2. Analyse   — spaCy: tokenise, POS-tag, lemmatise, dependency-parse
3. ISL gloss — stopword removal, negation handling, pronoun mapping,
               lemma->asset matching with synonym fallback, SOV reordering,
               tense-marker insertion
4. Resolve   — map each gloss token to an asset or split into characters
"""

from __future__ import annotations

import logging

import spacy
from spacy.tokens import Doc

from . import nlp_utils

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Lazy-loaded spaCy model
# ---------------------------------------------------------------------------

_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


# ---------------------------------------------------------------------------
# 1. Pre-processing
# ---------------------------------------------------------------------------

def _merge_multi_word_phrases(tokens):
    """Greedily merge consecutive tokens that match a multi-word asset."""
    multi = nlp_utils.get_multi_word_assets()
    if not multi:
        return tokens

    result = []
    i = 0
    while i < len(tokens):
        matched = False
        for parts, stem in multi:
            n = len(parts)
            if i + n <= len(tokens) and [t.lower() for t in tokens[i:i + n]] == parts:
                result.append(stem)
                i += n
                matched = True
                break
        if not matched:
            result.append(tokens[i])
            i += 1
    return result


# ---------------------------------------------------------------------------
# 2. Analysis (spaCy)
# ---------------------------------------------------------------------------

def _detect_tense(doc):
    """Heuristic tense detection from spaCy POS + morphology."""
    counts = {"past": 0, "future": 0, "present": 0, "present_continuous": 0}

    for token in doc:
        tag = token.tag_
        if tag == "MD":
            if token.text.lower() in ("will", "shall", "'ll"):
                counts["future"] += 1
        elif tag in ("VBD", "VBN"):
            counts["past"] += 1
        elif tag == "VBG":
            counts["present_continuous"] += 1
            counts["present"] += 1
        elif tag in ("VBP", "VBZ"):
            counts["present"] += 1

    if not any(counts.values()):
        return "present"
    return max(counts, key=counts.get)


# ---------------------------------------------------------------------------
# 3. ISL gloss conversion
# ---------------------------------------------------------------------------

_PRONOUN_MAP = {
    "i": "Me", "me": "Me", "my": "My", "mine": "My", "myself": "Self",
    "he": "He", "him": "He", "his": "His", "himself": "Self",
    "she": "Her", "her": "Her", "hers": "Her", "herself": "Self",
    "we": "We", "us": "Us", "our": "Our", "ours": "Our", "ourselves": "Self",
    "they": "They", "them": "They", "their": "Their", "theirs": "Their", "themselves": "Self",
    "you": "You", "your": "Your", "yours": "Your", "yourself": "Yourself", "yourselves": "Yourself",
    "it": "It", "its": "It", "itself": "Self",
}


def _map_pronoun(word):
    return _PRONOUN_MAP.get(word.lower())


def _resolve_token(token_text, spacy_pos):
    """Try to find a video asset for *token_text*."""
    hit = nlp_utils.has_video(token_text)
    if hit:
        return hit

    wn_pos = nlp_utils.spacy_pos_to_wn(spacy_pos)
    hit = nlp_utils.find_synonym_with_video(token_text, pos=wn_pos)
    if hit:
        return hit

    return None


def _sov_reorder(tokens_with_dep):
    """Basic SOV reordering for ISL based on dependency parse."""
    subjects = []
    objects = []
    verbs = []
    wh_words = []
    negation = []
    others = []

    for t in tokens_with_dep:
        dep = t["dep"]
        pos = t["pos"]
        text = t["text"]
        head_dep = t["head_dep"]

        if dep in ("nsubj", "nsubjpass"):
            subjects.append(text)
        elif dep in ("poss", "compound"):
            if head_dep in ("nsubj", "nsubjpass", "ROOT"):
                subjects.insert(max(len(subjects) - 1, 0), text)
            elif head_dep in ("dobj", "pobj", "attr", "dative", "oprd", "acomp"):
                objects.insert(max(len(objects) - 1, 0), text)
            else:
                others.append(text)
        elif dep in ("dobj", "pobj", "attr", "dative", "oprd", "acomp"):
            objects.append(text)
        elif pos == "VERB" or dep == "ROOT":
            verbs.append(text)
        elif dep == "advmod" and text.lower() in (
            "what", "where", "when", "why", "how", "which", "who", "whom", "whose",
        ):
            wh_words.append(text)
        elif dep == "neg" or text.lower() in ("not", "no", "never"):
            negation.append(text)
        else:
            others.append(text)

    # ISL order: Subject + Object + Negation + Others + Verb + WH-word
    return subjects + objects + negation + others + verbs + wh_words


# ---------------------------------------------------------------------------
# 4. Full pipeline
# ---------------------------------------------------------------------------

def process_text(text):
    """Convert an English sentence to a list of ISL animation tokens.

    Each returned string is either:
    - an asset stem matching <stem>.mp4
    - a single uppercase character for fingerspelling
    """
    text = (text or "").strip()
    if not text:
        raise ValueError("Input text is empty.")

    nlp = _get_nlp()

    # 1. spaCy analysis
    doc = nlp(text.lower())

    # 2. Tense detection
    tense = _detect_tense(doc)

    # 3. Multi-word phrase detection
    raw_words = [token.text for token in doc if not token.is_punct and not token.is_space]
    merged_raw = _merge_multi_word_phrases(raw_words)

    merged_set = set()
    phrase_tokens = []
    ri = 0
    for m in merged_raw:
        if " " in m:
            parts = m.lower().split()
            for p in parts:
                merged_set.add((ri, p))
                ri += 1
            phrase_tokens.append(m)
        else:
            ri += 1

    # 4. Stopword removal + lemmatisation + pronoun mapping
    stopwords = nlp_utils.get_stopwords()
    processed = []
    token_idx = 0

    for token in doc:
        if token.is_punct or token.is_space:
            continue

        word = token.text
        lemma = token.lemma_

        if (token_idx, word.lower()) in merged_set:
            token_idx += 1
            continue
        token_idx += 1

        # pronoun mapping
        pronoun = _map_pronoun(word)
        if pronoun:
            processed.append({
                "text": pronoun,
                "dep": token.dep_,
                "pos": token.pos_,
                "head_dep": token.head.dep_,
            })
            continue

        # skip stopwords (but keep negation)
        if word in stopwords and token.dep_ != "neg":
            continue

        # resolve token to asset
        if token.pos_ in ("VERB", "ADJ", "ADV"):
            resolved = _resolve_token(lemma, token.pos_)
        else:
            resolved = _resolve_token(word, token.pos_)

        if resolved is None and word != lemma:
            resolved = _resolve_token(lemma, token.pos_)

        if resolved is None:
            resolved = _resolve_token(word.title(), token.pos_)

        final_text = resolved if resolved else word
        processed.append({
            "text": final_text,
            "dep": token.dep_,
            "pos": token.pos_,
            "head_dep": token.head.dep_,
        })

    # 5. Combine phrase tokens with processed single tokens
    all_tokens = phrase_tokens + [t["text"] for t in processed]
    all_tokens = _merge_multi_word_phrases(all_tokens)

    # 6. SOV reordering
    if not phrase_tokens and len(processed) > 1:
        reordered = _sov_reorder(processed)
    else:
        reordered = all_tokens

    # 7. Tense marker insertion
    if tense == "past":
        reordered = ["Before"] + reordered
    elif tense == "future":
        if "Will" not in reordered:
            reordered = ["Will"] + reordered
    elif tense == "present_continuous":
        reordered = ["Now"] + reordered

    # 8. Asset resolution — video or fingerspelling
    final_tokens = []
    for word in reordered:
        hit = nlp_utils.has_video(word)
        if hit:
            final_tokens.append(hit)
        else:
            for ch in word.upper():
                if ch.isalpha():
                    final_tokens.append(ch)

    return final_tokens
