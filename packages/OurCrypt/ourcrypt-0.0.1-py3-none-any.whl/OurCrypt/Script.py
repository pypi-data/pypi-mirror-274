import os
from tkinter import Tk, filedialog
from tkinter.filedialog import askopenfilename

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_file(file_path: str, password: str):
    salt = os.urandom(16)
    key = generate_key(password, salt)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as f:
        file_data = f.read()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(file_data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    file_name, file_extension = os.path.splitext(file_path)
    encrypted_file_path = f"{file_name}_enc{file_extension}"

    with open(encrypted_file_path, 'wb') as f:
        f.write(salt + iv + encrypted_data)

    print(f"File encrypted and saved as {encrypted_file_path}")


def decrypt_file(encrypted_file_path: str, password: str):
    with open(encrypted_file_path, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        encrypted_data = f.read()

    key = generate_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    file_name, file_extension = os.path.splitext(encrypted_file_path)
    decrypted_file_path = f"{file_name}_dec{file_extension}"

    with open(decrypted_file_path, 'wb') as f:
        f.write(decrypted_data)

    print(f"File decrypted and saved as {decrypted_file_path}")


def select_file() -> str:
    root = Tk()
    root.withdraw()  # Скрыть главное окно
    file_path = filedialog.askopenfilename()
    return file_path

#def main():
 #   password = "your_password"

    # if input("Input number \"1\" for enc: ") == "1":
    #     print("Select a file to encrypt:")
    #     file_path = select_file()
    #     if file_path:
    #         encrypt_file(file_path, password)
    # if input("Input number \"2\" for dec: ") == "2":
    #     print("Select a file to decrypt:")
    #     encrypted_file_path = select_file()
    #     if encrypted_file_path:
    #         decrypt_file(encrypted_file_path, password)

