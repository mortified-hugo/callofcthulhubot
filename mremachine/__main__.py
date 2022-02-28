from mremachine.functions import enconding, decoding


action = input("ENCODE OR DECODE:")
if action == "ENCODE":
    word = enconding(input("Please type a word"),
                     input("Please type an all capital letter code"))
    print(f'Your encrypted word is {word}')
elif action == "DECODE":
    word = decoding(input("Please type a word"),
                    input("Please type an all capital letter code"))
    print(f'Your decrypted word is {word}')
else:
    print("INVALID INPUT")