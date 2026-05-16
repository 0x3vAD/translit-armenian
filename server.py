from flask import Flask, request, jsonify, render_template
from candidates import get_choices
from translit import armenian_to_latin, restore_capitalization
from dictionary import load_dictionary

app = Flask(__name__)

print("Loading dictionary…")
dictionary = load_dictionary()
print(f"Dictionary ready.")

MAX_OPTIONS = 12


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "ready",
            "dict_size": 67000,
        }
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    data = request.json or {}
    text = data.get("text", "").strip()
    direction = data.get("direction", "lat2arm")

    if not text:
        return jsonify({"tokens": []})

    if direction == "arm2lat":
        return jsonify({"result": armenian_to_latin(text)})
    tokens = []

    import re

    parts = re.findall(r"\S+|\s+", text)

    for part in parts:
        if not part.strip():

            tokens.append({"kind": "fixed", "text": part})
            continue

        m = re.match(r"^(\W*)(.*?)(\W*)$", part, re.UNICODE)
        prefix = m.group(1) if m else ""
        word = m.group(2) if m else part
        suffix = m.group(3) if m else ""

        if not word:
            tokens.append({"kind": "fixed", "text": part})
            continue

        choices = get_choices(word.lower(), dictionary)

        if not choices:

            tokens.append({"kind": "fixed", "text": part})

        elif len(choices) == 1:

            converted = restore_capitalization(word, choices[0])
            tokens.append({"kind": "fixed", "text": prefix + converted + suffix})

        else:

            styled = [restore_capitalization(word, c) for c in choices]
            in_dict = True
            shown = styled[:MAX_OPTIONS]
            truncated = len(styled) > MAX_OPTIONS

            tokens.append(
                {
                    "kind": "choice",
                    "prefix": prefix,
                    "suffix": suffix,
                    "options": styled,
                    "in_dict": in_dict,
                    "original": word,
                    "truncated": False,
                }
            )

    return jsonify({"tokens": tokens})


if __name__ == "__main__":
    app.run(debug=True)
