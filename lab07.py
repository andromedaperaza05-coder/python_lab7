ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
encrypted_texts = []


def vigenere_sq(alphabet=ALPHABET):
    square = [
        [alphabet[(row + column) % len(alphabet)] for column in range(len(alphabet))]
        for row in range(len(alphabet))
    ]
    cell_width = max(1, len(max(alphabet, key=len)))
    print("    " + " ".join(f"{letter:>{cell_width}}" for letter in alphabet))
    print("   -" + "---" * len(alphabet))
    for row_letter, row in zip(alphabet, square):
        print(f"{row_letter:>2} | " + " ".join(f"{letter:>{cell_width}}" for letter in row))
    return square


def letter_to_index(letter, alphabet):
    return alphabet.index(letter)


def index_to_letter(index, alphabet):
    return alphabet[index % len(alphabet)]


def vigenere_index(key_letter, plaintext_letter, alphabet):
    key_index = letter_to_index(key_letter, alphabet)
    plaintext_index = letter_to_index(plaintext_letter, alphabet)
    return index_to_letter(key_index + plaintext_index, alphabet)


def undo_vigenere_index(key_letter, cipher_letter, alphabet):
    key_index = letter_to_index(key_letter, alphabet)
    cipher_index = letter_to_index(cipher_letter, alphabet)
    return index_to_letter(cipher_index - key_index, alphabet)


def _transform(key, text, alphabet, transform_letter):
    if not key:
        raise ValueError("The key must not be empty.")
    if not alphabet:
        raise ValueError("The alphabet must not be empty.")

    key = key.upper()
    text = text.upper()
    if any(letter not in alphabet for letter in key):
        raise ValueError("Every key character must be in the alphabet.")

    result = []
    key_position = 0
    for letter in text:
        if letter in alphabet:
            key_letter = key[key_position % len(key)]
            result.append(transform_letter(key_letter, letter, alphabet))
            key_position += 1
        else:
            # Keep spaces and punctuation, without advancing the key.
            result.append(letter)
    return "".join(result)


def encrypt_vigenere(key, plaintext, alphabet=ALPHABET):
    return _transform(key, plaintext, alphabet, vigenere_index)


def decrypt_vigenere(key, cipher_text, alphabet=ALPHABET):
    return _transform(key, cipher_text, alphabet, undo_vigenere_index)


def encrypt_action():
    plaintext = input("Plain text: ")
    key = input("Key: ").strip()
    cipher_text = encrypt_vigenere(key, plaintext, ALPHABET)
    encrypted_texts.append((key, cipher_text))
    print(f"Encrypted: {cipher_text}")


def decrypt_action():
    if not encrypted_texts:
        print("There is no encrypted text to decrypt.")
        return
    for key, cipher_text in encrypted_texts:
        print(f"Decrypted: {decrypt_vigenere(key, cipher_text, ALPHABET)}")


def dump_action():
    print(encrypted_texts)


def quit_action():
    print("Goodbye!")


def run_app():
    menu = [
        ["1. Encrypt", encrypt_action],
        ["2. Decrypt", decrypt_action],
        ["3. Dump Encrypted Text", dump_action],
        ["4. Quit", quit_action],
    ]
    while True:
        print("\nVigenere Cipher")
        for label, _ in menu:
            print(label)
        choice = input("Choose an option: ").strip()
        selected = next((item for item in menu if item[0].startswith(choice + ".")), None)
        if selected is None:
            print("Please choose 1, 2, 3, or 4.")
            continue
        selected[1]()
        if selected[1] is quit_action:
            break


if __name__ == "__main__":
    run_app()