from mremachine.alphabet import numbered_alphabet, stable_alphabet


def enconding(word, key):
    word = word.upper()
    key = key.upper()
    end_code = []
    n = 0

    for letter in word:
        code = numbered_alphabet[letter] + numbered_alphabet[key[n]] - 1
        if code > 26:
            code = code - 26
        end_code.append(code)
        n += 1
        if n > len(key) - 1:
            n = 0
    new_word = ""

    for number in end_code:
        new_word += stable_alphabet[number]
    return new_word

def decoding(word, key):
    word = word.upper()
    key = key.upper()
    end_code = []
    n = 0

    for letter in word:
        code = numbered_alphabet[letter] - numbered_alphabet[key[n]] + 1
        if code < 1:
            code = code + 26
        end_code.append(code)
        n += 1
        if n > len(key) - 1:
            n = 0
    old_word = ""

    for number in end_code:
        old_word += stable_alphabet[number]
    return old_word
