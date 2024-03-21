```shell
# Generate RSA private key
openssl genrsa -out private.pem 2048
```

```shell
# Generate RSA publick key
openssl rsa -in private.pem -outform PEM -pubout -out publick.pem
```