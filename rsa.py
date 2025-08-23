class RSA:
    def __init__(self, publicKey, privateKey):  
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

    def decrypt(self, cipher_chunks):
        plaintext = ""
        for c in cipher_chunks:
            m = self.mod_pow(c, self.privateKey["d"], self.privateKey["n"])
            plaintext += f"{m:x}"
        return plaintext

