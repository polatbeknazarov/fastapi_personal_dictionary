# FASTAPI Personal Dictionary (SQLAlchemy, JWT)


# Install

1. Install dependencies using `poetry`:
```bash
poetry install
```
or `pip`:
```bash
pip install -r requirements.txt
```

2. Generate RSA private key:
```shell
# Generate RSA private key
openssl genrsa -out private.pem 2048
```
And publick key:
```shell
# Generate RSA publick key
openssl rsa -in private.pem -outform PEM -pubout -out publick.pem
```

# Launch the server
```bash
python src/main.py
```