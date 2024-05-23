import base64

class dataEncryptor:
    def __init__(self, key_manager):
        self.key_manager = key_manager

    def encrypt(self, source, file_or_string):
        import os
        key = self.key_manager.key
        if isinstance(source, str):
            data = source.encode()
        elif isinstance(source, os.__file__):
            with open(source, 'rb') as f:
                data = f.read()
        else:
            raise ValueError("Invalid source type. Must be a file or string.")

        encrypted_data = self._xor_encrypt(data, key)
        if file_or_string == 'file':
            encrypted_file = source + '.enc'
            with open(encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            return encrypted_file
        elif file_or_string == 'string':
            return base64.b64encode(encrypted_data).decode()
        else:
            raise ValueError("Invalid file_or_string value. Must be 'file' or 'string'.")

    def decrypt(self, source, file_or_string):
        key = self.key_manager.key
        if file_or_string == 'file':
            decrypted_file = source[:-4]  # Remove the '.enc' extension
            with open(source, 'rb') as f:
                encrypted_data = f.read()
        elif file_or_string == 'string':
            encrypted_data = base64.b64decode(source.encode())
        else:
            raise ValueError("Invalid file_or_string value. Must be 'file' or 'string'.")

        decrypted_data = self._xor_encrypt(encrypted_data, key)
        if file_or_string == 'file':
            with open(decrypted_file, 'wb') as f:
                f.write(decrypted_data)
            return decrypted_file
        elif file_or_string == 'string':
            return decrypted_data.decode()
        else:
            raise ValueError("Invalid file_or_string value. Must be 'file' or 'string'.")

    def _xor_encrypt(self, data, key):
        encrypted_data = bytearray()
        key_length = len(key)
        for i, byte in enumerate(data):
            encrypted_data.append(byte ^ key[i % key_length])
        return encrypted_data