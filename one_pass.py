import os
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import cryptography

def calculate_salt_positions(file_name, salt_length):
    hash_object = hashlib.sha256(file_name.encode())
    hex_dig = hash_object.hexdigest()
    ascii_sum = sum(ord(char) for char in str(hex_dig))
    start_position = int(str(ascii_sum)[0])
    if start_position <= 1 or start_position >= 6:
        start_position = 3
    return start_position

def calculate_iterations(file_name):
    hash_object = hashlib.sha256(file_name.encode())
    hex_dig = hash_object.hexdigest()
    ascii_sum = sum(ord(char) for char in str(hex_dig))
    file_name_length = len(file_name)
    i = ascii_sum
    while i < 10000000:
        i = i ** file_name_length
    iterations = int(str(i)[:7]) + ascii_sum - file_name_length
    return iterations

def generate_fernet_key(password, salt, file):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=calculate_iterations(file),
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

#########################################################33
def encrypt_file(source_file, encrypted_file, password):
    try:
        # יצירת מלח
        salt = os.urandom(32)

        # יצירת מפתח מהסיסמה והמלח
        key = generate_fernet_key(password, salt,encrypted_file)
        fernet = Fernet(key)

        # קריאת הנתונים מהקובץ המקורי
        with open(source_file, 'rb') as file:
            file_data = file.read()

        # הצפנת הנתונים
        encrypted_data = fernet.encrypt(file_data)
        
        key = generate_fernet_key(password, password,encrypted_file)
        fernet = Fernet(key)
        # הוספת המלח לתחילת ולסוף הנתונים המוצפנים
        encrypted_data_with_salt = fernet.encrypt(salt + encrypted_data + os.urandom(32))
        
        with open(encrypted_file, 'wb') as file:
            file.write(base64.b64encode(encrypted_data_with_salt))                                          
    except Exception as e:
        print(e)
        if os.path.exists(encrypted_file):os.remove(encrypted_file)
            


def decrypt_file(encrypted_file, decrypted_file, password):
    with open(encrypted_file, 'rb') as file:
        encrypted_data_with_salt = file.read()
    encrypted_data_with_salt=base64.b64decode(encrypted_data_with_salt)
    key = generate_fernet_key(password, password,encrypted_file)
    fernet = Fernet(key)
    encrypted_data_with_salt=fernet.decrypt(encrypted_data_with_salt)
    # חילוץ המלח מהנתונים המוצפנים (32 הבייטים הראשונים)
    salt = encrypted_data_with_salt[:32]
    # יצירת מפתח מהסיסמה והמלח
    key = generate_fernet_key(password, salt,encrypted_file)
    fernet = Fernet(key)

    # הורדת המלח מהתחלה וסוף הנתונים המוצפנים
    encrypted_data = encrypted_data_with_salt[32:-32]

    # פענוח הנתונים
    decrypted_data = fernet.decrypt(encrypted_data)

    # שמירת הנתונים המפוענחים בקובץ
    with open(decrypted_file, 'wb') as file:
        file.write(decrypted_data)


def add_to_gitignore(filename):
    gitignore_exists = os.path.exists('.gitignore')
    
    if gitignore_exists:
        with open('.gitignore', 'r+') as file:
            lines = file.readlines()
            if '\n' not in lines[-1]:
                file.write('\n')
            if filename + '\n' not in lines:
                file.write(filename + '\n')
    else:
        with open('.gitignore', 'w') as file:
            file.write(filename + '\n')

def read_credentials(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            password = lines[0].strip()
            if password == 'your_default_password':
                print(f"{file_name} edit it with pass\n and add encrypted file")
                exit(1)
            encrypted_file_name = lines[1].strip()
            return password, encrypted_file_name
    else:
        default_password = 'your_default_password'
        default_encrypted_file_name = 'your_default_encrypted_file_name'
        with open(file_name, 'w') as file:
            file.write(default_password + '\n')
            file.write(default_encrypted_file_name + '\n')
        print(f"{file_name} edit it with pass\n and add encrypted file")
        exit()


def get_type_of_input(input_str):
    try:
        # Try to convert the input to int
        value = int(input_str)
        return value
    except ValueError:
        try:
            # Try to convert the input to float
            value = float(input_str)
            return value
        except ValueError:
            if input_str.startswith("[") and input_str.endswith("]"):
                try:
                    # Try to parse the input as a list
                    value = eval(input_str)
                    if isinstance(value, list):
                        return value
                except:
                    pass

            # Check if the string is enclosed in quotes
            if len(input_str) > 2 and input_str[0] == input_str[-1] and input_str[0] in "\"'":
                return input_str[1:-1]
            return input_str  # Return the string as is if not enclosed in quotes


def env():
    config_file_name = '.p.p'
    decrypted_file_name = "secrets.txt"
    add_to_gitignore(config_file_name)
    add_to_gitignore(decrypted_file_name)

    password, encrypted_file_name = read_credentials(config_file_name)
    password = password.encode()

    if not os.path.exists(encrypted_file_name):
        print("\n", encrypted_file_name, "=> not exists")
        if not os.path.exists(decrypted_file_name):
            with open(decrypted_file_name, 'w') as f:
                f.write('SECRET_NAME1=SECRET\nSECRET_NAME2=SECRET2')
                print("\n", decrypted_file_name, '=> ENTER THE SECRET TO FILE FOR CRYPTE IT\n')
                exit(1)
        else:
            with open(decrypted_file_name, 'r') as file:
                if 'SECRET_NAME1=SECRET\nSECRET_NAME2=SECRET2' not in file.read():
                    print("\nclose: please wait .. now encrypt", decrypted_file_name, "to be", encrypted_file_name, "\n")
                    encrypt_file(decrypted_file_name, encrypted_file_name, password)
                else:
                    print("\n", decrypted_file_name, '=> ENTER THE SECRET TO FILE FOR CRYPTE IT\n')
                    exit(1)
    else:
        if not os.path.exists(decrypted_file_name):
            print("\nopen: please wait .. now decrypt", encrypted_file_name, "to be", decrypted_file_name, "\n")
            decrypt_file(encrypted_file_name, decrypted_file_name, password)

    try:
        with open(decrypted_file_name, 'r') as f:
                data={}
                for i in f:
                    k_v=i.strip().split('=')
                    if len(k_v)==2:
                        key=k_v[0].strip()
                        val=get_type_of_input(k_v[1].strip())
                        data[key] = val
      
        return data
    except Exception as e: print(e)