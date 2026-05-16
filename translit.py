from mapping import LATIN_TO_ARMENIAN, ARMENIAN_TO_LATIN


def armenian_to_latin(text: str) -> str:
    result = []
    for char in text:
        result.append(ARMENIAN_TO_LATIN.get(char, char))
    return "".join(result)


def latin_to_armenian_simple(word: str) -> str:
    result, i = [], 0
    while i < len(word):
        matched = False
        for lat, arm in LATIN_TO_ARMENIAN:
            if word[i:].startswith(lat):
                result.append(arm)
                i += len(lat)
                matched = True
                break
        if not matched:
            result.append(word[i])
            i += 1
    return "".join(result)
