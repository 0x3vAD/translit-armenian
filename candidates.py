from spylls.hunspell import Dictionary
from mapping import LATIN_TO_ARMENIAN


def generate_candidates(word: str, index: int = 0) -> list[str]:
    if index == len(word):
        return [""]

    results = []
    for lat, arm in LATIN_TO_ARMENIAN:
        if word[index:].startswith(lat):
            options = (arm,) if isinstance(arm, str) else arm
            for option in options:
                rest = generate_candidates(word, index + len(lat))
                results.extend(option + r for r in rest)
    return results


def get_choices(word: str, dictionary: Dictionary) -> list[str]:
    candidates = list(dict.fromkeys(generate_candidates(word)))
    valid = [c for c in candidates if dictionary.lookup(c)]

    if valid:
        return valid
    else:
        return candidates
