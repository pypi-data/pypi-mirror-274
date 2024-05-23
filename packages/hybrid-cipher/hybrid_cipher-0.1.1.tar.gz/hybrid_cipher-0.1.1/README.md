# hybrid-cipher

Hybrid Encryption Mode with Public-Key Encryption and Symmetric Encryption.

## Install

```
pip install hybrid-cipher
```

## 加密原理

### 加密步骤

1. 生成随机32位临时密钥。
2. 使用RSA公钥加密临时密钥。
3. 使用临时密钥及AES GCM加密算法加密数据内容。
4. 把临时密钥的密文及数据密文相关字段拼接在一起，作为整体密文。

### 解密步骤

1. 分割密文为：临时密钥密文、数据密文相关字段。
2. 使用RSA私钥解密临时密钥密文，得到临时密钥明文。
3. 使用临时密钥明文及AES GCM解密算法解密数据密文相关字段，得到数据明文。

## Usage

```
In [1]: from Crypto.PublicKey import RSA
   ...: from hybrid_cipher import HybridCipher
   ...: 
   ...: sk = RSA.generate(1024)

In [2]: 

In [2]: cipher = HybridCipher(sk)

In [3]: cipher.encrypt({"a": "b"})
Out[3]: 'LS8T8hzgCfzo9QzlJ8pO7DD+pSolam9EZIhr35gTSGQayTj2NLqPgx7T8VGbgC2EnAf7fuFN0EXNlljQt1Vg9EyUC8sAMCRCw21zGN/SQttVQFQrETtZndNw/c5pODMVeVFELKnzbw0E50IC3f4mTd38il6O7fQz9SH7zr8Lle0=.tXn5E6vUHLbufPi7gIEFJg+iZDrxOq73q3ds3ZUHFOA=.51hM5vLf4x3nmwlbKRTgwA==.DK5W89RZ9MCl220YqZo5mA==./0O4k+4zIwIGrw=='

In [4]: cipher.decrypt('LS8T8hzgCfzo9QzlJ8pO7DD+pSolam9EZIhr35gTSGQayTj2NLqPgx7T8VGbgC2EnAf7fuFN0EXNlljQt1Vg9EyUC8sAMCRCw21zGN/SQttVQFQrETtZndNw/c5pODMVeVFELKnzbw0E50IC3f4mTd
   ...: 38il6O7fQz9SH7zr8Lle0=.tXn5E6vUHLbufPi7gIEFJg+iZDrxOq73q3ds3ZUHFOA=.51hM5vLf4x3nmwlbKRTgwA==.DK5W89RZ9MCl220YqZo5mA==./0O4k+4zIwIGrw==')
Out[4]: {'a': 'b'}
```

## Release

### v0.1.1

- First release.
