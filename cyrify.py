"""Transliterate English text to Cyrillic by phonetic approximation (Runglish style).

Two-pass rule engine:
  Pass 1 — Regex rules (context-sensitive: boundaries, lookahead)
  Pass 2 — Literal rules (flat longest-match substitution on raw Latin text)
Exception dict for genuinely irregular words.
"""

import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# === Exception dict (words rules get wrong) ===
DICT = {
    "the": "да", "a": "а", "an": "ан",
    "of": "оф", "to": "то",
    "I": "ай", "you": "ю", "your": "юър",
    "we": "уи", "me": "ми",
    "my": "май", "by": "бай",
    "one": "уан", "two": "ту", "once": "уанс",
    "was": "уас", "were": "уер", "are": "аре",
    "is": "из", "does": "даз",
    "done": "дан", "none": "нан",
    "come": "кам", "some": "съм",
    "say": "сей", "says": "сез", "said": "сед",
    "buy": "бай", "guy": "гай",
    "bury": "бери", "busy": "бизи",
    "build": "билд", "built": "билт",
    "give": "гив", "gift": "гифт", "girl": "гърл", "guard": "гард",
    "friend": "френд",
    "eye": "ай", "eyes": "айс",
    "heart": "харт",
    "tongue": "танг", "people": "пипл",
    "pretty": "прити", "beautiful": "бьютифул",
    "enough": "инаф",
    "hour": "ауър", "answer": "ансър",
    "debt": "дет", "subtle": "сатл", "sword": "сорд",
    "vehicle": "виикл", "view": "вью",
    "colonel": "кърнл", "lieutenant": "лефтенънт",
    "oh": "оу",
    "believe": "белийв",
    "actually": "акшуали",
    "absolutely": "апсолутли",
    "ridiculous": "рейдикюлъс",
    "cannot": "кенот",
    "can't": "кент",
    "listen": "лисен",
    "because": "бикъз",
    "our": "ауър",
    "their": "деир",
    "about": "абоут",
    "always": "ауейс",
    "everything": "евритинг",
    "behind": "бихайнд",
    "backs": "бекс",
    "movie": "моуви",
    "truth": "трут",
    "whole": "хоул",
    "going": "гоуинг",
    "here": "хиър",
    "there": "дер",
    "where": "уер",
    "what": "уот",
    "why": "уай",
    "try": "трай",
    "trying": "трайинг",
    "overriding": "оверрайдинг",
    "understand": "ъндърстенд",
    "different": "диферент",
    "semantic": "семантик",
    "rules": "рулес",
    "convey": "конвей",
    "okay": "окей",
    "nosed": "нозед",
    "planning": "пленинг",
    "plan": "плен",
    "building": "билдинг",
    "or": "ор",
    "brother": "брадър",
    "but": "бът",
    "specific": "специфик",
    "reply": "риплей",
    "pipeline": "пайплейн",
    "through": "тхру",
    "am": "ем",
    "Am": "Ем",
}

# === PASS 1: Regex rules (context-sensitive) ===
REGEX_PASS = [
    # y context
    (r"\by(?=[aeiou])", "й"),
    (r"y\b", "и"),
    (r"y", "ай"),

    # short a before n + consonant → e
    (r"an(?=[bcdfghjklmnpqrstvwxz])", "ен"),

    # magic-e: vowel + C + e at word end
    (r"i(?=[bcdfghjklmnpqrstvwxz]e\b)", "ай"),
    (r"a(?=[bcdfghjklmnpqrstvwxz]e\b)", "ей"),
    (r"o(?=[bcdfghjklmnpqrstvwxz]e\b)", "оу"),
    (r"u(?=[bcdfghjklmnpqrstvwxz]e\b)", "ю"),
    # magic-e mid-word (compound boundary): vowel + C + e + letter
    (r"i(?=[bcdfghjklmnpqrstvwxz]e(?=[a-z]))", "ай"),
    (r"a(?=[bcdfghjklmnpqrstvwxz]e(?=[a-z]))", "ей"),
    (r"o(?=[bcdfghjklmnpqrstvwxz]e(?=[a-z]))", "оу"),
    (r"u(?=[bcdfghjklmnpqrstvwxz]e(?=[a-z]))", "ю"),

    # wh
    (r"\bwh(?=[aeiou])", "у"),
    (r"\bwh(?=o)", "х"),

    # th context: voiced vs voiceless approximation
    (r"\bthe", "де"),
    (r"\btha", "да"),
    (r"\bthi", "ди"),
    (r"\btho", "до"),
    (r"\bthu", "ду"),
    (r"\bthr", "тр"),
    (r"th", "д"),
]

