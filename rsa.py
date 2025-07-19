class RSA:
    def __init__(self, publicKey=None, privateKey=None):
        # default values if none provided
        if publicKey is None:
            publicKey = { "e": 3, "n": 15 }
        if privateKey is None:
            privateKey = { "d": 3, "n": 15 }
        
        self.publicKey = publicKey
        self.privateKey = privateKey

    def mod_pow(self, base, exponent, modulus):
        result = 1
        b = base % modulus
        e = exponent
        while e > 0:
            if e % 2 == 1:
                result = (result * b) % modulus
            b = (b * b) % modulus
            e //= 2
        return result

    def encrypt(self, hex_string):
        digits = list(hex_string)
        result = []
        for digit in digits:
            m = int(digit, 16)
            if m >= self.publicKey["n"]:
                raise ValueError(
                    f"Digit {digit} too large for modulus {self.publicKey['n']}"
                )
            c = self.mod_pow(m, self.publicKey["e"], self.publicKey["n"])
            result.append(c)
        return result

    def decrypt(self, cipher_chunks):
        plaintext = ""
        for c in cipher_chunks:
            m = self.mod_pow(c, self.privateKey["d"], self.privateKey["n"])
            plaintext += hex(m)[2:]
        return plaintext


if __name__ == "__main__":
    rsa = RSA()

    # Example: encrypt hex digit "a" (which is 10 decimal)
    ciphertext_chunks = rsa.encrypt("a")
    print("Ciphertext chunks:", ciphertext_chunks)

    plaintext_hex = rsa.decrypt(ciphertext_chunks)
    print("Decrypted hex:", plaintext_hex)
