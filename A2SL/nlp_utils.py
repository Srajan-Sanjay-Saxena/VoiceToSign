"""
Utility helpers for the Voice2Sign NLP pipeline.

- Asset registry: scans the static assets directory for available .mp4 signs
- Stopword set: hardcoded English stopwords, negation words preserved
- Synonym lookup: manual synonym map
"""

import os
from functools import lru_cache

# ---------------------------------------------------------------------------
# Asset Registry
# ---------------------------------------------------------------------------

_asset_registry = None
_multi_word_assets = None


def _scan_assets(assets_dir):
    """Walk *assets_dir* and return (single_word_map, multi_word_list)."""
    singles = {}
    multis = []

    for fname in os.listdir(assets_dir):
        if not fname.lower().endswith(".mp4"):
            continue
        stem = fname[:-4]
        key = stem.lower()
        if " " in stem:
            parts = [w.lower() for w in stem.split()]
            multis.append((parts, stem))
            singles[key] = stem
        else:
            singles[key] = stem

    multis.sort(key=lambda x: len(x[0]), reverse=True)
    return singles, multis


def build_asset_registry(assets_dir):
    """Populate the module-level asset registry by scanning *assets_dir*."""
    global _asset_registry, _multi_word_assets
    _asset_registry, _multi_word_assets = _scan_assets(assets_dir)


def get_asset_registry():
    if _asset_registry is None:
        raise RuntimeError("Asset registry not initialised – call build_asset_registry() first.")
    return _asset_registry


def get_multi_word_assets():
    if _multi_word_assets is None:
        raise RuntimeError("Asset registry not initialised – call build_asset_registry() first.")
    return _multi_word_assets


def has_video(word):
    """Return the asset stem if a video exists for *word*, else None."""
    reg = get_asset_registry()
    return reg.get(word.lower())


# ---------------------------------------------------------------------------
# Stopwords (negation words preserved)
# ---------------------------------------------------------------------------

_STOPWORDS = frozenset({
    "a", "an", "the", "this", "that", "these", "those",
    "in", "on", "at", "to", "for", "of", "with", "by",
    "from", "up", "about", "into", "through", "during",
    "above", "below", "between", "under", "over", "out",
    "off", "against", "further",
    "and", "but", "or", "so", "yet", "both", "either",
    "than", "because", "while", "although", "though",
    "am", "is", "are", "was", "were",
    "be", "been", "being",
    "has", "have", "had", "having",
    "do", "does", "did", "doing",
    "will", "shall", "would", "should", "could",
    "may", "might", "must", "need",
    "'s", "'re", "'ve", "'ll", "'d", "'m",
    "just", "very", "really", "quite", "too", "also",
    "then", "there", "here", "own", "same", "other",
    "each", "every", "any", "some", "such", "only",
    "nor", "as", "if", "once", "until", "since",
    "again", "further", "already", "still",
    "whom",
})


@lru_cache(maxsize=1)
def get_stopwords():
    return _STOPWORDS


# ---------------------------------------------------------------------------
# Synonym Map
# ---------------------------------------------------------------------------

_SYNONYM_MAP = {
    "glad": ["happy"], "joyful": ["happy"], "cheerful": ["happy"],
    "delighted": ["happy"], "pleased": ["happy"], "content": ["happy"],
    "unhappy": ["sad"], "miserable": ["sad"], "upset": ["sad"],
    "angry": ["fight"], "furious": ["fight"], "mad": ["fight"],
    "scared": ["sad"], "afraid": ["sad"],
    "hi": ["hello"], "hey": ["hello"], "greetings": ["hello"],
    "goodbye": ["bye"], "farewell": ["bye"],
    "speak": ["talk"], "tell": ["talk"], "say": ["talk"],
    "run": ["walk"], "stroll": ["walk"], "jog": ["walk"],
    "observe": ["see"], "watch": ["see"], "look": ["see"], "view": ["see"],
    "assist": ["help"], "aid": ["help"], "support": ["help"],
    "consume": ["eat"], "dine": ["eat"],
    "depart": ["go"], "leave": ["go"], "exit": ["go"],
    "arrive": ["come"], "enter": ["come"],
    "remain": ["stay"], "wait": ["stay"],
    "giggle": ["laugh"], "chuckle": ["laugh"],
    "educate": ["learn"], "teach": ["learn"],
    "alter": ["change"], "modify": ["change"],
    "create": ["invent"], "build": ["invent"], "make": ["invent"],
    "complete": ["finish"], "end": ["finish"], "done": ["finish"],
    "request": ["ask"], "inquire": ["ask"],
    "clean": ["wash"],
    "lovely": ["beautiful"], "gorgeous": ["beautiful"], "attractive": ["pretty"],
    "excellent": ["great"], "wonderful": ["great"], "fantastic": ["great"],
    "fine": ["good"], "nice": ["good"], "okay": ["good"],
    "correct": ["right"], "accurate": ["right"],
    "incorrect": ["wrong"], "false": ["wrong"],
    "entire": ["whole"],
    "occupied": ["busy"],
    "secure": ["safe"], "protected": ["safe"],
    "house": ["home"], "residence": ["home"],
    "pc": ["computer"], "laptop": ["computer"],
    "tv": ["television"],
    "university": ["college"], "school": ["college"],
    "term": ["name"], "title": ["name"],
}


def find_synonym_with_video(word, pos=None):
    """Look up *word* in the synonym map. Returns asset stem or None."""
    reg = get_asset_registry()
    candidates = _SYNONYM_MAP.get(word.lower(), [])
    for syn in candidates:
        match = reg.get(syn.lower())
        if match:
            return match
    return None


# ---------------------------------------------------------------------------
# POS tag helpers
# ---------------------------------------------------------------------------

SPACY_TO_WN_POS = {
    "VERB": "v",
    "ADJ": "a",
    "ADV": "r",
    "NOUN": "n",
}


def spacy_pos_to_wn(spacy_pos):
    return SPACY_TO_WN_POS.get(spacy_pos)