# === PASS 2: Literal rules (longest-match regex alternation) ===
LITERAL_RULES = [
    # Consonant digraphs
    "sh", "ш", "ch", "ч", "ck", "к", "tch", "ч", "cht", "чт",
    "ph", "ф", "kn", "н", "gn", "н", "ps", "пс", "wr", "р",
    "ng", "нг", "nk", "нк", "qu", "ку",
    # c softener
    "ce", "се", "ci", "си", "cy", "сы",
    # Endings
    "tion", "шн", "sion", "жн", "ture", "чур",
    # Vowel digraphs (longest first)
    "eigh", "ей", "igh", "ай", "augh", "о", "ough", "оу",
    "ee", "и", "oo", "у", "ou", "ау", "ow", "оу",
    "oi", "ой", "oy", "ой", "ay", "ей", "ai", "ей",
    "ea", "и", "oa", "оу", "ui", "уи", "ie", "и",
    "ei", "ей", "eu", "ю", "ew", "ю", "au", "о", "aw", "о",
    # R-colored vowels
    "wor", "уър", "war", "уор",
    "air", "эр", "ear", "ир",
    "er", "ер", "ir", "ер", "ur", "ер", "or", "ор", "ar", "ар",
    # Single vowels
    "a", "а", "e", "е", "i", "и", "o", "о", "u", "а",
    # Single consonants
    "b", "б", "c", "к", "d", "д", "f", "ф", "g", "г",
    "h", "х", "j", "дж", "k", "к", "l", "л", "m", "м",
    "n", "н", "p", "п", "q", "к", "r", "р", "s", "с",
    "t", "т", "v", "в", "w", "у", "x", "кс", "z", "з",
]

_LIT_TUPLES = list(zip(LITERAL_RULES[::2], LITERAL_RULES[1::2]))
_LIT_SORTED = sorted(_LIT_TUPLES, key=lambda r: len(r[0]), reverse=True)
_LIT_PATTERN = re.compile("|".join(re.escape(p) for p, _ in _LIT_SORTED), re.IGNORECASE)
_LIT_REPL = {p.lower(): r for p, r in _LIT_SORTED}


def _apply_rules(word: str) -> str:
    """Apply phonetic rules to a word not in dictionary."""
    w = word.lower()

    for pattern, repl in REGEX_PASS:
        w = re.sub(pattern, repl, w)

    def replacer(m):
        return _LIT_REPL.get(m.group(0).lower(), m.group(0))
    w = _LIT_PATTERN.sub(replacer, w)

    # Post-processing
    if w.endswith("е") and len(w) > 1:
        w = w[:-1]
    if w.endswith("ер") and len(w) > 4:
        w = w[:-2] + "ър"

    if word[:1].isupper():
        w = w[:1].upper() + w[1:]
    return w


def cyrify(text: str) -> str:
    """Transliterate English text to Cyrillic phonetic approximation."""
    out = []
    for token in re.split(r"(\W+)", text):
        if token.strip() == "" or not re.search(r"[a-zA-Z]", token):
            out.append(token)
            continue
        translated = DICT.get(token) or DICT.get(token.lower())
        if translated:
            if token[:1].isupper() and not token.isupper():
                translated = translated[:1].upper() + translated[1:]
            elif token.isupper() and len(token) > 1:
                translated = translated.upper()
            out.append(translated)
        else:
            out.append(_apply_rules(token))

    result = "".join(out)
    result = re.sub(r"([бвгджклмнпртфхцч])\1", r"\1", result)
    result = re.sub(r"([.!?]\s+)([А-Я])", lambda m: m.group(1) + m.group(2).lower(), result)
    return result


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--file":
        with open(sys.argv[2], encoding="utf-8") as f:
            text = f.read()
        print(cyrify(text))
        return
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        print(cyrify(text))
        return
    if not sys.stdin.isatty():
        text = sys.stdin.read()
        print(cyrify(text))
        return
    print("Cyrillic transliterator (Runglish). Ctrl+C or empty line to exit.\n")
    try:
        while True:
            line = input("> ")
            if not line:
                break
            print(cyrify(line))
            print()
    except (KeyboardInterrupt, EOFError):
        pass


if __name__ == "__main__":
    main()
