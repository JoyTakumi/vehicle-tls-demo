# 车联网双向认证实践报告  
**学生：林小悰**   

---

##   项目背景  

在阅读您关于车联网安全的论文后，我尝试搭建了一套基于PKI的双向认证原型系统，通过本次实践：  

- **初步理解**了TLS握手流程中证书校验的核心机制
- **解决了**OpenSSL签发证书时的`subjectAltName`兼容性问题 
- **验证了**双向认证对防御中间人攻击的有效性 

## 项目文件结构说明

- `server.py` - 车联网云平台服务端（基于Flask实现双向认证）
- `client.py` - 车端智能设备模拟客户端（支持合法/非法证书测试场景）

**证书体系目录（certs/）**：
- `/ca` - 自建根证书颁发机构（CA）

  
- `/server` - 云服务平台数字证书


- `/client` - 合法车端设备证书


- `/invalid` - 攻击测试证书集
  - `fake_ca.crt` - 伪造CA证书（模拟中间人攻击）
  - `invalid_client.crt` - 无效客户端证书（测试证书链验证）
---

## ▍关键技术实现    

### 1. 证书体系搭建 
- 通过手动创建CA根证书，理解了证书链信任机制
- 为服务端/客户端签发专属证书  

```
# 签发证书
openssl x509 -req -in server.csr -CA ../ca/ca.crt -CAkey ../ca/ca.key -out server.crt -days 365
```

- 遇到的困难：运行客户端报`NET::ERR_CERT_COMMON_NAME_INVALID` → 发现必须添加`subjectAltName`扩展

```
# 添加SAN扩展
openssl req -new -key server.key -subj "/CN=carcloud" \
  -addext "subjectAltName = DNS:localhost, IP:127.0.0.1" -out server.csr
```

  

### 2. 基于Flask的双向认证实现  
```python  
# 服务端关键配置（server.py）  
ssl_context.verify_mode = ssl.CERT_REQUIRED  # 必须验证客户端证书  
ssl_context.load_verify_locations(cafile='ca.crt')  # 只信任自建CA
```

### 3. 测试验证成果

| 测试场景            | 预期结果       | 实际输出           |
| ------------------- | -------------- | ------------------ |
| 有效证书访问        | 200 OK         | “车辆状态校验通过” |
| 无证书/无效证书访问 | 服务端拒绝连接 | Connection refused |

以下为运行结果截图：![image-20250228234656508](C:\Users\Takumi\AppData\Roaming\Typora\typora-user-images\image-20250228234656508.png)

这次项目的实现还很基础，期待在您的指导下继续探索！

