![image](https://github.com/NermeenKamal/Security-System/assets/114883845/7c1ed27b-d96b-4921-8360-ad95347af59e)

---

# Security System

This project is a simple GUI-based application that demonstrates various classical and modern encryption techniques. It is built using Python's Tkinter library for the GUI and Cryptodome library for cryptographic functions.

## Features

The application supports the following encryption and decryption methods:

1. Ceaser Cipher
2. Monoalphabetic Cipher
3. Playfair Cipher (to be implemented)
4. Polyalphabetic Cipher (to be implemented)
5. Vigenère Cipher (to be implemented)
6. Rail Fence Cipher (to be implemented)
7. Row Transposition Cipher (to be implemented)
8. DES (Data Encryption Standard)
9. AES (Advanced Encryption Standard)

## Prerequisites

- Python 3.x
- Cryptodome library

You can install the Cryptodome library using pip:

```bash
pip install pycryptodome
```

## How to Run

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the Python script:

```bash
python sec.py
```

## GUI Layout

The GUI consists of the following elements:

- A title label at the top.
- A listbox to select the type of encryption/decryption.
- Entry fields to input plaintext and key.
- Buttons to perform encryption, decryption, and to exit the application.

## Code Explanation

### Encryption Function

The `Encryption` function handles the encryption process. It reads the selected encryption method, plaintext, and key from the user inputs, and performs the corresponding encryption.

### Decryption Function

The `Decryption` function handles the decryption process. It reads the selected decryption method, ciphertext (entered as plaintext in the input field), and key from the user inputs, and performs the corresponding decryption.

### Supported Ciphers

#### Ceaser Cipher

A simple substitution cipher where each letter in the plaintext is shifted by a fixed number of positions down the alphabet.

#### Monoalphabetic Cipher

A substitution cipher where each letter of the plaintext is mapped to a different letter.

#### DES (Data Encryption Standard)

A symmetric-key algorithm for the encryption of digital data. The key size is 8 bytes, and the block size is 8 bytes. 

#### AES (Advanced Encryption Standard)

A symmetric-key algorithm that can encrypt and decrypt data in blocks of 128 bits using cryptographic keys of 128, 192, and 256 bits.

## Example Usage

1. **Ceaser Cipher**
   - **Encryption**
     - Plaintext: `HELLO`
     - Key: `3`
     - Ciphertext: `KHOOR`
   - **Decryption**
     - Ciphertext: `KHOOR`
     - Key: `3`
     - Plaintext: `HELLO`

2. **Monoalphabetic Cipher**
   - **Encryption**
     - Plaintext: `hello`
     - Key: `qwertyuiopasdfghjklzxcvbnm`
     - Ciphertext: `itssg`
   - **Decryption**
     - Ciphertext: `itssg`
     - Key: `qwertyuiopasdfghjklzxcvbnm`
     - Plaintext: `hello`

3. **DES**
   - **Encryption**
     - Plaintext: `HELLODES`
     - Key: `mysecret`
     - Ciphertext: `<hexadecimal string>`
   - **Decryption**
     - Ciphertext: `<hexadecimal string>`
     - Key: `mysecret`
     - Plaintext: `HELLODES`

4. **AES**
   - **Encryption**
     - Plaintext: `HELLOAES`
     - Key: `mysecretkey123456`
     - Ciphertext: `<hexadecimal string>`
   - **Decryption**
     - Ciphertext: `<hexadecimal string>`
     - Key: `mysecretkey123456`
     - Plaintext: `HELLOAES`

## Future Work

- Implement Playfair, Polyalphabetic, Vigenère, Rail Fence, and Row Transposition ciphers.
- Improve error handling and input validation.
- Add support for more advanced cryptographic techniques.

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

---
