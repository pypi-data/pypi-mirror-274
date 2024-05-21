import unittest
from atl.encryption_rsa import rsa_private_encrypt_string, rsa_public_decrypt_string

class TestRSAEncryption(unittest.TestCase):

    def setUp(self):
        self.public_key_file = './tests/tools/id_rsa.pub'
        self.private_key_file = './tests/tools/id_rsa'
        self.string_to_encrypt = "This is the string to encrypt"

    def test_rsa_encryption_decryption(self):
        # Encrypt the string
        encrypted_string = rsa_private_encrypt_string(self.public_key_file, self.string_to_encrypt)
        self.assertIsInstance(encrypted_string, str)

        # Decrypt the string
        decrypted_string = rsa_public_decrypt_string(self.private_key_file, encrypted_string)
        self.assertIsInstance(decrypted_string, str)
        self.assertEqual(decrypted_string, self.string_to_encrypt)

if __name__ == '__main__':
    unittest.main()