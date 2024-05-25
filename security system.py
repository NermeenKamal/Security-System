import os
from tkinter import *
from tkinter import messagebox

import hashlib

import numpy as np
from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad

from Cryptodome.Cipher import AES



def Encryption():
    selected_indices = options.curselection()
    if not selected_indices:
        messagebox.showinfo("Error", "No option selected!")
        return
    option = [options.get(i) for i in selected_indices]

    plaintext = plaintxt.get()
    if not plaintext:
        messagebox.showinfo("Error", "EMPTY PlainText!")
        return
    key = keytxt.get()
    if not key:
        messagebox.showinfo("Error", "EMPTY KEY!")
        return


    if option[0] == 'Ceaser':
        key = int(keytxt.get())
        plaintext = plaintxt.get()

        ciphertext = ''
        for char in plaintext:
            if char.isalpha():
                if char.islower():
                    ciphertext += chr((ord(char) - 97 + key) % 26 + 97)
                else:
                    ciphertext += chr((ord(char) - 65 + key) % 26 + 65)
            else:
                ciphertext += char

        messagebox.showinfo(title="Ceaser_Encryption", message=f"Ciphertext: {ciphertext}")

    elif option[0] == 'Monoalphabetic':
        import string
        alphabets = string.ascii_lowercase
        key_map = dict(zip(alphabets, key.lower()))
        ciphertext = ''.join(key_map.get(char, char) for char in plaintext.lower())
        messagebox.showinfo(title="Monoalphabetic_Encryption", message=f"Ciphertext: {ciphertext}")

    elif option[0] == 'Playfair':
        def prepare_key(key):
            key = key.lower().replace("j", "i")  # Convert to lowercase and replace 'j' with 'i'
            key = ''.join(filter(str.isalpha, key))  # Remove non-alphabetic characters
            return key

        def generate_key_square(key):
            alphabet = "abcdefghiklmnopqrstuvwxyz"  # Exclude 'j' (used 'i' instead)
            key = prepare_key(key)
            key = ''.join(dict.fromkeys(key))  # Remove duplicate characters
            key += alphabet
            key_square = np.array(list(key)).reshape(5, 5)
            return key_square

        def find_letter_positions(letter, key_square):
            indices = np.where(key_square == letter)
            return indices[0][0], indices[1][0]

        def split_text(text):
            pairs = []
            for i in range(0, len(text), 2):
                if i == len(text) - 1:  # If the last pair has only one character, add 'x' to make it a pair
                    pairs.append(text[i] + 'x')
                elif text[i] == text[i + 1]:  # If the two characters in a pair are the same, add 'x' between them
                    pairs.append(text[i] + 'x')
                else:
                    pairs.append(text[i:i + 2])
            return pairs

        key_square = generate_key_square(key)
        prepared_text = prepare_key(plaintext)
        if len(prepared_text) % 2 != 0:
            prepared_text += 'x'  # Add an extra 'x' if the text length is odd

        encrypted_text = ""
        for pair in split_text(prepared_text):
            row1, col1 = find_letter_positions(pair[0], key_square)
            row2, col2 = find_letter_positions(pair[1], key_square)
            if row1 == row2:  # Same row
                encrypted_text += key_square[row1, (col1 + 1) % 5] + key_square[row2, (col2 + 1) % 5]
            elif col1 == col2:  # Same column
                encrypted_text += key_square[(row1 + 1) % 5, col1] + key_square[(row2 + 1) % 5, col2]
            else:  # Different rows and columns
                encrypted_text += key_square[row1, col2] + key_square[row2, col1]
        messagebox.showinfo(title="Playfair_Encryption", message="cipher Text  "+encrypted_text)

    elif option[0] == 'Polyalphabetic':
            shifts = []
            for i in range(3):
                shift = int(input(f"Enter the shift for letter {i+1}: "))
                shifts.append(shift)
            encrypted_text = ""
            for i in range(0, len(plaintext), 3):
                slice_text = plaintext[i:i+3]
                if len(slice_text) < 3:
                    slice_text += ' ' * (3 - len(slice_text))  # Padding with spaces if the slice is less than 3 characters
                for j in range(3):
                    shift = shifts[j]
                    encrypted_char = chr((ord(slice_text[j]) - ord('a') + shift) % 26 + ord('a'))
                    encrypted_text += encrypted_char
            messagebox.showinfo(title="Polyalphabetic_Encryption", message="Cipher text  "+encrypted_text)

    elif option[0] == 'Vigenère':
            encrypted_text = ""
            key_length = len(key)
            for i, char in enumerate(plaintext):
                if char.isalpha():
                    key_char = key[i % key_length]
                    shift = ord(key_char.lower()) - ord('a')
                    if char.isupper():
                        encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                    else:
                        encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                    encrypted_text += encrypted_char
                else:
                    encrypted_text += char
            messagebox.showinfo(title="Vigenère_Encryption", message="Cipher text  "+encrypted_text)

    elif option[0] == 'Rail_Fence':
        rails = int(keytxt.get())
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1

        for char in plaintext:
            fence[rail].append(char)
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction *= -1
        encrypted_text = ''.join([''.join(rail) for rail in fence])

        messagebox.showinfo(title="Rail_Fence_Encryption", message="Cipher text  " + encrypted_text)

    elif option[0] == 'Row_Transposition':
        key_order = sorted(range(1, len(key) + 1), key=lambda k: key[k - 1])
        num_columns = len(key)
        num_rows = -(-len(plaintext) // num_columns)
        matrix = [['' for _ in range(num_columns)] for _ in range(num_rows)]

        for i, char in enumerate(plaintext):
            matrix[i // num_columns][i % num_columns] = char

        encrypted_text = ''
        for row in matrix:
            for col in key_order:
                encrypted_text += row[col - 1]
        messagebox.showinfo(title="Row_Transposition_Encryption", message="Cipher text  "+encrypted_text)

    elif option[0] == 'DES':
        key = key.encode().ljust(8, b'\0')[:8]
        cipher = DES.new(key, DES.MODE_CBC)
        padded_text = pad(plaintext.encode(), DES.block_size)
        ciphertext = cipher.encrypt(padded_text)
        messagebox.showinfo(title="DES_Encryption", message=f"Ciphertext: {ciphertext.hex()}\nIV: {cipher.iv.hex()}")

    elif option[0] == 'AES':
        key = key.encode('utf-8')  # Convert to bytes
        key = hashlib.sha256(key).digest()  # Generate a 32-byte key using SHA-256

        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        ciphertext_hex = ciphertext.hex()
        iv_hex = cipher.iv.hex()
        messagebox.showinfo(title="AES_Encryption", message="Cipher text: " + ciphertext_hex + "\nInitialization Vector: " + iv_hex)

    else:
        print("INVALID VALUE!")
        return


def Decryption():
    selected_indices = options.curselection()
    if not selected_indices:
        messagebox.showinfo("Error", "No option selected!")
        return
    option = [options.get(i) for i in selected_indices]

    plaintext = plaintxt.get()
    if not plaintext:
        messagebox.showinfo("Error", "EMPTY PlainText!")
        return
    key = keytxt.get()
    if not key:
        messagebox.showinfo("Error", "EMPTY KEY!")
        return


    if option[0] == 'Ceaser':
        key = int(keytxt.get())
        ciphertext = plaintxt.get()

        plaintext = ''
        for char in ciphertext:
            if char.isalpha():
                if char.islower():
                    plaintext += chr((ord(char) - 97 - key) % 26 + 97)
                else:
                    plaintext += chr((ord(char) - 65 - key) % 26 + 65)
            else:
                plaintext += char
        messagebox.showinfo(title="Ceaser_Decryption", message=f"Decrypted Text: {plaintext}")

    elif option[0] == 'Monoalphabetic':
        import string
        alphabets = string.ascii_lowercase
        key_map = dict(zip(key.lower(), alphabets))
        plaintext = ''.join(key_map.get(char, char) for char in plaintext.lower())
        messagebox.showinfo(title="Monoalphabetic_Decryption", message=f"Plaintext: {plaintext}")


    elif option[0] == 'Playfair':
        def prepare_key(key):
            key = key.lower().replace("j", "i")  # Convert to lowercase and replace 'j' with 'i'
            key = ''.join(filter(str.isalpha, key))  # Remove non-alphabetic characters
            key = ''.join(dict.fromkeys(key))  # Remove duplicate characters
            return key

        def generate_key_square(key):
            alphabet = "abcdefghiklmnopqrstuvwxyz"  # Exclude 'j' (used 'i' instead)
            key = prepare_key(key)
            key += alphabet
            key_square = np.array(list(key)).reshape(5, 5)
            return key_square

        def find_letter_positions(letter, key_square):
            indices = np.where(key_square == letter)
            return indices[0][0], indices[1][0]

        def split_text(text):
            pairs = []
            text += 'x' if len(text) % 2 != 0 else ''  # Pad with 'x' if text length is odd
            for i in range(0, len(text), 2):
                pairs.append(text[i:i + 2])
            return pairs

        key_square = generate_key_square(key)
        decrypted_text = ""
        for pair in split_text(plaintext):
            row1, col1 = find_letter_positions(pair[0], key_square)
            row2, col2 = find_letter_positions(pair[1], key_square)
            if row1 == row2:  # Same row
                decrypted_text += key_square[row1, (col1 - 1) % 5] + key_square[row2, (col2 - 1) % 5]
            elif col1 == col2:  # Same column
                decrypted_text += key_square[(row1 - 1) % 5, col1] + key_square[(row2 - 1) % 5, col2]
            else:  # Different rows and columns
                decrypted_text += key_square[row1, col2] + key_square[row2, col1]

        messagebox.showinfo(title="Playfair_Decryption", message="Cipher Text  " + decrypted_text)

    elif option[0] == 'Polyalphabetic':
            shifts = []
            for i in range(3):
                shift = int(input(f"Enter the shift for letter {i + 1}: "))
                shifts.append(shift)

            plaintext_length = len(plaintext)
            if plaintext_length % 3 != 0:
                padding_length = 3 - (plaintext_length % 3)
                plaintext += ' ' * padding_length

            decrypted_text = ""
            for i in range(0, len(plaintext), 3):
                slice_text = plaintext[i:i + 3]
                for j in range(3):
                    shift = shifts[j]
                    char = slice_text[j]
                    if char.islower():
                        decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                    elif char.isupper():
                        decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                    else:
                        decrypted_char = char
                    decrypted_text += decrypted_char
            messagebox.showinfo(title="Polyalphabetic_Decryption", message="PlainText  " + decrypted_text)

    elif option[0] == 'Vigenère':
        decrypted_text = ""
        key_length = len(key)
        for i, char in enumerate(plaintext):
            if char.isalpha():
                key_char = key[i % key_length]
                shift = ord(key_char.lower()) - ord('a')
                if char.isupper():
                    decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                else:
                    decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                decrypted_text += decrypted_char
            else:
                decrypted_text += char
        messagebox.showinfo(title="Vigenère_Decryption", message="PlainText  "+decrypted_text)

    elif option[0] == 'Rail_Fence':
        rails = int(keytxt.get())
        fence = [['' for _ in range(len(plaintext))] for _ in range(rails)]
        rail = 0
        direction = 1

        for i in range(len(plaintext)):
            fence[rail][i] = '*'
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction *= -1

        index = 0
        for i in range(rails):
            for j in range(len(plaintext)):
                if fence[i][j] == '*':
                    fence[i][j] = plaintext[index]
                    index += 1

        rail = 0
        direction = 1
        decrypted_text = ''
        for _ in range(len(plaintext)):
            decrypted_text += fence[rail][_]
            rail += direction
            if rail == rails - 1 or rail == 0:
                direction *= -1
        messagebox.showinfo(title="Rail_Fence_Decryption", message="PlainText  " + decrypted_text)

    elif option[0] == 'Row_Transposition':
        key_order = sorted(range(1, len(key) + 1), key=lambda k: key[k - 1])
        num_columns = len(key)
        num_rows = -(-len(plaintext) // num_columns)
        matrix = [['' for _ in range(num_columns)] for _ in range(num_rows)]

        index = 0
        for col in key_order:
            for row in range(num_rows):
                if index < len(plaintext):
                    matrix[row][col - 1] = plaintext[index]
                    index += 1

        decrypted_text = ''
        for i in range(num_rows):
            for j in range(num_columns):
                decrypted_text += matrix[i][j]
        messagebox.showinfo(title="Row_Transposition_Decryption", message="PlainText  "+decrypted_text)

    elif option[0] == 'DES':
        key = key.encode().ljust(8, b'\0')[:8]
        iv = os.urandom(8)  # Generate a new random IV
        cipher = DES.new(key, DES.MODE_CBC, iv)

        # Pad the plaintext to a multiple of the block size
        padded_text = pad(plaintext.encode(), DES.block_size)

        ciphertext = cipher.encrypt(padded_text)
        messagebox.showinfo(title="DES_Encryption", message=f"Ciphertext: {ciphertext.hex()}\nIV: {iv.hex()}")

    elif option[0] == 'AES':
        key = key.encode('utf-8')  # Convert to bytes
        key = hashlib.sha256(key).digest()  # Generate a 32-byte key using SHA-256
        iv = os.urandom(16)  # Generate a new random IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # Pad the plaintext to a multiple of the block size
        padded_text = pad(plaintext.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_text)
        messagebox.showinfo(title="AES_Encryption", message=f"Ciphertext: {ciphertext.hex()}\nInitialization Vector: {iv.hex()}")

    else:
        print("INVALID VALUE!")
        return


frame = Tk()
frame.title("Security System")
frame.geometry("700x600")
frame.resizable(False, False)
frame.configure(background="grey")

label = Label(frame, text="Security System", fg="black", font=("Arial", 30, "bold"), pady=10, bg="grey")
label.place(x=180, y=10)


options = Listbox(frame, height=20, width=80, font=("Arial", 10, "bold"), bg="black", fg="white")
options.place(x=70, y=80)
options.insert(1, "Ceaser")
options.insert(2, "Monoalphabetic")
options.insert(3, "Playfair")
options.insert(4, "Polyalphabetic")
options.insert(5, "Vigenère")
options.insert(6, "Rail_Fence")
options.insert(7, "Row_Transposition")
options.insert(8, "DES")
options.insert(9, "AES")

plain = Label(frame, text="PlainText", fg="black", font=("Arial", 10, "bold"), pady=10, bg="grey")
plain.place(x=110, y=440)
plaintxt = Entry(frame)
plaintxt.place(x=180, y=450)

key = Label(frame, text="KEY", fg="black", font=("Arial", 10, "bold"), pady=10, bg="grey")
key.place(x=350, y=440)
keytxt = Entry(frame)
keytxt.place(x=385, y=450)


button1 = Button(frame, text="Decryption", fg="white", bg="red", font=("Arial", 10, "bold"), command=Decryption)
button2 = Button(frame, text="Encryption", fg="white", bg="green", font=("Arial", 10, "bold"), command=Encryption)
button3 = Button(frame, text="Exit", fg="white", bg="black", font=("Arial", 10, "bold"), command=frame.quit)

button3.place(x=300, y=550)
button3.configure(padx=20)
button2.place(x=230, y=500)
button1.place(x=360, y=500)

frame.mainloop()