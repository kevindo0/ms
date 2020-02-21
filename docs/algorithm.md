### 1. RSA
  1. 生成私钥文件 RSA PRIVATE KEY
    ```bash
    openssl genrsa -out sk.pem 1024
    ```
  2. 通过生成的私钥文件签发一个公钥文件  PUBLIC KEY
    ```bash
    openssl rsa -in sk.pem -pubout -out pk.pem
    ```

### 2. 文件格式
  1. DER格式
    * DER是Distinguished Encoding Rules的缩写，DER格式是最常见的X.509证书文件编码格式，以二进制方式进行存储
    该类型文件和PEM文件是同一个证书文件的2种表现形式
    * openssl查看操作 
    ```bash
    openssl x509 -in cert.der -inform der -text -noout
    ```
  2. **PKCS** (Publish Key Cryptography Standard) 公钥加密标准
    * PKCS#12 定义了包含私钥与公钥证书(publish key certificate)的文件格式。私钥采用密码保护。常见的PFX就是履行了PKCS#12。

### 3. 文件扩展名
1. PEM文件（.pem）  
  说明该文件是标准X.509证书文件，编译格式为PEM编码
2. CRT文件(.crt)  
  CRT是certificate的简写，其意义就是证书的意思。编码可以是PEM，也可以是DER，大多数是PEM编码
3. KEY文件(.key)  
  密钥文件，不是X.509证书文件。编码可以是PEM编码，也可以是DER编码
4. CSR文件(.csr)  
  CSR是certificat Signing Request的缩写，即证书签名请求，这个并不是证书，而是向权威证书颁发机构获得签名证书的申请，
  其核心内容是一个公钥，在生成这个申请的时候，同时也会生成一个私钥，私钥要自己保管好。
5. P12/PFX文件（.p12）  
  P12是PKCS#12的简写，是密钥文件的PKCS#12格式。P12文件包含了CRT和KEY两部分内容。需要提取密码才能提取相关内容。
6. JKS文件  
  JKS是JAVA Key Storage的缩写，是java用来存放密钥的文件。一般是java的keytool工具进行生成。

### 4. 格式转换
  * PEM to DER
  ```bash
  openssl x509 -in cert.pem -outform def -out cert.der
  ```
  * DER to PEM
  ```bash
  openssl x509 -in cert.der -inform der -outform pem -out cert.pem
  ```
  * PFX to PEM
  ```bash
  openssl pkcs12 -in file.pfx -out cert.pem -nodes
  ```
  * PFX to private key pem
  ```bash
  openssl pkcs12 -in file.pfx -nocerts -out key.pem
  ```
  * PFX to certificate only
  ```bash
  openssl pkcs12 -in file.pfx -clcerts -nokeys -out cert.pem
  ```
  * removing password from the extracted private key
  ```bash
  openssl rsa -in key.pem -out server.key`
  ```

### 5. 证书
#### 1. 生成自己的CA(Certificate Authority)

##### 1.生成CA的key
```bash
openssl genrsa -des3 -out ca.key 2048
openssl genrsa -out ca.key 2048
```

##### 2. 生成CA证书 -subj参数中“/CN”的值为Master主机名
```bash
openssl req -x509 -new -nodes -key ca.key -subj="/CN=k8s-master" -days 5000 -out ca.crt
```

##### 3. 生成我们的key和csr
```bash
openssl genrsa -out server.key 2048
```
##### 4. 生成证书请求文件(csr文件)
```bash
openssl req -new -key server.key -subj "/CN=k8s-master" -out server.csr
```

##### 5 使用ca的证书和key，生成我们的证书  
这里的set_serial指明了证书的序号，如果证书过期了或者key泄漏了，需要重新发证的时候，就加1
```bash
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -set_serial -days 5000 -out server.crt
```
#### 2. 查看证书
```bash
# 查看KEY信息
openssl rsa -noout -text -in server.key
# 查看CSR信息
openssl req -noout -text -in server.csr
# 查看证书信息
openssl x509 -noout -text -in ca.crt
# 验证证书
openssl verify -CAfile ca.crt server.crt      # server.crt: OK
```
#### 3. Openssl 参数
  * genrsa:  使用RSA算法产生私钥
  * -aes256:  使用256位密钥的AES算法对私钥进行加密
  * -subj:    证书相关的用户信息(subject的缩写)
  * x509:   生成x509格式证书
  * -req:   输入csr文件格式
  * -sha1:  证书摘要采用sha1算法
  * -extensions v3_ca:  按照openssl.cnf文件中配置的v3_ca项添加扩展
  * -CAserial: 指定证书序列号文件的路径
  * -CAcreateserial: 表示创建证书序号号文件，指定的证书名称后加上**.srl**后缀
  * pkcs12:  用来处理pkcs#12格式的证书
  * -clcerts: 导出的是客户端证书
  * -cacerts: 导出的是ca证书
#### 4. 去除私钥密码保护
```bash
openssl rsa -in encryedprivate.key -out unencryed.key
```

### 加解密
1. AES 高级加密标准(Advanced Encryption Standard) 最常见对称加密算法。
实际不，一般是通过RSA加密AES的密钥，传输到接收方，接收方解密得到AES密钥，然后发送方和接收方用AES密钥来通信。

2. AES-ECB 电子密码本模式 (Electronic CodeBook(ECB))
最简单的块密码加密模式，加密前根据加密块大小(如AES为128位)分成若干块，之后将每块使用相同的密钥单独加密。

3. AES-CBC模式加密-密码分组链接模块(Cipher Block Chaining(CBC))
aes-cbc模式加密在加密和解密是需要一个初始化向量(initialization Vector, IV)，在每次加密之前或解密之后，使用初始化向量与明文或密文件异或。
* 加密时，明文首先与IV异或，然后将结果进行加密，得到输出的就是密文件，同时本次的输出密文作为下一个块加密的IV。
* 解密时，先将密文的第一块进行块解密，然后将结果与IV异或，就得到明文，同时本次解密的输入密文作为下一个块解密的IV。

4. CTR (Counter 计算器模式)
在计算器模式下，不再对密方进行加密，而是对一个逐次累加的计算器进行加密，用加密后的比特序列与明文进行异或运算得到密文。

5. MAC(Message Authentication Code 消息验证码)
* 消息验证码是一种与秘钥相关的单项散列函数
* 密文的收发双方需要提前共享一个密钥。密文发送者将密文件的MAC值随密文一起发送，密文接收者通过共享秘钥计算收到密文的MAC值，这样就可以对收到的密文做完整性校验。当篡改者篡改密文后，没有共享秘钥，就无法计算出篡改后的MAC值。
* 如果生成的密文的加密模式是CTP，或者是其他的初始IV的加密模式，需将初始时的计时器或初始向量的值作为附加消息与密文一起计算MAC。

6. GMAC(Galois Message Authentication code mode, 伽罗瓦消息验证码)
就是利用伽罗瓦或(Galois Field, GF, 有限域)乘法运算来计算消息的MAC值。

7. GCM(Galois/Counter Mode)
GCM中的G就是指GMAC, C就是指CTR。
GCM可以提供对消息的加密和完整性校验，另外，还可以提供附加消息的完整性校验。

8. ECDSA: 椭圆曲线数字签名算法, 使用椭圆曲线密码(ECC) 对数字签名算法(DSA)的模拟。
