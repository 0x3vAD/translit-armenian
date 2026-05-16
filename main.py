import inquirer
from translit import armenian_to_latin
from candidates import get_choices
from dictionary import load_dictionary

dictionary = load_dictionary()


def convert_sentence(text: str) -> str:
    words = text.split()
    output = []

    for word in words:
        prefix = ""
        suffix = ""
        clean = word
        if clean and not clean[-1].isalpha():
            suffix = clean[-1]
            clean = clean[:-1]
        choices = get_choices(clean.lower(), dictionary)

        if len(choices) == 0:
            output.append(word)

        elif len(choices) == 1:
            output.append(prefix + choices[0] + suffix)

        else:
            answer = inquirer.prompt(
                [
                    inquirer.List(
                        "choice",
                        message=f"Multiple options for '{clean}' — pick one",
                        choices=choices + [f"[keep as '{clean}']"],
                    )
                ]
            )
            chosen = answer["choice"]
            if chosen.startswith("[keep"):
                output.append(word)
            else:
                output.append(prefix + chosen + suffix)

    return " ".join(output)


mode = input(
    "Mode?\n  1) Latin translit → Armenian\n  2) Armenian → Latin\nChoice: "
).strip()
text = input("Enter text: ").strip()

if mode == "1":
    print("\nResult:", convert_sentence(text))
elif mode == "2":
    print("\nResult:", armenian_to_latin(text))
