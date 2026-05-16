from spylls.hunspell import Dictionary
from mapping import LATIN_TO_ARMENIAN


def generate_candidates(word: str, index: int = 0) -> list[str]:
    if index == len(word):
        return [""]

    results = []
    for lat, arm in LATIN_TO_ARMENIAN:
        if word[index:].startswith(lat):
            print(f"Matched '{lat}' at index {index} in '{word}' → candidates: {arm}")

            options = (arm,) if isinstance(arm, str) else arm
            print(options)
            for option in options:
                rest = generate_candidates(word, index + len(lat))
                results.extend(option + r for r in rest)
    return results


def get_choices(word: str, dictionary: Dictionary) -> list[str]:
    candidates = list(dict.fromkeys(generate_candidates(word)))

    print(candidates)
    valid = [c for c in candidates if dictionary.lookup(c)]
    print(valid)

    if valid:
        return valid
    else:
        return candidates
