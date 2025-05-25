import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from src.utils import save_file, load_file, generate_key_file


def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt_text(input_file):
    try:
        with open(input_file, 'r') as f:
            text = f.read()

        private_key, public_key = generate_rsa_keys()
        rsa_key = RSA.import_key(public_key)

        
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        aes_key = os.urandom(16)

        
        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher_aes.encrypt_and_digest(text.encode('utf-8'))

        
        encrypted_data = (
            cipher_rsa.encrypt(aes_key).hex() + "\n" +
            cipher_aes.nonce.hex() + "\n" +
            tag.hex() + "\n" +
            ciphertext.hex()
        )

        encrypted_file = "encrypted_data/text_encrypted.txt"
        os.makedirs(os.path.dirname(encrypted_file), exist_ok=True)
        with open(encrypted_file, 'w') as f:
            f.write(encrypted_data)

        
        private_key_path = generate_key_file("text")
        save_file(private_key, private_key_path)

        return encrypted_file, private_key_path

    except Exception as e:
        raise RuntimeError(f"Error during encryption: {e}")


def decrypt_text(encrypted_file, private_key_file):
    try:
        with open(encrypted_file, 'r') as f:
            encrypted_data = f.read().splitlines()

        
        encrypted_aes_key = bytes.fromhex(encrypted_data[0])
        nonce = bytes.fromhex(encrypted_data[1])
        tag = bytes.fromhex(encrypted_data[2])
        ciphertext = bytes.fromhex(encrypted_data[3])

        
        private_key = load_file(private_key_file)
        rsa_key = RSA.import_key(private_key)

        
        cipher_rsa = PKCS1_OAEP.new(rsa_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)

        
        cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)
        original_text = cipher_aes.decrypt_and_verify(ciphertext, tag).decode('utf-8')

        return original_text

    except Exception as e:
        raise RuntimeError(f"Error during decryption: {e}")