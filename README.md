### ms
```bash
# 公钥私钥生成
openssl genrsa -out sk.pem 1024
openssl rsa -in sk.pem -pubout -out pk.pem
# jwt
pip install pyjwt
pip install pyjwt[crypto]
```

### tools
* [httpie](https://github.com/jakubroztocil/httpie.git)
* [apidoc](https://apidocjs.com/)
* [pyjwt](https://pyjwt.readthedocs.io/en/latest/installation.html)
