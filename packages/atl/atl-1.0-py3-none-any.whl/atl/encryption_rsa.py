'''
Example:
  if __name__ == "__main__":
    public_key_file = "./id_rsa.pub"  
    string_to_encrypt = "This is the string to encrypt"

    encrypted_string = encrypt_string(public_key_file, string_to_encrypt)
    print("Encrypted string:", encrypted_string)

    private_key_file = "./id_rsa"

    decrypted_string = decrypt_string(private_key_file, encrypted_string)
    print("Decrypted string:", decrypted_string)
'''

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def rsa_private_encrypt_string(public_key_file, string_to_encrypt):
  with open(public_key_file, "rb") as key_file:
    public_key = RSA.importKey(key_file.read())

  cipher = PKCS1_OAEP.new(public_key)
  encrypted_data = cipher.encrypt(string_to_encrypt.encode())
  encrypted_string = base64.b64encode(encrypted_data).decode()

  return encrypted_string

def rsa_public_decrypt_string(private_key_file, encrypted_string):
    with open(private_key_file, "rb") as key_file:
        private_key = RSA.importKey(key_file.read())

    cipher = PKCS1_OAEP.new(private_key)
    encrypted_data = base64.b64decode(encrypted_string)
    decrypted_data = cipher.decrypt(encrypted_data)
    decrypted_string = decrypted_data.decode()

    return decrypted_string
