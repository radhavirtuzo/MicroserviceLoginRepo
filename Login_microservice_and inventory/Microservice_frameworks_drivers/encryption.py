import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
class Encryption:
    @staticmethod
    def decrypt(cipher_text: str) -> str:
        encryption_key = "CIRCUMFRANCES6546753"
        cipher_text = cipher_text.replace(" ", "+")
        cipher_bytes = base64.b64decode(cipher_text)
        
        backend = default_backend()
        salt = bytes([0x49, 0x76, 0x61, 0x6e, 0x20, 0x4d, 0x65, 0x64, 0x76, 0x65, 0x64, 0x65, 0x76])
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=48,   
            salt=salt,
            iterations=100000,
            backend=backend
        )
        key_iv = kdf.derive(encryption_key.encode())
        key = key_iv[:32]   
        iv = key_iv[32:]    

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(cipher_bytes) + decryptor.finalize()
       
        padding_len = decrypted_padded[-1]
        decrypted_bytes = decrypted_padded[:-padding_len]

        return decrypted_bytes.decode('utf-16le')

    @staticmethod
    def encrypt(clear_text: str) -> str:
        encryption_key = "CIRCUMFRANCES6546753"
        clear_bytes = clear_text.encode('utf-16le')
        
        backend = default_backend()
        salt = bytes([0x49, 0x76, 0x61, 0x6e, 0x20, 0x4d, 0x65, 0x64, 0x76, 0x65, 0x64, 0x65, 0x76])
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=48,   
            salt=salt,
            iterations=100000,
            backend=backend
        )
        key_iv = kdf.derive(encryption_key.encode())
        key = key_iv[:32]  
        iv = key_iv[32:]   

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
    
        padding_len = 16 - (len(clear_bytes) % 16)
        padded_clear_bytes = clear_bytes + bytes([padding_len]) * padding_len
        
        encrypted_padded = encryptor.update(padded_clear_bytes) + encryptor.finalize()
        return base64.b64encode(encrypted_padded).decode('utf-8')
if __name__ == "__main__":
    text = input("Enter the text to encrypt: ")
    encrypted = Encryption.encrypt(text)
    print(f"Encrypted: {encrypted}")