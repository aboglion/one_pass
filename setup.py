from setuptools import setup, find_packages

setup(
    name='ONE_PASS',
    version='0.1',
    packages=find_packages(),
    description='To manage private variables with only one password, a key and the name of the encrypted file. To protect sensitive data from being uploaded to GitHub',
    author='U.N.S',
    author_email='aboglion@gmail.com',
    keywords=['encryption', 'security', 'configuration'],
    install_requires=[
        'cryptography',
    ],
    entry_points={
        'console_scripts': [
            'one-pass=one_pass:env',
        ],
    },
)
