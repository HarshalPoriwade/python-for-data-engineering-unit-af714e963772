import time

SENTENCES = [
    "Hello, World!",
    "Python is fun to learn.",
    "Practice makes perfect!",
]

PUNCTUATION = ".,!?;:'\"-"


def clean_text(text):
    """Lowercase the text, remove punctuation and return a list of words."""
    text = text.lower()
    for mark in PUNCTUATION:
        text = text.replace(mark, "")
    return text.split()


def count_correct(original, typed):
    """Count how many letters of the original sentence were typed correctly.

    Words are compared one by one, and letters inside a word are compared
    position by position. Case, punctuation and spaces are ignored.
    """
    original_words = clean_text(original)
    typed_words = clean_text(typed)
    correct = 0
    for i in range(min(len(original_words), len(typed_words))):
        original_word = original_words[i]
        typed_word = typed_words[i]
        if typed_word.startswith(original_word):
            correct = correct + len(original_word)
        else:
            for j in range(min(len(original_word), len(typed_word))):
                if original_word[j] == typed_word[j]:
                    correct = correct + 1
    return correct


def total_letters(sentence):
    """Count the letters that can be typed correctly in a sentence."""
    total = 0
    for word in clean_text(sentence):
        total = total + len(word)
    return total


def accuracy(original, typed):
    """Return the accuracy as a percentage, rounded to one decimal place."""
    total = total_letters(original)
    if total == 0:
        return 0.0
    return round(count_correct(original, typed) / total * 100, 1)


def check_attempt(sentence, typed, seconds):
    """Build the record dictionary for one attempt."""
    return {
        "sentence": sentence,
        "typed": typed,
        "accuracy": accuracy(sentence, typed),
        "time": round(seconds, 2),
    }


def average_accuracy(records):
    """Return the average accuracy of all records."""
    if len(records) == 0:
        return 0.0
    total = 0
    for record in records:
        total = total + record["accuracy"]
    return round(total / len(records), 1)


def run_tutor(sentences):
    """Ask the user to type each sentence and return the list of records."""
    records = []
    for sentence in sentences:
        print()
        print("Type this:", sentence)
        start = time.time()
        typed = input("> ")
        seconds = time.time() - start
        record = check_attempt(sentence, typed, seconds)
        records.append(record)
        print("Correct characters:", count_correct(sentence, typed),
              "of", total_letters(sentence))
        print("Accuracy:", str(record["accuracy"]) + "%")
        print("Time taken:", record["time"], "seconds")
    return records


def print_summary(records):
    """Print every attempt and the average accuracy."""
    print()
    print("=== Summary ===")
    for record in records:
        print(record["sentence"], "->", str(record["accuracy"]) + "%",
              "in", record["time"], "seconds")
    print("Average accuracy:", str(average_accuracy(records)) + "%")


if __name__ == "__main__":
    print("Typing Tutor - type each sentence and press Enter.")
    results = run_tutor(SENTENCES)
    print_summary(results)
    