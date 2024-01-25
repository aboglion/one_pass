
# ONE_PASS

## Overview

`ONE_PASS` is a sophisticated Python library designed for the secure management and protection of sensitive data, such as configuration files or environmental variables. By leveraging strong encryption algorithms, it ensures that private information is safeguarded from unauthorized access, especially when working with public repositories like GitHub.

## Installation

Install `ONE_PASS` using pip:

```
pip install ONE_PASS
```

## Usage

### Initialization and Managing Secrets

1. **Import and Initialize**: 
   In your Python environment, import and run the `env` function from `ONE_PASS`:
   ```
   import ONE_PASS
   ONE_PASS.env()
   ```
   This will check for the presence of configuration and secret files in your directory.

2. **Configure and Modify Secrets**:
   On the first run, `env` will create a `.p.p` file and a default `secrets.txt` file. Edit `secrets.txt` with your key-value pairs. To add new variables later, simply update `secrets.txt` and delete the existing encrypted file. Running `env` again will generate a new encrypted file with all your current secrets.

3. **Encryption and Decryption**:
   When you run `ONE_PASS.env()`, it either encrypts the data in `secrets.txt` (creating a new encrypted file if it doesn't exist or the previous one was deleted) or decrypts an existing encrypted file, returning the data as a dictionary of key-value pairs.

### Safe for Version Control

- **Automatic `.gitignore` Management**: `ONE_PASS` adds sensitive files (`.p.p` and the encrypted file) to `.gitignore` automatically. 
- **Secure Sharing**: The encrypted file can safely be uploaded to version control systems like GitHub. When downloaded or cloned, `ONE_PASS` can automatically decrypt this file back into a usable format, ensuring continuous security and ease of collaboration.

## Encryption Strength

`ONE_PASS` uses advanced encryption standards to secure your data. It employs a robust key derivation function (KDF) coupled with a powerful encryption algorithm (Fernet, which uses AES in CBC mode with a 128-bit key for encryption) to ensure that your sensitive information is highly secure and resistant to various attack vectors. This approach guarantees that your data remains protected, both at rest and in transit.

## Contributing

We encourage contributions to `ONE_PASS`! If you have suggestions for improvements or find any issues, please feel free to submit pull requests or open issues for discussion.

## License

This project is licensed under the [AGPL License](LICENSE).
